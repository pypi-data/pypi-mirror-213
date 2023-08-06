"""Dataset model."""

from datetime import date, datetime
from operator import attrgetter
from typing import List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, constr, validator

from dbnomics_data_model.utils import find

from .attributes import AttributeDef
from .common import DimensionCode, dataset_code_re
from .dimensions import DimensionDef
from .merge_utils import iter_merged_items
from .releases_metadata import LATEST_RELEASE, parse_dataset_release

__all__ = ["DatasetMetadata"]


class DatasetMetadata(BaseModel):
    """Metadata about a dataset."""

    code: constr(regex=dataset_code_re)  # type:ignore

    attributes: List[AttributeDef] = Field(default_factory=list)
    description: Optional[str] = None
    dimensions: List[DimensionDef] = Field(default_factory=list)
    discontinued: bool = False
    doc_href: Optional[HttpUrl] = None
    name: Optional[str] = None
    next_release_at: Optional[Union[date, datetime]] = None
    notes: Optional[str] = None
    source_href: Optional[HttpUrl] = None
    updated_at: Optional[Union[date, datetime]] = None

    @validator("code")
    def check_release_code(cls, value: str):
        """Check that the release code part of the dataset code is not "latest"."""
        _, release_code = parse_dataset_release(value)
        if release_code == LATEST_RELEASE:
            raise ValueError(f"Invalid release code {LATEST_RELEASE!r}")
        return value

    def find_dimension_by_code(self, dimension_code: DimensionCode) -> Optional[DimensionDef]:
        """Return the dimension having this code, or `None` if not found."""
        return find(lambda dimension: dimension.code == dimension_code, self.dimensions, default=None)

    def merge(self, other: "DatasetMetadata") -> "DatasetMetadata":
        """Return a copy of the instance merged with `other`."""
        assert self.code == other.code, (self, other)
        attributes = list(
            iter_merged_items(
                self.attributes,
                other.attributes,
                key=attrgetter("code"),
            )
        )
        dimensions = list(
            iter_merged_items(
                self.dimensions,
                other.dimensions,
                key=attrgetter("code"),
            )
        )
        return self.copy(
            update={
                **dict(other),
                "attributes": attributes,
                "dimensions": dimensions,
            }
        )
