"""Base class for physical models representing series metadata."""

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field, HttpUrl, constr
from toolz import valfilter

from dbnomics_data_model.model.common import (
    AttributeCode,
    AttributeValueCode,
    DimensionCode,
    DimensionValueCode,
    series_code_re,
)
from dbnomics_data_model.model.series import Series, SeriesMetadata
from dbnomics_data_model.utils import is_empty_collection

__all__ = ["BaseSeriesJson"]


T = TypeVar("T", bound="BaseSeriesJson")


class BaseSeriesJson(BaseModel, ABC):
    """Base class for physical models representing series metadata."""

    code: constr(regex=series_code_re)  # type:ignore

    attributes: Dict[AttributeCode, AttributeValueCode] = Field(default_factory=dict)
    description: Optional[str] = None
    dimensions: Union[
        Dict[DimensionCode, DimensionValueCode],
        List[DimensionValueCode],  # same order than BaseDatasetJson.dimensions_codes_order
    ] = Field(default_factory=dict)
    doc_href: Optional[HttpUrl] = None
    name: Optional[str] = None
    next_release_at: Optional[Union[date, datetime]] = None
    notes: Optional[List[str]] = None
    updated_at: Optional[Union[date, datetime]] = None

    def dict(self, *args, **kwargs) -> dict:  # noqa: A003
        """Generate a dictionary representation of the model."""
        kwargs["exclude_defaults"] = True
        data = super().dict(*args, **kwargs)

        # Use valfilter in addition to "exclude_defaults" because it does not work with
        # fields using default_factory.
        return valfilter(lambda v: not is_empty_collection(v), data)

    @classmethod
    def from_series(cls: Type[T], series: Series) -> T:
        """Convert logical model to physical model."""
        notes = [series.metadata.notes] if series.metadata.notes is not None else None

        return cls(
            attributes=series.metadata.attributes,
            code=series.metadata.code,
            description=series.metadata.description,
            dimensions=series.metadata.dimensions,
            doc_href=series.metadata.doc_href,
            name=series.metadata.name,
            next_release_at=series.metadata.next_release_at,
            notes=notes,
            updated_at=series.metadata.updated_at,
        )

    @classmethod
    def from_series_metadata(cls: Type[T], series_metadata: SeriesMetadata) -> T:
        """Convert logical model to physical model."""
        return cls.from_series(Series(metadata=series_metadata, observations=[]))

    @abstractmethod
    def to_series(self, *, dimensions_codes_order: Optional[List[DimensionCode]] = None) -> Series:
        """Convert physical model to logical model."""

    def to_series_metadata(self, *, dimensions_codes_order: Optional[List[DimensionCode]] = None) -> SeriesMetadata:
        """Convert physical model to logical model.

        Return only the metadata part of the series.
        """
        notes = "\n".join(self.notes) if self.notes is not None else None
        return SeriesMetadata.construct(
            attributes=self.attributes,
            code=self.code,
            description=self.description,
            dimensions=self._get_dimensions_as_dict(dimensions_codes_order=dimensions_codes_order),
            doc_href=self.doc_href,
            name=self.name,
            next_release_at=self.next_release_at,
            notes=notes,
            updated_at=self.updated_at,
        )

    def _get_dimensions_as_dict(
        self, *, dimensions_codes_order: Optional[List[DimensionCode]]
    ) -> Dict[DimensionCode, DimensionValueCode]:
        if isinstance(self.dimensions, dict):
            return self.dimensions

        if isinstance(self.dimensions, list):
            if dimensions_codes_order is None:
                raise ValueError("dimensions_codes_order must be given when dimensions is a list")
            if len(dimensions_codes_order) != len(self.dimensions):
                raise ValueError("dimensions_codes_order and series dimensions must have the same length")
            return dict(zip(dimensions_codes_order, self.dimensions))

        # This should not happen thanks to the class instance validators.
        raise TypeError("Unsupported type for dimensions")
