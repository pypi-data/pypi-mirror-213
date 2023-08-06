# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module that defines an multi object tracker based on bounding boxes. It utilizes
the ImageTrack class and determines an optimal bounding box to track assignment
by using the principle of the "hungarian algorithm" for minimizing a cost matrix.
"""

import logging
import time
from typing import Any, Dict, List, Optional

import cv2
import numpy as np
from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import compute_iou, euclidean_distance
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from nptyping import Float, NDArray, Shape
from scipy.optimize import linear_sum_assignment

from mlcvzoo_tracker.configuration import TrackerConfig
from mlcvzoo_tracker.image_track import ImageTrack
from mlcvzoo_tracker.types import ImageType

logger = logging.getLogger(__name__)


class HungarianImageTracker:
    """
    Class for matching newly detected bounding boxes to existing tracks via the hungarian algorithm.
    """

    def __init__(
        self, configuration: TrackerConfig, object_class_identifier: ClassIdentifier
    ):
        """
        Initialize this object.
        """

        self.configuration = configuration
        self.current_frame_id: int = 0
        self._tracks: List[ImageTrack] = []
        self.object_class_identifier = object_class_identifier

        self.track_id_counter: int = 0

    def __str__(self) -> str:
        return "{} tracks".format(len(self._tracks))

    def to_list(self, raw_type: bool = False, reduced: bool = False) -> List[Any]:
        """
        Args:
            raw_type: Whether to return the class identifier and timestamp as object or in its representation
                      as dictionary
            reduced: Whether to return the full or a reduced representation of each bounding box and timestamp

        Returns:
            A list of dictionary representations of all stored tracks.
        """
        return [t.to_dict(raw_type=raw_type, reduced=reduced) for t in self._tracks]

    def compute_track_statistics(self) -> Dict[int, Dict[str, Dict[str, Any]]]:
        track_statistics: Dict[int, Dict[str, Dict[str, Any]]] = {}
        for track in self.get_tracks():
            speed_list: List[float] = []
            tracks_widths: List[int] = []
            tracks_heights: List[int] = []
            for track_event in track.track_events.values():
                if track_event.speed > 0.0:
                    speed_list.append(track_event.speed)
                tracks_widths.append(track_event.bounding_box.box.width)
                tracks_heights.append(track_event.bounding_box.box.height)

            if not (
                len(speed_list) > 0
                and len(tracks_widths) > 0
                and len(tracks_heights) > 0
            ):
                continue

            track_statistics[track.track_id] = {
                "speed_info": {
                    "max_speed": max(speed_list),
                    "min_speed": min(speed_list),
                    "avg_speed": sum(speed_list) / len(speed_list),
                },
                "width_info": {
                    "max_width": max(tracks_widths),
                    "min_width": min(tracks_widths),
                    "avg_width": sum(tracks_widths) / len(tracks_widths),
                },
                "height_info": {
                    "max_height": max(tracks_heights),
                    "min_height": min(tracks_heights),
                    "avg_height": sum(tracks_heights) / len(tracks_heights),
                },
            }

        return track_statistics

    def get_valid_tracks(self) -> List[ImageTrack]:
        """
        Get tracks that had enough bounding_boxes updates to be valid and are currently
        still alive (got bounding_boxes lastly).

        Returns:
            All tracks that are valid
        """

        return [track for track in self._tracks if track.is_valid()]

    def get_active_tracks(self) -> List[ImageTrack]:
        """
        Returns:
            All tracks that are active
        """
        return [t for t in self._tracks if t.is_active()]

    def get_alive_tracks(self) -> List[ImageTrack]:
        """
        Returns:
            All tracks that are alive
        """
        return [track for track in self._tracks if track.is_alive()]

    def get_tracks(self) -> List[ImageTrack]:
        """
        Returns:
            All currently managed ImageTrack's of the tracker.
        """
        return self._tracks

    @staticmethod
    def _compute_iou_costs(
        iou_weight: float,
        prev_bbox: Optional[BoundingBox],
        cur_bbox: Optional[BoundingBox],
    ) -> float:
        iou_cost: float = 0.0

        if iou_weight > 0 and prev_bbox and cur_bbox:
            iou_cost = 1.0 - compute_iou(box_1=prev_bbox.box, box_2=cur_bbox.box)

        return iou_cost

    @staticmethod
    def _compute_norm_dist_cost(
        distance_weight: float,
        max_dist: float,
        prev_bbox: Optional[BoundingBox],
        cur_bbox: Optional[BoundingBox],
    ) -> float:
        norm_dist_cost = 0.0
        if distance_weight > 0 and prev_bbox and cur_bbox:
            norm_dist_cost = euclidean_distance(prev_bbox.box, cur_bbox.box) / max_dist

        return norm_dist_cost

    @staticmethod
    def _compute_color_cost(
        color_weight: float,
        prev_hist: Optional[ImageType],
        cur_hist: Optional[ImageType],
    ) -> float:
        # TODO should this be a config parameter, is 10 a reasonable value?
        color_dist_cost = 10.0  # In case it cannot be calculated

        if color_weight > 0 and prev_hist is not None and cur_hist is not None:
            color_dist_cost = cv2.compareHist(prev_hist, cur_hist, 4)

        return color_dist_cost

    @staticmethod
    def _compute_cost_matrix(
        iou_weight: float,
        distance_cost_weight: float,
        color_cost_weight: float,
        alive_tracks: List[ImageTrack],
        bounding_boxes: List[BoundingBox],
        current_hists: List[Optional[ImageType]],
    ) -> ImageType:
        # Span cost Matrix
        # row => alive_tracks
        # column => new bounding boxes

        cost_matrix = np.zeros((len(alive_tracks), len(bounding_boxes)))
        for row, alive_track in enumerate(alive_tracks):
            # TODO: Get the ImageTrack bounding boxes as parameter?
            prev_bbox = alive_track.get_current_bounding_box()
            for col, (cur_bbox, cur_hist) in enumerate(
                zip(bounding_boxes, current_hists)
            ):
                # IoU costs
                iou_cost: float = HungarianImageTracker._compute_iou_costs(
                    iou_weight=iou_weight,
                    prev_bbox=prev_bbox,
                    cur_bbox=cur_bbox,
                )

                # TODO no consequences when exceeding max_dist?

                # Distance costs
                norm_dist_cost: float = HungarianImageTracker._compute_norm_dist_cost(
                    distance_weight=distance_cost_weight,
                    max_dist=alive_track.get_redetect_radius(),
                    prev_bbox=prev_bbox,
                    cur_bbox=cur_bbox,
                )

                # Color costs
                color_dist_cost: float = HungarianImageTracker._compute_color_cost(
                    color_weight=color_cost_weight,
                    prev_hist=alive_track.current_color_hist,
                    cur_hist=cur_hist,
                )

                # Complete weighted cost
                cost_matrix[row, col] = (
                    iou_weight * iou_cost
                    + distance_cost_weight * norm_dist_cost
                    + color_cost_weight * color_dist_cost
                )

        return cost_matrix

    @staticmethod
    def _update_tracks(
        row_ind: NDArray[Shape["Any"], Float],
        col_ind: NDArray[Shape["Any"], Float],
        assignment_threshold: float,
        cost_matrix: NDArray[Shape["Any, Any"], Float],
        alive_tracks: List[ImageTrack],
        bounding_boxes: List[BoundingBox],
        current_hists: List[Optional[ImageType]],
    ) -> List[bool]:
        """
        Calls the update(...) method for all object in the alive-track list.


        Args:
            row_ind:
            col_ind:
            assignment_threshold:
            cost_matrix:
            alive_tracks:
            bounding_boxes:
            current_hists:

        Returns:

        """
        #
        # t1 : b1 - - - bm
        #  |
        #  |
        # tn : b1 - - - bm

        # List that states whether a bounding box entry has been assigned to a track
        are_detections_assigned: List[bool] = len(bounding_boxes) * [False]

        for i in range(len(row_ind)):
            bbox_index = col_ind[i]
            track_index = row_ind[i]

            if (
                cost_matrix[track_index, bbox_index] < assignment_threshold
                and not are_detections_assigned[bbox_index]
            ):
                _t = alive_tracks[row_ind[i]]
                _t.update(bounding_boxes[bbox_index])
                if current_hists[bbox_index] is not None:
                    _t.set_color_histogram(current_hists[bbox_index])
                are_detections_assigned[bbox_index] = True

        return are_detections_assigned

    def next(
        self,
        bounding_boxes: List[BoundingBox],
        frame: Optional[ImageType] = None,
        occlusion_bounding_boxes: Optional[List[BoundingBox]] = None,
    ) -> None:
        """
        Update the internal list of ImageTracks by using
        the given bounding-box and frame information

        Args:
            bounding_boxes: All bounding-boxes for this frame that should be considered
                            as sensor update
            frame: (Optional) The complete image for cutting out
                   color histograms from the given bounding boxes
            occlusion_bounding_boxes: bounding-boxes that can possibly be a reason for
                                      occluding an ImageTrack for this class

        Returns:
            None
        """

        log_timings: bool = False

        current_hists: List[Optional[ImageType]]

        start = time.time()
        if (
            frame is not None
            and self.configuration.assignment_cost_config.color_cost.weight > 0.0
        ):
            # TODO: Check for runtime issues
            current_hists = [
                b.box.color_hist(
                    margin_x=self.configuration.assignment_cost_config.color_cost.margin_x,
                    margin_y=self.configuration.assignment_cost_config.color_cost.margin_y,
                    frame=frame,
                )
                for b in bounding_boxes
            ]
        else:
            current_hists = len(bounding_boxes) * [None]  # type: ignore[assignment]

        if log_timings:
            logger.info("color_hist: %s" % (time.time() - start))

        # List that states whether a bounding box entry has been assigned to a track
        are_detections_assigned: List[bool]

        # Do this if there are already tracks, not in case of first frame
        if self._tracks:
            alive_tracks = self.get_alive_tracks()

            for track in alive_tracks:
                track.predict(occlusion_bounding_boxes=occlusion_bounding_boxes)

            start = time.time()
            cost_matrix: NDArray[
                Shape["Any, Any"], Float
            ] = HungarianImageTracker._compute_cost_matrix(
                iou_weight=self.configuration.assignment_cost_config.iou_weight,
                distance_cost_weight=self.configuration.assignment_cost_config.distance_cost.weight,
                color_cost_weight=self.configuration.assignment_cost_config.color_cost.weight,
                alive_tracks=alive_tracks,
                bounding_boxes=bounding_boxes,
                current_hists=current_hists,
            )
            if log_timings:
                logger.info("_compute_cost_matrix: %s" % (time.time() - start))

            # Based on the cost-matrix run a linear-sum-assignment that is based on the
            # Hungarian algorithm. This solves the problem of assigning new bounding-boxes
            # to active tracks.
            row_ind: NDArray[Shape["Any"], Float]
            col_ind: NDArray[Shape["Any"], Float]
            start = time.time()
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            if log_timings:
                logger.info("linear_sum_assignment: %s" % (time.time() - start))

            start = time.time()
            are_detections_assigned = HungarianImageTracker._update_tracks(
                row_ind=row_ind,
                col_ind=col_ind,
                assignment_threshold=self.configuration.assignment_cost_config.assignment_threshold,
                cost_matrix=cost_matrix,
                alive_tracks=alive_tracks,
                bounding_boxes=bounding_boxes,
                current_hists=current_hists,
            )
            if log_timings:
                logger.info("_update_tracks: %s" % (time.time() - start))
        else:
            are_detections_assigned = len(bounding_boxes) * [False]

        # In case the cost matrix was not square there are unassigned
        # detections or tracks. Therefore:
        # - Create a new track for each unassigned detection
        # - Not updated tracks are just ignored
        for det_idx, (is_assigned, bounding_box) in enumerate(
            zip(are_detections_assigned, bounding_boxes)
        ):
            if not is_assigned:
                self._tracks.append(
                    ImageTrack(
                        configuration=self.configuration,
                        track_id=self.track_id_counter,
                        initial_frame_id=self.current_frame_id,
                        initial_bbox=bounding_box,
                        initial_color_hist=current_hists[det_idx],
                    )
                )
                self.track_id_counter += 1

        self.current_frame_id += 1

        if not self.configuration.keep_dead_tracks:
            self._tracks = [t for t in self._tracks if t.is_alive()]
