"""Physical model representing series metadata and data when using the JSON lines storage variant."""

from decimal import Decimal
from typing import Any, Dict, Iterator, List, Literal, Optional, Set, Tuple, Union

from pydantic import Field, root_validator

from dbnomics_data_model.model.common import AttributeCode, AttributeValueCode, DimensionCode
from dbnomics_data_model.model.series import Observation, ObservationValue, Series

from ..base_series_json import BaseSeriesJson

__all__ = ["JsonLinesSeriesItem"]


ObservationAttributes = List[List[Optional[AttributeValueCode]]]
ObservationJsonPeriod = str
ObservationJsonValue = Union[float, Literal["NA"]]
ObservationJson = Tuple[ObservationJsonPeriod, ObservationJsonValue]
RawObservations = List[Any]
SeparatedObservations = Tuple[List[ObservationJson], List[str], ObservationAttributes]

default_observations_header = ["PERIOD", "VALUE"]


class JsonLinesSeriesItem(BaseSeriesJson):
    """Model for series metadata and data when using the JSON lines storage variant.

    Series are stored in the series.jsonl file.
    Each JSON lines item contains:
    - metadata in top-level properties
    - data under the "observations*" properties
    """

    observation_attributes: ObservationAttributes = Field(default_factory=list)
    observations: List[ObservationJson] = Field(default_factory=list)
    observations_header: List[str] = Field(default_factory=lambda: default_observations_header)

    def dict(self, *args, **kwargs) -> dict:  # noqa: A003
        """Generate a dictionary representation of the model.

        Handle specific case about observations and its header.
        """
        data = super().dict(*args, **kwargs)

        if self.observations and self.observations_header:
            data["observations"] = recombine_observations(
                self.observations, self.observations_header, self.observation_attributes
            )
        if "observations_header" in data:
            del data["observations_header"]
        if "observation_attributes" in data:
            del data["observation_attributes"]

        return data

    @root_validator(pre=True)
    def separate_observations_validator(cls, values):
        """Extract observations, attributes and header from "observation" property of JSON lines items."""
        raw_observations = values.get("observations")
        if not raw_observations:
            return values

        observations, observations_header, observation_attributes = separate_observations(raw_observations)
        return {
            **values,
            "observation_attributes": observation_attributes,
            "observations": observations,
            "observations_header": observations_header,
        }

    @classmethod
    def from_series(cls, series: Series) -> "JsonLinesSeriesItem":
        """Convert logical model to physical model."""
        instance = super().from_series(series)
        raw_observations = build_raw_observations_from_series(series)
        observations, observations_header, observation_attributes = separate_observations(raw_observations)
        instance.observations = observations
        instance.observations_header = observations_header
        instance.observation_attributes = observation_attributes
        return instance

    def to_series(self, *, dimensions_codes_order: Optional[List[DimensionCode]] = None) -> Series:
        """Convert physical model to logical model."""

        def build_observation_attributes(index: int) -> Dict[AttributeCode, AttributeValueCode]:
            if self.observation_attributes is None or self.observations_header is None:
                return {}
            codes = self.observations_header[2:]
            values = self.observation_attributes[index]
            return {k: v for k, v in zip(codes, values) if v}

        def build_observation_value(json_value: ObservationJsonValue) -> ObservationValue:
            if isinstance(json_value, float):
                return Decimal.from_float(json_value)
            return json_value

        def iter_observations() -> Iterator[Observation]:
            for index, observation in enumerate(self.observations or []):
                yield Observation.construct(
                    period=observation[0],
                    value=build_observation_value(observation[1]),
                    attributes=build_observation_attributes(index),
                )

        return Series.construct(
            metadata=self.to_series_metadata(dimensions_codes_order=dimensions_codes_order),
            observations=list(iter_observations()),
        )


def build_raw_observations_from_series(series: Series) -> RawObservations:
    attribute_codes_set: Set[AttributeCode] = set()
    for observation in series.observations:
        attribute_codes_set |= observation.attributes.keys()
    attribute_codes = sorted(attribute_codes_set)

    header: List[Any] = default_observations_header + attribute_codes

    rows: List[Any] = [
        [
            observation.period,
            float(observation.value) if isinstance(observation.value, Decimal) else observation.value,
        ]
        + [observation.attributes.get(code, "") for code in attribute_codes]
        for observation in series.observations
    ]

    if len(rows) == 0:
        return []

    return [header] + rows


def separate_observations(raw_observations: RawObservations) -> SeparatedObservations:
    if len(raw_observations) == 0:
        return [], default_observations_header, []

    observations_header = raw_observations[0]
    if observations_header[0] != "PERIOD" or observations_header[1] != "VALUE":
        raise ValueError("Observations header should start with PERIOD and VALUE")

    observation_attributes = []
    observations = []
    rows = raw_observations[1:]
    for row in rows:
        period, value = row[:2]
        attributes = row[2:]
        observations.append((period, value))
        observation_attributes.append(attributes)

    return (observations, observations_header, observation_attributes)


def recombine_observations(
    observations: List[ObservationJson], observations_header: List[str], observation_attributes: ObservationAttributes
) -> RawObservations:
    if len(observations) == 0:
        return []

    recombined: RawObservations = [observations_header]
    observations_with_attributes = [
        [*observation, *attributes] for observation, attributes in zip(observations, observation_attributes)
    ]
    recombined.extend(observations_with_attributes)
    return recombined
