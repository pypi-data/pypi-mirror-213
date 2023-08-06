# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for encapsulating the history of an object tracked over time, estimating its
current state even in case of missing updates and managing its lifecycle
"""

from __future__ import annotations

import logging
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import numpy as np
from filterpy.kalman import KalmanFilter
from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import compute_iou, euclidean_distance
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier

from mlcvzoo_tracker.configuration import (
    KalmanFilterConfig,
    TrackerConfig,
    TrackingToolTrackerConfigObjectSpeed,
)
from mlcvzoo_tracker.types import ImageType

logger = logging.getLogger(__name__)

image_type = Union[np.ndarray]


class TrackerState(Enum):
    """
    A Track has three states:

        1. INITIATED: When an ImageTrack is instantiated
        2. ACTIVE: ImageTrack got enough sensor updates
        3. OCCLUDED: The track is occluded by another object and therefore currently
                     not visible. In this state, the bounding-box of the last update
                     before the occlusion will be used, until it is not occluded / gets
                     a sensor update.
        4. DEAD: If a ImageTrack does not get sensor updates for the configured period
                 of frames
    """

    INITIATED = "INITIATED"
    ACTIVE = "ACTIVE"
    OCCLUDED = "OCCLUDED"
    DEAD = "DEAD"


@dataclass
class TrackEvent:
    """
    Class for storing all tracking information related to a single bounding box at the time of a specific frame.
    """

    bounding_box: BoundingBox
    timestamp: datetime
    state: TrackerState
    frame_id: int
    track_id: int
    speed: float

    __timestamp_format: str = "%Y-%m-%d_%H-%M-%S"

    def __repr__(self) -> str:
        return (
            f"TrackEvent - "
            f"timestamp: {self.timestamp.strftime(self.__timestamp_format)} "
            f"state: {self.state} "
            f"frame_id: {self.frame_id} "
            f"track_id: {self.track_id} "
            f"speed: {self.speed} "
            f"bounding_box: {self.bounding_box}"
        )

    def to_dict(self, raw_type: bool = False, reduced: bool = False) -> Dict[str, Any]:
        """
        Args:
            raw_type: Whether to return the class identifier and timestamp as object or in its representation
                      as dictionary
            reduced: Whether to return the full or a reduced representation of each bounding box

        Returns:
            A dictionary representations of the track event
        """
        return {
            "bounding_box": self.bounding_box.to_dict(
                raw_type=raw_type, reduced=reduced
            ),
            "timestamp": self.timestamp
            if raw_type
            else self.timestamp.strftime(self.__timestamp_format),
            "state": self.state.value,
            "frame_id": self.frame_id,
            "track_id": self.track_id,
            "speed": self.speed,
        }

    @staticmethod
    def from_dict(input_dict: Dict[str, Any], reduced: bool = False) -> TrackEvent:
        """
        Creates a new TrackEvent object from the dictionary representation.

        Args:
            input_dict: The dictionary to create the TrackEvent from
            reduced: Whether the input_dict stores a reduced version of information

        Returns:
            The TrackEvent created from the input_dict
        """
        return TrackEvent(
            bounding_box=BoundingBox.from_dict(
                input_dict=input_dict["bounding_box"], reduced=reduced
            ),
            timestamp=datetime.strptime(
                input_dict["timestamp"], TrackEvent.__timestamp_format
            ),
            state=TrackerState(input_dict["state"]),
            frame_id=int(input_dict["frame_id"]),
            track_id=input_dict["track_id"],
            speed=input_dict["speed"],
        )


class ImageTrack:
    """
    Class using Kalman filter to track a single object represented by its bounding box, storing its
    history as a list of TrackEvents and managing the lifecycle of the track.
    """

    def __init__(
        self,
        configuration: TrackerConfig,
        track_id: int,
        initial_frame_id: int,
        initial_bbox: BoundingBox,
        initial_color_hist: Optional[ImageType] = None,
        meta_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize object.

        Args:
            initial_frame_id: The time stamp to start with.
            initial_bbox: First detection.
            configuration: Tracker configuration for this ImageTrack object
            initial_color_hist: Color history of the initial box. Can be None if not used.
            meta_info: Dictionary providing meta information for this ImageTrack object
        """

        # ========================================================
        # Static information

        self.configuration = configuration

        self.track_id = track_id

        # The tracks class-identifier is defined by its initial bounding-box
        self.class_identifier: ClassIdentifier = initial_bbox.class_identifier

        # TODO: Store meta_info per TrackEvent?
        # Dictionary that can be filled with meta information about this ImageTrack
        self.meta_info: Optional[Dict[str, Any]] = meta_info

        self._start_frame_id: int = initial_frame_id

        self.current_state: TrackerState = TrackerState.INITIATED

        # Flag that indicates that the ImageTrack has been active for at least one frame
        self.was_active: bool = False

        if self.configuration.min_detections_active == 0:
            self.current_state = TrackerState.ACTIVE
            self.was_active = True

        # ========================================================
        # Dynamic information that changes with the tracking

        # The current color histogram of this ImageTrack
        self.current_color_hist: Optional[ImageType] = initial_color_hist

        # Will be counted up for every call of next_frame(...)
        self.current_frame_id: int = initial_frame_id

        # Current speed for this ImageTrack, defined as the distance of pixels
        # that the track has traveled between two consecutive frames
        self._current_speed: float = 0.0

        # Current speed for this ImageTrack, defined as the distance of pixels
        # that the track has traveled between two consecutive frames
        self._current_bounding_box: BoundingBox = initial_bbox

        # The complete track. Note that the key is the frame ID and can thus
        # start and end at any time but should not have gaps if next_frame is
        # always called.
        # Key: Frame ID
        self.track_events: Dict[int, TrackEvent] = {
            self.current_frame_id: TrackEvent(
                bounding_box=initial_bbox,
                timestamp=datetime.now(),
                state=self.current_state,
                frame_id=self.current_frame_id,
                track_id=self.track_id,
                speed=0.0,
            )
        }

        # The complete information about sensor updates.
        # Initialization counts as one sensor update.
        # Key: Frame ID
        self._sensor_updates: Dict[int, BoundingBox] = {
            self.current_frame_id: deepcopy(initial_bbox)
        }

        self._kf: KalmanFilter = ImageTrack.create_kalman_filter(
            kalman_filter_config=self.configuration.kalman_filter_config,
            initial_bbox=initial_bbox,
        )

    def __repr__(self) -> str:
        return (
            f"ImageTrack: class-identifier={self.class_identifier}, "
            f"len: {len(self.track_events)}, "
            f"latest_track_event: {self.get_latest_track_event()}"
        )

    def to_dict(self, raw_type: bool = False, reduced: bool = False) -> Dict[str, Any]:
        """
        TODO
        Args:
            raw_type:
            reduced:

        Returns:

        """
        return self.track_events[self.current_frame_id].to_dict(
            raw_type=raw_type, reduced=reduced
        )

    def to_json(self) -> Any:
        return self.to_dict(raw_type=False)

    @property
    def current_speed(self) -> float:
        """
        TODO
        Returns:

        """
        return self._current_speed

    @staticmethod
    def create_kalman_filter(
        kalman_filter_config: KalmanFilterConfig, initial_bbox: BoundingBox
    ) -> KalmanFilter:
        """
        Create a KalmanFilter object from the given configuration
        and initial bounding box.

        State is position and speed for x and y with unit pixel and
        pixel per frame so this is independent of fps. The (x, y)
        position is the center of the box that will be tracked with
        the kalman filter.

        - State transition:
         x      1 1 0 0       x
        dx  =   0 1 0 0      dx
         y      0 0 1 1       y
        dy      0 0 0 1      dy

        - Measurement:
         x      1 0
        dx  =   0 0     z_x
         y      0 1     z_y
        dy      0 0

        Args:
            kalman_filter_config: The KalmanFilterConfig defining the relevant parameter
            initial_bbox: The bounding-box for initializing the KalmanFilter

        Returns:
            The created KalmanFilter object
        """

        kalman_filter: KalmanFilter = KalmanFilter(dim_x=4, dim_z=2)

        kalman_filter.x = np.array(
            [[initial_bbox.box.center()[0]], [0], [initial_bbox.box.center()[1]], [0]]
        )

        kalman_filter.H = np.array([[1, 0, 0, 0], [0, 0, 1, 0]])

        kalman_filter.F = np.array(
            [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]]
        )

        kalman_filter.R = np.array(
            [
                [kalman_filter_config.R, 0],
                [0, kalman_filter_config.R],
            ]
        )

        kalman_filter.P *= kalman_filter_config.P

        # self.kf.Q = Q_discrete_white_noise(dim=4, dt=1, var=0.1)

        return kalman_filter

    def get_start_time(self) -> datetime:
        """
        Returns:
            The datetime object when the track was initially started
        """
        return self.track_events[self._start_frame_id].timestamp

    def get_alive_time(self) -> timedelta:
        """
        Returns:
            The datetime object when the track was initially started
        """
        return datetime.now() - self.track_events[self._start_frame_id].timestamp

    def get_stop_time(
        self,
    ) -> Optional[datetime]:
        """
        Get the stop time of this ImageTrack. When the ImageTrack is still active,
        then it returns None.

        Returns:
            The datetime object when the track was stopped / was not active anymore
        """
        if not self.is_active():
            return self.track_events[max(self.track_events.keys())].timestamp

        return None

    def is_valid(self) -> bool:
        """
        An ImageTrack is valid when it was active for at least one frame

        Returns:
            Whether the ImageTrack is valid
        """
        return self.was_active

    def is_alive(self) -> bool:
        """
        An ImageTrack is alive when it is not in the TrackerState.DEAD state

        Returns:
            Whether a track is alive
        """
        return self.current_state is not TrackerState.DEAD

    def is_active(self) -> bool:
        """
        Determines if a track is still active, based on:

        Returns:
            Whether the track is counted as active based on the described conditions
        """
        return (
            self.current_state is TrackerState.ACTIVE
            or self.current_state is TrackerState.OCCLUDED
        )

    def last_sensor_update_frame_id(self) -> int:
        """
        Determines the last frame ID where a detection was added.
        Can be used to determine how long an object was not detected.

        Returns:
            The frame ID
        """
        return max(self._sensor_updates.keys())

    def set_color_histogram(self, color_hist: Optional[ImageType]) -> None:
        """
        Sets the current color histogram for this track

        Args:
            color_hist: The color histogram to set

        Returns:
            None
        """
        alpha = self.configuration.assignment_cost_config.color_cost.color_filter_alpha
        if self.current_color_hist is not None and alpha < 1:
            self.current_color_hist = (1 - alpha) * self.current_color_hist + alpha * color_hist  # type: ignore
        else:
            self.current_color_hist = color_hist

    def get_latest_track_event(
        self,
    ) -> TrackEvent:
        """
        Determines the latest TrackEvent of this track.

        Returns:
            The determined TrackEvent
        """

        return self.track_events[max(self.track_events.keys())]

    def get_current_bounding_box(self) -> BoundingBox:
        return self._current_bounding_box

    def get_redetect_radius(self) -> float:
        """
        Based on the motion model of objects, this determines a radius where the object could
        have been moved to while it was not detected / got no sensor updates. Note that the
        kalman filter only gives the estimated position based on the last speed. A kalman filter
        does not include such a motion model as applied here.

        Returns:
            The possible radius the object can be found now.
        """

        # TODO discuss readding s0 to relax/widen the radius for redetection
        # Formula:
        # s = v*t + s0  => s0 is always zero, since the distance is measured from the
        #                  center of the bounding.box

        object_speed_config: TrackingToolTrackerConfigObjectSpeed = (
            self.configuration.assignment_cost_config.distance_cost.obj_speed[
                self.class_identifier.class_id
            ]
        )

        return (
            self.current_frame_id - self.last_sensor_update_frame_id()
        ) * object_speed_config.x + object_speed_config.b

    def __update_current_bounding_box(self) -> None:
        """
        Use the bounding-boxes for <kalman_delay> frames as tracker positions
        instead of the position from the filter.
        Reason: We need some detections to be able to estimate a good speed.
        """
        if self.configuration.kalman_filter_config.kalman_delay >= len(
            self._sensor_updates
        ):
            self._current_bounding_box = deepcopy(
                self._sensor_updates[self.last_sensor_update_frame_id()]
            )
        else:
            self._current_bounding_box.box.new_center(
                int(self._kf.x[0]), int(self._kf.x[2])
            )

    def __update_speed_and_track_events(self) -> None:
        # update speed
        if len(self.track_events) >= 2:
            self._current_speed = euclidean_distance(
                box_1=self._current_bounding_box.box,
                box_2=self.track_events[self.current_frame_id - 1].bounding_box.box,
            )

        # update the current TrackEvent
        self.track_events[self.current_frame_id] = TrackEvent(
            bounding_box=self._current_bounding_box,
            timestamp=datetime.now(),
            state=self.current_state,
            frame_id=self.current_frame_id,
            track_id=self.track_id,
            speed=self.current_speed,
        )

    def predict(
        self, occlusion_bounding_boxes: Optional[List[BoundingBox]] = None
    ) -> None:
        """
        Update the internal Kalman filter (prediction step) and the state of this ImageTrack.
        It does not have an effect if the ImageTrack is in the TrackerState.DEAD state.

        Must be called for every frame in the following order:
        predict(...) --> (Optional) update(...)

        Args:
            occlusion_bounding_boxes: Potential bounding boxes of object that might occlude
                                      this track, respectively the current bounding box of
                                      this track

        Returns:
            None
        """

        if self.current_state is TrackerState.DEAD:
            return

        last_sensor_update_frame_id = self.last_sensor_update_frame_id()

        # Check if ImageTrack got to old and therefore is DEAD now
        if (
            self.current_frame_id - last_sensor_update_frame_id
            > self.configuration.max_age
        ):
            self.current_state = TrackerState.DEAD
            self.track_events[max(self.track_events.keys())].state = TrackerState.DEAD

            # return prematurely because the image track is DEAD now
            return

        self.current_frame_id += 1
        self._kf.predict()

        self.__update_current_bounding_box()

        # check occlusion
        if (
            occlusion_bounding_boxes is not None
            and self.current_state is TrackerState.ACTIVE
        ):
            for occlusion_bounding_box in occlusion_bounding_boxes:
                # TODO: Check if this could trigger to much computing time
                if (
                    compute_iou(
                        box_1=occlusion_bounding_box.box,
                        box_2=self._current_bounding_box.box,
                    )
                    > 0.0
                ):
                    # Assume that the bounding box has not changed during the time
                    # the object was occluded
                    self.current_state = TrackerState.OCCLUDED
                    break

        self.__update_speed_and_track_events()

    def update(self, bounding_box: BoundingBox) -> None:
        """
        Perform a sensor update of the internal kalman filter for this
        ImageTrack using the given bounding-box. It does not have an effect
        if the ImageTrack is in the TrackerState.DEAD state

        Should be called once within a step in the following order:
        predict(...) --> (Optional) update(...)

        Args:
            bounding_box: The bounding box that should be used as sensor update

        Returns:
            None
        """

        if self.current_state is TrackerState.DEAD:
            return

        if self.current_state is TrackerState.OCCLUDED:
            self.current_state = TrackerState.ACTIVE

        self._sensor_updates[self.current_frame_id] = deepcopy(bounding_box)
        self._kf.update(bounding_box.box.center())

        # Switch to state ACTIVE when the ImageTrack got enough sensor updates
        if (
            self.current_state is TrackerState.INITIATED
            and len(self._sensor_updates) >= self.configuration.min_detections_active
        ):
            self.current_state = TrackerState.ACTIVE
            self.was_active = True

        self.__update_current_bounding_box()
        self.__update_speed_and_track_events()
