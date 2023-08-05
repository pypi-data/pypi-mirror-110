"""dataset.py
============
The dataset and dataset frame classes.
"""

import datetime
import json
from io import IOBase
from tempfile import NamedTemporaryFile
import pyarrow as pa
import numpy as np
import pandas as pd
import re
from typing import Any, Optional, Union, Callable, List, Dict, Tuple, Set, IO, cast
from typing_extensions import Protocol, TypedDict

from .util import (
    _is_one_gb_available,
    assert_valid_name,
    add_object_user_attrs,
    create_temp_directory,
    mark_temp_directory_complete,
    TYPE_PRIMITIVE_TO_STRING_MAP,
    USER_METADATA_PRIMITIVE,
    POLYGON_VERTICES_KEYS,
    POSITION_KEYS,
    ORIENTATION_KEYS,
    KEYPOINT_KEYS,
    MAX_FRAMES_PER_BATCH,
    GtLabelEntryDict,
    FrameEmbeddingDict,
    CropEmbeddingDict,
    LabelType,
    LabelFrameSummary,
)
from .frames import BaseFrame
from .labels import GTLabelSet, InferenceLabelSet


class GTFrameWithEmbeddings(Protocol):
    embedding: FrameEmbeddingDict
    _labels: GTLabelSet


class LabeledFrame(BaseFrame):
    """A labeled frame for a dataset.

    Args:
        frame_id (str): A unique id for this frame.
        date_captured (str, optional): ISO formatted datetime string. Defaults to None.
        device_id (str, optional): The device that generated this frame. Defaults to None.
    """

    _labels: GTLabelSet

    def __init__(
        self,
        *,
        frame_id: str,
        date_captured: Optional[str] = None,
        device_id: Optional[str] = None,
    ) -> None:
        super(LabeledFrame, self).__init__(
            frame_id=frame_id, date_captured=date_captured, device_id=device_id
        )

        self._labels = GTLabelSet(frame_id=frame_id)

    def _all_label_classes(self) -> List[str]:
        return self._labels._all_label_classes()

    def add_crop_embedding(
        self, *, label_id: str, embedding: List[float], model_id: str = ""
    ) -> None:
        """Add a per label crop embedding

        Args:
            label_id (str): [description]
            embedding (List[float]): A vector of floats between length 0 and 12,000.
            model_id (str, optional): The model id used to generate these embeddings. Defaults to "".
        """
        self._labels.add_crop_embedding(
            label_id=label_id, embedding=embedding, model_id=model_id
        )

    # TODO: Better datamodel for embeddings, make it more first class
    def add_embedding(
        self,
        *,
        embedding: List[float],
        crop_embeddings: Optional[List[CropEmbeddingDict]] = None,
        model_id: str = "",
    ) -> None:
        """DEPRECATED! PLEASE USE add_frame_embedding and add_crop_embedding
        Add an embedding to this frame, and optionally to crops/labels within it.

        If provided, "crop_embeddings" is a list of dicts of the form:
            'uuid': the label id for the crop/label
            'embedding': a vector of floats between length 0 and 12,000.

        Args:
            embedding (list of floats): A vector of floats between length 0 and 12,000.
            crop_embeddings (list of dicts, optional): A list of dictionaries representing crop embeddings. Defaults to None.
            model_id (str, optional): The model id used to generate these embeddings. Defaults to "".
        """
        raise Exception("This method has been deprecated!")

    def add_label_text_token(
        self,
        *,
        sensor_id: str,
        label_id: str,
        index: int,
        token: str,
        classification: str,
        visible: bool,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for a text token.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            index (int): the index of this token in the text
            token (str): the text content of this token
            classification (str): the classification string
            visible (bool): is this a visible token in the text
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """
        self._labels.add_text_token(
            sensor_id=sensor_id,
            label_id=label_id,
            index=index,
            token=token,
            classification=classification,
            visible=visible,
            confidence=None,
            user_attrs=user_attrs,
        )

    # TODO: Dedupe code between here and inferences
    def add_label_3d_cuboid(
        self,
        *,
        label_id: str,
        classification: str,
        position: List[float],
        dimensions: List[float],
        rotation: List[float],
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        links: Optional[Dict[str, Any]] = None,
        coord_frame_id: Optional[str] = None,
    ) -> None:
        """Add a label for a 3D cuboid.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            position (list of float): the position of the center of the cuboid
            dimensions (list of float): the dimensions of the cuboid
            rotation (list of float): the local rotation of the cuboid, represented as an xyzw quaternion.
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
            links (dict, optional): Links between labels. Defaults to None.
            coord_frame_id (str, optional): Coordinate frame id. Defaults to 'world'
        """
        self._labels.add_3d_cuboid(
            label_id=label_id,
            classification=classification,
            position=position,
            dimensions=dimensions,
            rotation=rotation,
            confidence=None,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            links=links,
            coord_frame_id=coord_frame_id,
        )

    def add_label_2d_bbox(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        top: Union[int, float],
        left: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        links: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for a 2D bounding box.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
            links (dict, optional): Links between labels. Defaults to None.
        """
        self._labels.add_2d_bbox(
            sensor_id=sensor_id,
            label_id=label_id,
            classification=classification,
            top=top,
            left=left,
            width=width,
            height=height,
            confidence=None,
            area=None,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            links=links,
        )

    def add_label_2d_keypoints(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        top: Union[int, float],
        left: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        keypoints: List[Dict[KEYPOINT_KEYS, Union[int, float, str]]],
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for a 2D keypoints task.

        A keypoint is a dictionary of the form:
            'x': x-coordinate in pixels
            'y': y-coordinate in pixels
            'name': string name of the keypoint

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            keypoints (list of dicts): The keypoints of this detection
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """
        self._labels.add_2d_keypoints(
            sensor_id=sensor_id,
            label_id=label_id,
            classification=classification,
            top=top,
            left=left,
            width=width,
            height=height,
            keypoints=keypoints,
            confidence=None,
            user_attrs=user_attrs,
        )

    def add_label_2d_polygon_list(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        polygons: List[Dict[POLYGON_VERTICES_KEYS, List[Tuple[Union[int, float]]]]],
        center: Optional[List[Union[int, float]]] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for a 2D polygon list instance segmentation task.

        Polygons are dictionaries of the form:
            'vertices': List of (x, y) vertices (e.g. [[x1,y1], [x2,y2], ...])
                The polygon does not need to be closed with (x1, y1).
                As an example, a bounding box in polygon representation would look like:

                .. code-block::

                    {
                        'vertices': [
                            [left, top],
                            [left + width, top],
                            [left + width, top + height],
                            [left, top + height]
                        ]
                    }

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            polygons (list of dicts): The polygon geometry
            center (list of ints or floats, optional): The center point of the instance
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """
        self._labels.add_2d_polygon_list(
            sensor_id=sensor_id,
            label_id=label_id,
            classification=classification,
            polygons=polygons,
            confidence=None,
            center=center,
            user_attrs=user_attrs,
        )

    def add_label_2d_semseg(
        self, *, sensor_id: str, label_id: str, mask_url: str
    ) -> None:
        """Add a label for 2D semseg.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            mask_url (str): URL to the pixel mask png.
        """
        self._labels.add_2d_semseg(
            sensor_id=sensor_id, label_id=label_id, mask_url=mask_url
        )

    # TODO: handle secondary labels
    def add_label_2d_classification(
        self,
        *,
        sensor_id: str,
        label_id: str,
        classification: str,
        secondary_labels: Optional[Dict[str, Any]] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for 2D classification.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            secondary_labels (dict, optional): dictionary of secondary labels
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """
        self._labels.add_2d_classification(
            sensor_id=sensor_id,
            label_id=label_id,
            classification=classification,
            secondary_labels=secondary_labels,
            confidence=None,
            user_attrs=user_attrs,
        )

    def add_label_3d_classification(
        self,
        *,
        label_id: str,
        classification: str,
        coord_frame_id: Optional[str] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a label for 3D classification.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            coord_frame_id (str, optional): The coordinate frame id.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """
        self._labels.add_3d_classification(
            label_id=label_id,
            classification=classification,
            confidence=None,
            coord_frame_id=coord_frame_id,
            user_attrs=user_attrs,
        )

    def _to_summary(self) -> LabelFrameSummary:
        """Converts this frame to a lightweight summary dict for internal cataloging

        Returns:
            dict: lightweight summaried frame
        """
        return self._labels._to_summary()


class LabeledDataset:
    """A container used to construct a labeled dataset.

    Typical usage is to create a LabeledDataset, add multiple LabeledFrames to it,
    then serialize the frames to be submitted.
    """

    _frames: List[LabeledFrame]
    _frame_ids_set: Set[str]
    _label_ids_set: Set[str]
    _label_classes_set: Set[str]
    _frame_summaries: List[LabelFrameSummary]
    _temp_frame_file_names: List[str]
    _temp_frame_embeddings_file_names: List[str]
    _temp_frame_file_names_streaming: List[str]
    _temp_frame_embeddings_file_names_streaming: List[str]
    _temp_crop_file_names_streaming: List[str]
    _temp_crop_embeddings_file_names_streaming: List[str]
    pipeline_mode: str

    def __init__(self, *, pipeline_mode: str = "BATCH") -> None:
        self._frames = []
        self._frame_ids_set = set()
        self._label_ids_set = set()
        self._label_classes_set = set()
        self._frame_summaries = []
        current_time = datetime.datetime.now()
        self.temp_file_path = create_temp_directory()
        self._temp_frame_prefix = "al_{}_dataset_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_embeddings_prefix = "al_{}_dataset_frame_embeddings_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_crop_prefix = "al_{}_dataset_crops_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_crop_embeddings_prefix = "al_{}_dataset_crop_embeddings_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_file_names = []
        self._temp_frame_embeddings_file_names = []

        self._temp_frame_file_names_streaming = []
        self._temp_frame_embeddings_file_names_streaming = []
        self._temp_crop_file_names_streaming = []
        self._temp_crop_embeddings_file_names_streaming = []
        self.pipeline_mode = pipeline_mode

    def _cleanup_temp_dir(self) -> None:
        mark_temp_directory_complete(self.temp_file_path)

    def get_first_frame_dict(self) -> Dict[str, Any]:
        if self.pipeline_mode == "STREAMING":
            first_frame_file_name = self._temp_frame_file_names_streaming[0]
            first_crop_file_name = self._temp_crop_file_names_streaming[0]
            with open(first_frame_file_name, "r") as first_frame_file:
                with open(first_crop_file_name, "r") as first_crop_file:
                    first_frame_json = first_frame_file.readline().strip()
                    loaded_streaming: Dict[str, Any] = json.loads(first_frame_json)
                    first_crop_json = first_crop_file.readline().strip()
                    loaded_crop: Dict[str, Any] = json.loads(first_crop_json)
                    loaded_streaming["label_data"] = loaded_crop["label_data"]
                    return loaded_streaming
        else:
            first_frame_file_name = self._temp_frame_file_names[0]
            with open(first_frame_file_name, "r") as first_frame_file:
                first_frame_json = first_frame_file.readline().strip()
                loaded: Dict[str, Any] = json.loads(first_frame_json)
                return loaded

    def _save_rows_to_temp(
        self,
        file_name_prefix: str,
        writefunc: Callable[[IO[Any]], None],
        mode: str = "w",
    ) -> Optional[str]:
        """[summary]

        Args:
            file_name_prefix (str): prefix for the filename being saved
            writefunc ([filelike): function used to write data to the file opened

        Returns:
            str or None: path of file or none if nothing written
        """

        if not _is_one_gb_available():
            raise OSError(
                "Attempting to flush dataset to disk with less than 1 GB of available disk space. Exiting..."
            )

        data_rows_content = NamedTemporaryFile(
            mode=mode, delete=False, prefix=file_name_prefix, dir=self.temp_file_path
        )
        data_rows_content_path = data_rows_content.name
        writefunc(data_rows_content)

        # Nothing was written, return None
        if data_rows_content.tell() == 0:
            return None

        data_rows_content.seek(0)
        data_rows_content.close()
        return data_rows_content_path

    def _flush_to_disk(self) -> None:
        """Writes the all the frames in the frame buffer to temp file on disk"""
        if self.pipeline_mode == "STREAMING":
            self._flush_to_disk_streaming()
        else:
            if len(self._frames) == 0:
                return
            frame_path = self._save_rows_to_temp(
                self._temp_frame_prefix, lambda x: self.write_to_file(x)
            )
            if frame_path:
                self._temp_frame_file_names.append(frame_path)
            embeddings_path = self._save_rows_to_temp(
                self._temp_frame_embeddings_prefix,
                lambda x: self.write_embeddings_to_file(x),
                mode="wb",
            )
            if embeddings_path:
                self._temp_frame_embeddings_file_names.append(embeddings_path)

            self._frames = []

    def _flush_to_disk_streaming(self) -> None:
        """Writes the all the frames in the frame buffer to temp file on disk"""
        if len(self._frames) == 0:
            return
        frame_path = self._save_rows_to_temp(
            self._temp_frame_prefix, lambda x: self.write_frames_to_file_streaming(x)
        )
        crop_path = self._save_rows_to_temp(
            self._temp_crop_prefix, lambda x: self.write_labels_to_file_streaming(x)
        )
        if frame_path:
            self._temp_frame_file_names_streaming.append(frame_path)
        if crop_path:
            self._temp_crop_file_names_streaming.append(crop_path)

        frame_embeddings_path = self._save_rows_to_temp(
            self._temp_frame_embeddings_prefix,
            lambda x: self.write_frame_embeddings_to_file_streaming(x),
            mode="wb",
        )
        if frame_embeddings_path:
            self._temp_frame_embeddings_file_names_streaming.append(
                frame_embeddings_path
            )

        crop_embeddings_path = self._save_rows_to_temp(
            self._temp_crop_embeddings_prefix,
            lambda x: self.write_crop_embeddings_to_file_streaming(x),
            mode="wb",
        )
        if crop_embeddings_path:
            self._temp_crop_embeddings_file_names_streaming.append(crop_embeddings_path)

        self._frames = []

    def _validate_frame(
        self, frame_summary: LabelFrameSummary, project_info: Dict[str, Any]
    ) -> None:
        """Validates single frame in set according to project constraints

        Args:
            frame_summary Dict[str, Any]: dictionary representation of a LabeledFrame's summary
            project_info Dict[str, Any]: metadata about the project being uploaded to
        """

        frame_id = frame_summary["frame_id"]
        primary_task = project_info.get("primary_task")
        if primary_task == "2D_SEMSEG":
            label_counts = frame_summary["label_counts"]

            # 2D_SEMSEG frames may only have one label of type SEMANTIC_LABEL_URL_2D
            if (
                len(label_counts) != 1
                or label_counts.get("SEMANTIC_LABEL_URL_2D", 0) != 1
            ):
                extra_labels = filter(
                    lambda x: x != "SEMANTIC_LABEL_URL_2D", label_counts.keys()
                )
                issue_text = (
                    "has no labels"
                    if not len(label_counts)
                    else f"has label types of {list(extra_labels)}"
                )

                raise Exception(
                    f"Frame {frame_id} {issue_text}. Dataset frames for 2D_SEMSEG projects must have exactly one 2d_semseg label"
                )

    def _validate_frames(self, project_info: Dict[str, Any]) -> None:
        """Validates all frames in set according to project constraints

        Args:
            project_info Dict[str, Any]: metadata about the project being uploaded to
        """
        for frame_summary in self._frame_summaries:
            self._validate_frame(frame_summary, project_info)

    def add_frame(self, frame: LabeledFrame) -> None:
        """Add a LabeledFrame to this dataset.

        Args:
            frame (LabeledFrame): A LabeledFrame in this dataset.
        """
        if not isinstance(frame, LabeledFrame):
            raise Exception("Frame is not an LabeledFrame")

        if frame.frame_id in self._frame_ids_set:
            raise Exception("Attempted to add duplicate frame id.")

        duplicate_label_ids = frame._label_ids_set & self._label_ids_set
        if duplicate_label_ids:
            raise Exception(
                f"Attempted to add duplicate label id(s): {duplicate_label_ids}"
            )

        self._frames.append(frame)
        self._frame_ids_set.add(frame.frame_id)
        self._label_ids_set.update(frame._label_ids_set)
        self._label_classes_set.update(frame._all_label_classes())
        self._frame_summaries.append(frame._to_summary())
        if len(self._frames) >= MAX_FRAMES_PER_BATCH:
            self._flush_to_disk()

    def write_to_file(self, filelike: IO[Any]) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in self._frames:
            row = frame.to_dict()
            row["label_data"] = frame._labels.to_dict()["label_data"]
            filelike.write(json.dumps(row) + "\n")

    def write_embeddings_to_file(self, filelike: IO[Any]) -> None:
        """Write the frame's embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        count = len([frame for frame in self._frames if frame.embedding is not None])

        if count == 0:
            return

        if count != len(self._frames):
            raise Exception(
                "If any frames have user provided embeddings, all frames must have embeddings."
            )

        # TODO: Is there a pattern like type predicate functions we can use
        # to avoid error-prone inline manual casts like this?
        frames_with_embs = cast(List[GTFrameWithEmbeddings], self._frames)

        # Get the first frame embedding dimension
        frame_embedding_dim = len(frames_with_embs[0].embedding["embedding"])
        # Get the first crop embedding dimension
        crop_embedding_dim = 1
        for frame in frames_with_embs:
            if frame._labels.crop_embeddings:
                first_crop_emb = frame._labels.crop_embeddings[0]
                crop_embedding_dim = len(first_crop_emb["embedding"])
                break

        frame_ids = np.empty((count), dtype=object)
        frame_embeddings = np.empty((count), dtype=object)
        crop_ids = np.empty((count), dtype=object)
        crop_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(frames_with_embs):
            frame_ids[i] = frame.embedding["task_id"]
            frame_embeddings[i] = frame.embedding["embedding"]
            crop_ids[i] = [x["uuid"] for x in frame._labels.crop_embeddings]
            crop_embeddings[i] = [x["embedding"] for x in frame._labels.crop_embeddings]

        df = pd.DataFrame(
            {
                "frame_ids": pd.Series(frame_ids),
                "frame_embeddings": pd.Series(frame_embeddings),
                "crop_ids": pd.Series(crop_ids),
                "crop_embeddings": pd.Series(crop_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()

    def write_frames_to_file_streaming(self, filelike: IO[Any]) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in self._frames:
            row = frame.to_dict()
            row["change"] = "ADD"
            filelike.write(json.dumps(row) + "\n")

    def write_labels_to_file_streaming(self, filelike: IO[Any]) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in self._frames:
            row = frame._labels.to_dict()
            row["change"] = "ADD"
            filelike.write(json.dumps(row) + "\n")

    def write_frame_embeddings_to_file_streaming(self, filelike: IO[Any]) -> None:
        """Write the frame's embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """

        count = len([frame for frame in self._frames if frame.embedding is not None])
        if count == 0:
            return

        if count != len(self._frames):
            raise Exception(
                "If any frames have user provided embeddings, all frames must have embeddings."
            )

        # TODO: Is there a pattern like type predicate functions we can use
        # to avoid error-prone inline manual casts like this?
        frames_with_embs = cast(List[GTFrameWithEmbeddings], self._frames)

        frame_ids = np.empty((count), dtype=object)
        frame_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(frames_with_embs):
            frame_ids[i] = frame.embedding["task_id"]
            frame_embeddings[i] = frame.embedding["embedding"]

        df = pd.DataFrame(
            {
                "frame_ids": pd.Series(frame_ids),
                "frame_embeddings": pd.Series(frame_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()

    def write_crop_embeddings_to_file_streaming(self, filelike: IO[Any]) -> None:
        """Write the frame's embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        count = len([frame for frame in self._frames if frame.embedding is not None])

        if count == 0:
            return

        if count != len(self._frames):
            raise Exception(
                "If any frames have user provided embeddings, all frames must have embeddings."
            )

        # TODO: Is there a pattern like type predicate functions we can use
        # to avoid error-prone inline manual casts like this?
        frames_with_embs = cast(List[GTFrameWithEmbeddings], self._frames)

        # Get the first frame embedding dimension
        crop_ids = np.empty((count), dtype=object)
        crop_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(frames_with_embs):
            crop_ids[i] = [x["uuid"] for x in frame._labels.crop_embeddings]
            crop_embeddings[i] = [x["embedding"] for x in frame._labels.crop_embeddings]

        df = pd.DataFrame(
            {
                "crop_ids": pd.Series(crop_ids),
                "crop_embeddings": pd.Series(crop_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()
