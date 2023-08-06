# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
from datetime import datetime
from typing import Dict, List

from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.configuration.structs import ObjectDetectionBBoxFormats
from mlcvzoo_base.configuration.utils import str2bool
from mlcvzoo_base.utils import ensure_dir

from mlcvzoo_tracker.image_track import TrackerState, TrackEvent

logger = logging.getLogger(__name__)


def write_image_tracks_to_mot(
    complete_pallet_track_events: Dict[int, List[TrackEvent]],
    output_file_path: str,
) -> None:
    """
    Write an annotation file in the MOT201617 / MOT2020 format
    based on the given list of image-tracks. Format for is:

    <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <class>, <visibility>

    Args:
        complete_pallet_track_events: 1st key: Frame-ID
                                      2nd key: Track-ID
                                      value: TrackEvent
        output_file_path: The path to the file were the data should be written to

    Returns:
        None
    """

    mot_lines: List[str] = []

    for frame_id, track_events in complete_pallet_track_events.items():
        for track_event in track_events:
            if (
                track_event.state is TrackerState.ACTIVE
                or track_event.state is TrackerState.OCCLUDED
                or track_event.state is TrackerState.INITIATED
            ):
                conf = "1.0"
                visibility = "1.0"
                # IMPORTANT NOTE: Indices in MOT are 1-based, therefore plus 1 for the IDs
                mot_lines.append(
                    f"{frame_id + 1},"
                    f"{track_event.track_id + 1},"
                    f"{track_event.bounding_box.box.xmin},"
                    f"{track_event.bounding_box.box.ymin},"
                    f"{track_event.bounding_box.box.width},"
                    f"{track_event.bounding_box.box.height},"
                    f"{conf},"
                    f"{track_event.bounding_box.class_id + 1},"
                    f"{visibility}\n"
                )

    ensure_dir(file_path=output_file_path, verbose=True)

    logger.debug("Write mot annotation file to '%s'" % output_file_path)
    with open(output_file_path, "w") as output_file:
        output_file.writelines(mot_lines)


def read_image_tracks(input_path: str) -> Dict[int, List[TrackEvent]]:
    """
    Read an annotation file in the MOT201617 / MOT2020 format
    Format for MOT is:

    <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <class>, <visibility>

    Args:
        input_path:

    Returns:

    """
    complete_pallet_track_events: Dict[int, List[TrackEvent]] = {}

    with open(input_path, "r") as input_file:
        mot_lines = input_file.readlines()

    for mot_line in mot_lines:
        mot_line_split = mot_line.strip().split(",")

        # IMPORTANT NOTE: Indices in MOT are 1-based, therefore minus 1 for the IDs
        frame_id = int(mot_line_split[0]) - 1

        if frame_id not in complete_pallet_track_events:
            complete_pallet_track_events[frame_id] = []

        complete_pallet_track_events[frame_id].append(
            TrackEvent(
                bounding_box=BoundingBox(
                    box=Box.init_format_based(
                        box_list=(
                            int(float(mot_line_split[2])),
                            int(float(mot_line_split[3])),
                            int(float(mot_line_split[4])),
                            int(float(mot_line_split[5])),
                        ),
                        box_format=ObjectDetectionBBoxFormats.XYWH,
                    ),
                    class_identifier=ClassIdentifier(
                        class_id=int(mot_line_split[7]) - 1, class_name="MOT"
                    ),
                    score=float(mot_line_split[6]),
                    difficult=False,
                    occluded=str2bool(mot_line_split[8]),
                    content="",
                ),
                timestamp=datetime.now(),
                state=TrackerState.ACTIVE,
                frame_id=frame_id,
                track_id=int(mot_line_split[1]) - 1,
                speed=0.0,
            )
        )

    return complete_pallet_track_events
