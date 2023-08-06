"""Physical model representing series metadata when using the TSV storage variant."""

from typing import List, Optional

from dbnomics_data_model.model.common import DimensionCode
from dbnomics_data_model.model.series import Series

from ..base_series_json import BaseSeriesJson

__all__ = ["TsvSeriesJson"]


class TsvSeriesJson(BaseSeriesJson):
    """Model for series metadata when using the TSV storage variant.

    Series metadata is stored under the "series" property of dataset.json.
    """

    def to_series(self, *, dimensions_codes_order: Optional[List[DimensionCode]] = None) -> Series:
        """Convert physical model to logical model."""
        return Series.construct(
            metadata=self.to_series_metadata(dimensions_codes_order=dimensions_codes_order), observations=[]
        )
