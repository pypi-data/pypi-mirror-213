"""Dimension model."""

from operator import attrgetter
from typing import List, Optional

from pydantic import BaseModel

from dbnomics_data_model.utils import find

from .common import DimensionCode, DimensionValueCode
from .merge_utils import iter_merged_items

__all__ = ["DimensionDef", "DimensionValueDef"]


class DimensionValueDef(BaseModel):
    """Dimension value definition."""

    code: DimensionValueCode
    label: Optional[str] = None

    def merge(self, other: "DimensionValueDef") -> "DimensionValueDef":
        """Return a copy of self merged with `other`."""
        assert self.code == other.code, (self, other)
        return self.copy(update=dict(other))


class DimensionDef(BaseModel):
    """Dimension definition."""

    code: DimensionCode
    label: Optional[str] = None
    values: List[DimensionValueDef]

    def find_value_by_code(self, dimension_value_code: DimensionValueCode) -> Optional[DimensionValueDef]:
        """Find a dimension value definition by its code."""
        return find(lambda value: value.code == dimension_value_code, self.values, default=None)

    def merge(self, other: "DimensionDef") -> "DimensionDef":
        """Return a copy of self merged with `other`."""
        assert self.code == other.code, (self, other)
        return self.copy(
            update={
                **dict(other),
                "values": list(
                    iter_merged_items(
                        self.values,
                        other.values,
                        key=attrgetter("code"),
                    )
                ),
            }
        )
