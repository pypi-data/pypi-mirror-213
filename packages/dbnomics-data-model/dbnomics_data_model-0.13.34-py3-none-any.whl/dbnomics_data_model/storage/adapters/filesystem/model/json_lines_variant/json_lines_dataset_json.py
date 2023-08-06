"""Physical model representing dataset.json when using the JSON lines storage variant."""

from ..base_dataset_json import BaseDatasetJson

__all__ = ["JsonLinesDatasetJson"]


class JsonLinesDatasetJson(BaseDatasetJson):
    """Model for dataset.json when using the JSON lines storage variant.

    The dataset.json file contains dataset metadata.

    Note: in JSON lines variant, it does not contain series metadata, which are stored in series.jsonl.
    """
