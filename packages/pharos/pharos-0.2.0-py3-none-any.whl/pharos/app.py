#!/usr/bin/env python3
#
# Copyright 2021 Graviti. All Rights Reserved.
#

"""The api of pharos."""

import os
from typing import Any, Dict, List, Union

from flask import Flask, Response, abort, send_file
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from tensorbay.dataset import Data, Dataset, FusionDataset, RemoteData

app = Flask(__name__, static_folder="dist")
CORS(app)
api = Api(app)


class PharosDataset:  # pylint: disable=too-few-public-methods
    """This class defines the PharosDataset."""

    dataset: Union[Dataset, FusionDataset]
    type: int

    def set_dataset(self, local_dataset: Union[Dataset, FusionDataset]) -> None:
        """Set dataset and type for PharosDataset.

        Arguments:
             local_dataset: The local dataset.

        """
        self.dataset = local_dataset
        self.type = 0 if isinstance(local_dataset, Dataset) else 1


PHAROS_DATASET = PharosDataset()


def _dump_data(data: Union[Data, RemoteData]) -> Dict[str, str]:
    if isinstance(data, Data):
        response_data = {
            "remotePath": data.target_remote_path,
            "localFilePath": os.path.abspath(data.path),
        }
    else:
        response_data = {"remotePath": data.path, "url": data.get_url()}

    return response_data


def _get_root_dir() -> str:
    return os.path.abspath(os.path.dirname(__file__))


def visualize(
    local_dataset: Union[Dataset, FusionDataset],
    host: str = "127.0.0.1",
    port: int = 5000,
    debug: bool = False,
) -> None:
    """This is the starter of pharos app.

    Arguments:
        local_dataset: The local dataset.
        host: The hostname to listen on. Set this to ``'0.0.0.0'`` to
            have the server available externally as well.
        port: The port of the webserver.
        debug: Whether to enable debug mode.

    Raises:
        TypeError: When the dataset is not a Dataset or FusionDataset.

    """
    if not isinstance(local_dataset, (Dataset, FusionDataset)):
        raise TypeError("It is not a Dataset or FusionDataset.")

    PHAROS_DATASET.set_dataset(local_dataset)
    app.run(host, port, debug)


@app.route("/")
def pharos() -> Response:
    """The api about getting static resource in the repo.

    Returns:
        Main entrance of pharos.

    """
    return send_file(os.path.join(app.root_path, "dist", "index.html"))


@app.route("/<path:path>")
def get_static_resource(path: str) -> Response:
    """The api about getting static resource in the repo.

    Arguments:
        path: The relative path of static resource.

    Returns:
        Static resource in the repo.

    """
    return send_file(os.path.join(app.root_path, "dist", path), as_attachment=True)


class SegmentList(Resource):  # type: ignore[misc]
    """This class defines the relative api about segment list."""

    def __init__(self) -> None:
        super().__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "limit",
            type=int,
            required=False,
            default=128,
            location="args",
        )
        self.reqparse.add_argument(
            "offset",
            type=int,
            required=False,
            default=0,
            location="args",
        )
        self.reqparse.add_argument(
            "sortBy",
            type=str,
            required=False,
            choices=("asc", "desc"),
            default="asc",
            location="args",
        )

    def get(self) -> Dict[str, Any]:
        """Get segment list.

        Returns:
            Segment list.

        """
        args = self.reqparse.parse_args()
        limit = args["limit"]
        offset = args["offset"]
        sort_by = args["sortBy"]

        response_segments = [
            {"name": segment.name, "description": segment.description}
            for segment in PHAROS_DATASET.dataset[offset : offset + limit]
        ]

        response: Dict[str, Any] = {
            "segments": response_segments,
            "offset": offset,
            "recordSize": len(response_segments),
            "totalCount": len(PHAROS_DATASET.dataset),
        }

        if sort_by == "desc":
            response["segments"].reverse()
        return response


class CatalogList(Resource):  # type: ignore[misc]
    """This class defines the relative api about catalog."""

    @staticmethod
    def get() -> Dict[str, Any]:
        """Get catalog.

        Returns:
            Catalog.

        """
        return {"catalogs": PHAROS_DATASET.dataset.catalog.dumps()}


class NoteList(Resource):  # type: ignore[misc]
    """This class defines the relative api about note."""

    @staticmethod
    def get() -> Dict[str, Any]:
        """Get notes.

        Returns:
            Notes

        """
        response_note = {"notes": {"type": PHAROS_DATASET.type}}
        response_note["notes"].update(PHAROS_DATASET.dataset.notes.dumps())
        return response_note


Label_Types = [
    {"labelKey": "BOX2D", "labelType": "2D BOX"},
    {"labelKey": "CLASSIFICATION", "labelType": "CLASSIFICATION"},
    {"labelKey": "POLYGON2D", "labelType": "2D POLYGON"},
    {"labelKey": "POLYLINE2D", "labelType": "2D POLYLINE"},
    {"labelKey": "CUBOID2D", "labelType": "2D CUBOID"},
    {"labelKey": "BOX3D", "labelType": "3D BOX"},
    {"labelKey": "KEYPOINTS2D", "labelType": "KEYPOINTS"},
    {"labelKey": "SENTENCE", "labelType": "Audio Sentence"},
]


class LabelTypeList(Resource):  # type: ignore[misc]
    """This class defines the relative api about label type list."""

    @staticmethod
    def get() -> Dict[str, Any]:
        """Get label type list.

        Returns:
            Label type list.

        """
        return {"labelTypes": Label_Types}


class DataUriList(Resource):  # type: ignore[misc]
    """This class defines the relative api about data uri list."""

    def __init__(self) -> None:
        super().__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "segmentName",
            type=str,
            required=False,
            default="",
            location="args",
        )
        self.reqparse.add_argument(
            "remotePath",
            type=str,
            required=False,
            location="args",
        )
        self.reqparse.add_argument(
            "limit",
            type=int,
            required=False,
            default=128,
            location="args",
        )
        self.reqparse.add_argument(
            "offset",
            type=int,
            required=False,
            default=0,
            location="args",
        )
        self.reqparse.add_argument(
            "sortBy",
            type=str,
            required=False,
            choices=("asc", "desc"),
            default="asc",
            location="args",
        )

    def get(self) -> Dict[str, Any]:
        """Get data url list.

        Returns:
            Data url list.

        """
        args = self.reqparse.parse_args()
        limit = args["limit"]
        offset = args["offset"]
        sort_by = args["sortBy"]
        segment_name = args["segmentName"]

        try:
            segment = PHAROS_DATASET.dataset[segment_name]
        except KeyError:
            abort(404, f"Segment:'{segment_name}' does not exist.")

        if PHAROS_DATASET.type == 0:
            response_urls: List[Any] = [
                _dump_data(data) for data in segment[offset : offset + limit]
            ]
        else:
            response_urls = []
            for frame in segment[offset : offset + limit]:
                response_data_list: List[Any] = []
                response_frame = {
                    "frameId": frame.frame_id if hasattr(frame, "frame_id") else "",
                    "frame": response_data_list,
                }
                for sensor_name, data in frame.items():
                    response_data = {"sensorName": sensor_name}
                    response_data.update(_dump_data(data))
                    response_data_list.append(response_data)
                response_urls.append(response_frame)

        response: Dict[str, Any] = {
            "segmentName": segment_name,
            "type": PHAROS_DATASET.type,
            "urls": response_urls,
            "offset": offset,
            "recordSize": len(response_urls),
            "totalCount": len(segment),
        }

        if sort_by == "desc":
            response["urls"].reverse()
        return response


class LabelList(Resource):  # type: ignore[misc]
    """This class defines the relative api about label list."""

    def __init__(self) -> None:
        super().__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "segmentName",
            type=str,
            required=False,
            default="",
            location="args",
        )
        self.reqparse.add_argument(
            "limit",
            type=int,
            required=False,
            default=128,
            location="args",
        )
        self.reqparse.add_argument(
            "offset",
            type=int,
            required=False,
            default=0,
            location="args",
        )
        self.reqparse.add_argument(
            "sortBy",
            type=str,
            required=False,
            choices=("asc", "desc"),
            default="asc",
            location="args",
        )

    def get(self) -> Dict[str, Any]:
        """Get label list.

        Returns:
            Label list.

        """
        args = self.reqparse.parse_args()
        limit = args["limit"]
        offset = args["offset"]
        sort_by = args["sortBy"]
        segment_name = args["segmentName"]
        try:
            segment = PHAROS_DATASET.dataset[segment_name]
        except KeyError:
            abort(404, f"Segment:'{segment_name}' does not exist.")

        response_labels: List[Any] = []
        if PHAROS_DATASET.type == 0:
            for data in segment[offset : offset + limit]:
                response_data = {
                    "remotePath": data.target_remote_path if isinstance(data, Data) else data.path,
                    "label": data.label.dumps(),
                }
                response_labels.append(response_data)

        else:
            for frame in segment[offset : offset + limit]:
                response_data_list: List[Any] = []
                response_frame = {
                    "frameId": frame.frame_id if hasattr(frame, "frame_id") else "",
                    "frame": response_data_list,
                }
                for sensor_name, data in frame.items():
                    response_data = {
                        "sensorName": sensor_name,
                        "remotePath": data.target_remote_path
                        if isinstance(data, Data)
                        else data.path,
                        "label": data.label.dumps(),
                    }
                    response_data_list.append(response_data)
                response_labels.append(response_frame)

        response: Dict[str, Any] = {
            "segmentName": segment_name,
            "type": PHAROS_DATASET.type,
            "labels": response_labels,
            "offset": offset,
            "recordSize": len(response_labels),
            "totalCount": len(segment),
        }

        if sort_by == "desc":
            response["labels"].reverse()
        return response


class SensorList(Resource):  # type: ignore[misc]
    """This class defines the relative api about sensor list."""

    def __init__(self) -> None:
        super().__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "segmentName",
            type=str,
            required=False,
            default="",
            location="args",
        )

    def get(self) -> Dict[str, Any]:
        """Get sensor list.

        Returns:
            Sensor list.

        """
        if not PHAROS_DATASET.type:
            abort(404, "Please give fusion dataset.")

        args = self.reqparse.parse_args()
        segment_name = args["segmentName"]

        try:
            segment = PHAROS_DATASET.dataset[segment_name]
        except KeyError:
            abort(404, f"Segment:'{segment_name}' does not exist.")

        return {"segmentName": segment_name, "sensors": segment.sensors.dumps()}


class FileDownload(Resource):  # type: ignore[misc]
    """This class defines the relative api about file download."""

    def __init__(self) -> None:
        super().__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "localFilePath",
            type=str,
            required=False,
            default="",
            location="args",
        )

    def get(self) -> Response:  # pylint: disable=inconsistent-return-statements
        """Get file.

        Returns:
            Certain file.

        """
        args = self.reqparse.parse_args()
        file_path = args["localFilePath"]
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        abort(404, f"The local file:'{file_path}' does not exist")


api.add_resource(SegmentList, "/segments")
api.add_resource(CatalogList, "/catalogs")
api.add_resource(NoteList, "/notes")
api.add_resource(LabelTypeList, "/labelTypes")

api.add_resource(DataUriList, "/data/urls")
api.add_resource(LabelList, "/labels")
api.add_resource(SensorList, "/sensors")

api.add_resource(FileDownload, "/downloadFiles")
