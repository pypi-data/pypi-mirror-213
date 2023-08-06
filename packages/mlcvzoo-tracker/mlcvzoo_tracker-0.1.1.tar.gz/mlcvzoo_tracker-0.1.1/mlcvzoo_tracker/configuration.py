# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Definition of the TrackerConfig
"""

import logging
from typing import List

import related
from attr import define
from config_builder import BaseConfigClass

logger = logging.getLogger(__name__)


@define
class TrackingToolTrackerConfigObjectSpeed(BaseConfigClass):
    class_id: int = related.IntegerField(required=False)
    x: int = related.IntegerField(required=False)
    b: int = related.IntegerField(required=False, default=0)


@define
class KalmanFilterConfig(BaseConfigClass):
    # Kalman filter related parameter

    # Parameter for the kalman filter itself
    R: int = related.IntegerField(required=False, default=1000)
    P: int = related.IntegerField(required=False, default=10)

    # Use the bounding-boxes for <kalman_delay> frames as tracker positions
    # instead of the position from the filter.
    # Reason: We need some detections to be able to estimate a good speed.
    kalman_delay: int = related.IntegerField(required=False, default=10)


@define
class DistanceCostConfig(BaseConfigClass):
    weight: float = related.FloatField(required=False, default=1.0)

    # radius for assignment of detection to track = time not seen * x + b
    obj_speed: List[TrackingToolTrackerConfigObjectSpeed] = related.SequenceField(
        TrackingToolTrackerConfigObjectSpeed, required=False, default=[]
    )


@define
class ColorCostConfig(BaseConfigClass):
    # Color histogram related parameter
    weight: float = related.FloatField(required=False, default=0.0)

    # Margin for cropping the image
    margin_x: float = related.FloatField(required=False, default=0.5)
    margin_y: float = related.FloatField(required=False, default=0.5)
    # Alpha value for the histogram
    color_filter_alpha: float = related.FloatField(required=False, default=0)


@define
class AssignmentCostConfig(BaseConfigClass):
    color_cost: ColorCostConfig = related.ChildField(
        cls=ColorCostConfig, required=False, default=ColorCostConfig()
    )

    distance_cost: DistanceCostConfig = related.ChildField(
        cls=DistanceCostConfig, required=False, default=DistanceCostConfig()
    )

    # Threshold for the total weights that determining if a
    # bounding-box should be assigned to a track, sum of:
    # - IoU costs,
    # - Color Histogram costs
    # - Distance costs
    assignment_threshold: float = related.FloatField(required=False, default=1.5)

    iou_weight: float = related.FloatField(required=False, default=1.0)


@define
class TrackerConfig(BaseConfigClass):
    kalman_filter_config: KalmanFilterConfig = related.ChildField(
        cls=KalmanFilterConfig, required=False, default=KalmanFilterConfig()
    )

    assignment_cost_config: AssignmentCostConfig = related.ChildField(
        cls=AssignmentCostConfig, required=False, default=AssignmentCostConfig()
    )

    # Minimum amount of bounding-box updates for a track to be ACTIVE
    min_detections_active: int = related.IntegerField(required=False, default=5)

    # The maximum number of frames a track is allowed to get no sensor updates.
    # If this value is exceeded, the track is counted as DEAD
    max_age: int = related.IntegerField(required=False, default=20)

    # Whether to keep ImageTracks with the state DEAD
    keep_dead_tracks: bool = related.BooleanField(required=False, default=True)

    def check_values(self) -> bool:
        if self.min_detections_active < 0:
            logger.error("The minimum value for min_detections_active is zero.")
            return False

        if self.max_age < 0:
            logger.error(
                "The minimum value for max_age is zero. In this case, a sensor update is required in each iteration to keep the trace alive."
            )
            return False

        return True
