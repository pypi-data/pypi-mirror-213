"""Series model."""

from datetime import date, datetime
from decimal import Decimal
from operator import attrgetter
from typing import Dict, Iterator, List, Literal, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, constr

from dbnomics_data_model.errors import DBnomicsDataModelError

from .common import (
    AttributeCode,
    AttributeValueCode,
    DatasetCode,
    DimensionCode,
    DimensionValueCode,
    SeriesCode,
    series_code_re,
)
from .dimensions import DimensionDef
from .merge_utils import iter_merged_items
from .periods import detect_period_format_strict

__all__ = [
    "DuplicateSeriesError",
    "NotAvailable",
    "Observation",
    "ObservationValue",
    "Period",
    "Series",
    "SeriesMetadata",
]

NotAvailable = Literal["NA"]

# Don't use floats for observation values because of imprecision.
ObservationValue = Union[Decimal, NotAvailable]

Period = str


class DuplicateSeriesError(DBnomicsDataModelError):  # noqa: D101
    error_code: str
    dataset_code: DatasetCode
    series_code: SeriesCode

    def __init__(
        self, message: str, *, error_code: str, dataset_code: DatasetCode, series_code: SeriesCode
    ):  # noqa: D107
        super().__init__(message)
        self.error_code = error_code
        self.dataset_code = dataset_code
        self.series_code = series_code

    def __repr__(self):  # noqa: D105
        return (
            f"{self.__class__.__name__}({str(self)!r}, error_code={self.error_code!r}, "
            f"dataset_code={self.dataset_code!r}, "
            f"series_code={self.series_code!r})"
        )


class SeriesMetadataError(DBnomicsDataModelError):
    """Error about series metadata."""


class SeriesMetadata(BaseModel):
    """Metadata about a series."""

    code: constr(regex=series_code_re)  # type:ignore

    attributes: Dict[AttributeCode, AttributeValueCode] = Field(default_factory=dict)
    description: Optional[str] = None
    dimensions: Dict[DimensionCode, DimensionValueCode] = Field(default_factory=dict)
    doc_href: Optional[HttpUrl] = None
    name: Optional[str] = None
    next_release_at: Optional[Union[date, datetime]] = None
    notes: Optional[str] = None
    updated_at: Optional[Union[date, datetime]] = None

    def generate_name(self, dimensions: List[DimensionDef]) -> str:
        """Generate a name for a time series based on its dimensions.

        It is impossible to generate a name from an empty dimensions list.

        Raise SeriesMetadataError if a dimension code is not found in series,
        or ValueError if dimensions is an empty list.
        """

        def iter_series_name_fragments() -> Iterator[str]:
            for dimension in dimensions:
                dimension_value_code = self.dimensions.get(dimension.code)
                if dimension_value_code is None:
                    raise SeriesMetadataError(f"Series does not define a value for dimension {dimension.code!r}")
                dimension_value = dimension.find_value_by_code(dimension_value_code)
                if dimension_value is None or dimension_value.label is None:
                    yield dimension_value_code
                else:
                    label_usage_count = len([v for v in dimension.values if v.label == dimension_value.label])
                    dimension_value_label = dimension_value.label
                    # If label is used more than once, add the code as a precision.
                    if label_usage_count > 1:
                        dimension_value_label += f" ({dimension_value_code})"
                    yield dimension_value_label

        if len(dimensions) == 0:
            raise ValueError("Could not generate a name from an empty list of dimensions")

        return " - ".join(iter_series_name_fragments())

    def merge(self, other: "SeriesMetadata") -> "SeriesMetadata":
        """Return a copy of the instance merged with `other`."""
        return self.copy(
            update={
                **dict(other),
                "attributes": {**self.attributes, **other.attributes},
                "dimensions": {**self.dimensions, **other.dimensions},
            }
        )


class Observation(BaseModel):
    """An observation of a series."""

    period: Period
    value: ObservationValue

    attributes: Dict[AttributeCode, AttributeValueCode] = Field(default_factory=dict)

    def merge(self, other: "Observation") -> "Observation":
        """Return a copy of the instance merged with `other`."""
        return self.copy(
            update={
                **dict(other),
                "attributes": {**self.attributes, **other.attributes},
            }
        )


class Series(BaseModel):
    """A series with metadata and observations."""

    metadata: SeriesMetadata
    observations: List[Observation]

    def check_observations_are_sorted(self):
        """Check that observations are sorted by period."""
        observations = self.observations
        sorted_observations = sorted(observations, key=attrgetter("period"))
        if observations != sorted_observations:
            raise SeriesMetadataError("Observations are not sorted by period")

    def check_observations_are_unique(self):
        """Check that all observations have a different period."""
        observations = self.observations
        periods = [observation.period for observation in observations]
        if len(periods) != len(set(periods)):
            raise SeriesMetadataError("Some observations have the same period")

    def check_observation_periods(self):
        """Check that all observations have a valid period."""
        last_period_format = None
        for index, observation in enumerate(self.observations):
            period_format = detect_period_format_strict(observation.period)
            if period_format is None:
                raise SeriesMetadataError(f"Period of observation #{index} has an invalid format")
            if last_period_format is not None and last_period_format != period_format:
                raise SeriesMetadataError(
                    f"Period format of observation #{index} is different from the previous observation"
                )
            last_period_format = period_format

    def merge(self, other: "Series") -> "Series":
        """Return a copy of the instance merged with `other`."""
        observations = list(
            iter_merged_items(
                self.observations,
                other.observations,
                key=attrgetter("period"),
                sort_by_key=True,
            )
        )
        return Series.construct(
            metadata=self.metadata.merge(other.metadata),
            observations=observations,
        )
