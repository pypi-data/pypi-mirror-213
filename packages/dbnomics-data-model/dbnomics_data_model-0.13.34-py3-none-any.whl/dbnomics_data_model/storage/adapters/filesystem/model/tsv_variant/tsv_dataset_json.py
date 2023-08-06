"""Physical model representing dataset.json when using the TSV storage variant."""

from typing import List

from pydantic import Field

from dbnomics_data_model.model.series import SeriesMetadata
from dbnomics_data_model.utils import find_index

from ..base_dataset_json import BaseDatasetJson
from .tsv_series_json import TsvSeriesJson

__all__ = ["TsvDatasetJson"]


class TsvDatasetJson(BaseDatasetJson):
    """Model for dataset.json when using the TSV storage variant.

    The dataset.json file contains dataset metadata, and series metadata.
    """

    series: List[TsvSeriesJson] = Field(default_factory=list)

    def create_or_replace_series_metadata(self, series_metadata: SeriesMetadata):
        """Add series metadata if it does not exist, otherwise replace it."""
        existing_series_index = find_index(lambda series: series.code == series_metadata.code, self.series)
        series_json = TsvSeriesJson.from_series_metadata(series_metadata)
        if existing_series_index is None:
            self.series.append(series_json)
            return
        self.series[existing_series_index] = series_json
