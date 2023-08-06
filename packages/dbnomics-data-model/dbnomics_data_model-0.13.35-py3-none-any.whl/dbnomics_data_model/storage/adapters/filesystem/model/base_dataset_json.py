"""Base class for physical models representing dataset metadata."""

from datetime import date, datetime
from typing import Dict, Iterator, List, Optional, Tuple, Type, TypeVar, Union

from pydantic import BaseModel, Field, HttpUrl, constr, root_validator
from toolz import valfilter

from dbnomics_data_model.model.attributes import AttributeDef, AttributeValueDef
from dbnomics_data_model.model.common import (
    AttributeCode,
    AttributeValueCode,
    DimensionCode,
    DimensionValueCode,
    dataset_code_re,
)
from dbnomics_data_model.model.dataset_metadata import DatasetMetadata
from dbnomics_data_model.model.dimensions import DimensionDef, DimensionValueDef
from dbnomics_data_model.utils import is_empty_collection

__all__ = ["BaseDatasetJson"]

T = TypeVar("T", bound="BaseDatasetJson")


class BaseDatasetJson(BaseModel):
    """Base class for physical models representing dataset metadata.

    Dataset metadata is stored in the dataset.json file.
    This file can also contain series metadata when using the TSV storage variant.
    """

    code: constr(regex=dataset_code_re)  # type:ignore

    description: Optional[str] = None
    discontinued: bool = False
    doc_href: Optional[HttpUrl] = None
    name: Optional[str] = None
    next_release_at: Optional[Union[date, datetime]] = None
    notes: Optional[List[str]] = None
    source_href: Optional[HttpUrl] = None
    updated_at: Optional[Union[date, datetime]] = None

    attributes_labels: Dict[AttributeCode, Optional[str]] = Field(default_factory=dict)
    attributes_values_labels: Dict[AttributeCode, Dict[AttributeValueCode, Optional[str]]] = Field(default_factory=dict)

    dimensions_codes_order: Optional[List[DimensionCode]] = None
    dimensions_labels: Dict[DimensionCode, Optional[str]] = Field(default_factory=dict)
    dimensions_values_labels: Union[
        Dict[
            DimensionCode,
            Dict[DimensionValueCode, Optional[str]],
        ],
        Dict[
            DimensionCode,
            List[Tuple[DimensionValueCode, Optional[str]]],
        ],
    ] = Field(default_factory=dict)

    @root_validator(pre=False)
    def check_dimensions_labels_keys(cls, values):
        """Validate the keys of the `dimensions_labels` attribute.

        Check that every key of `dimensions_labels` is defined in `dimensions_codes_order`, if it's defined.
        """
        cls._check_extra_keys_versus_dimensions_codes_order(values, attribute_name="dimensions_labels")
        return values

    @root_validator(pre=False)
    def check_dimensions_values_labels_keys(cls, values):
        """Validate the keys of the `dimensions_values_labels` attribute.

        Check that every key of `dimensions_values_labels` is defined in `dimensions_codes_order`, if it's defined.
        """
        cls._check_extra_keys_versus_dimensions_codes_order(values, attribute_name="dimensions_values_labels")
        return values

    @classmethod
    def _check_extra_keys_versus_dimensions_codes_order(cls, values, *, attribute_name: str):
        dimensions_codes_order = values.get("dimensions_codes_order")
        if dimensions_codes_order is None:
            return values
        dimensions_codes_order = set(dimensions_codes_order)
        keys = set(values[attribute_name].keys())
        extra_keys = keys - dimensions_codes_order
        if extra_keys:
            raise ValueError(
                f"The keys {extra_keys!r} are defined in {attribute_name!r} but not in {dimensions_codes_order=}"
            )
        return values

    def dict(self, *args, **kwargs) -> dict:  # noqa: A003
        """Generate a dictionary representation of the model."""
        kwargs["exclude_defaults"] = True
        data = super().dict(*args, **kwargs)

        # Use valfilter in addition to "exclude_defaults" because it does not work with
        # fields using default_factory.
        return valfilter(lambda v: not is_empty_collection(v), data)

    @classmethod
    def from_dataset_metadata(cls: Type[T], dataset_metadata: DatasetMetadata) -> T:
        """Convert logical model to physical model."""
        attributes_labels = {attribute.code: attribute.label for attribute in dataset_metadata.attributes}
        attributes_values_labels = {
            attribute.code: {value.code: value.label for value in attribute.values}
            for attribute in dataset_metadata.attributes
        }

        dimensions_codes_order = [dimension.code for dimension in dataset_metadata.dimensions]
        dimensions_labels = {dimension.code: dimension.label for dimension in dataset_metadata.dimensions}
        dimensions_values_labels = {
            dimension.code: {value.code: value.label for value in dimension.values}
            for dimension in dataset_metadata.dimensions
        }

        notes = [dataset_metadata.notes] if dataset_metadata.notes is not None else None

        return cls.construct(
            attributes_labels=attributes_labels,
            attributes_values_labels=attributes_values_labels,
            code=dataset_metadata.code,
            description=dataset_metadata.description,
            dimensions_codes_order=dimensions_codes_order,
            dimensions_labels=dimensions_labels,
            dimensions_values_labels=dimensions_values_labels,
            discontinued=dataset_metadata.discontinued,
            doc_href=dataset_metadata.doc_href,
            name=dataset_metadata.name,
            next_release_at=dataset_metadata.next_release_at,
            notes=notes,
            source_href=dataset_metadata.source_href,
            updated_at=dataset_metadata.updated_at,
        )

    def to_dataset_metadata(self) -> DatasetMetadata:
        """Convert physical model to logical model."""

        def iter_attributes():
            codes = sorted(set(self.attributes_labels.keys()) | set(self.attributes_values_labels.keys()))
            for code in codes:
                label = self.attributes_labels.get(code)
                values = [
                    AttributeValueDef(code=value_code, label=value_label)
                    for value_code, value_label in self.attributes_values_labels.get(code, {}).items()
                ]
                yield AttributeDef(code=code, label=label, values=values)

        def iter_dimensions():
            for code in self._get_dimensions_codes_order():
                label = self.dimensions_labels.get(code)
                values = [
                    DimensionValueDef(code=value_code, label=value_label)
                    for value_code, value_label in self._iter_dimension_values(code)
                ]
                yield DimensionDef(code=code, label=label, values=values)

        notes = "\n".join(self.notes) if self.notes is not None else None

        # Note: do not call DatasetMetadata.construct to run DatasetMetadata validators like checking release code.
        return DatasetMetadata(
            attributes=list(iter_attributes()),
            code=self.code,
            description=self.description,
            dimensions=list(iter_dimensions()),
            discontinued=self.discontinued,
            doc_href=self.doc_href,
            name=self.name,
            next_release_at=self.next_release_at,
            notes=notes,
            source_href=self.source_href,
            updated_at=self.updated_at,
        )

    def _get_dimensions_codes_order(self) -> List[DimensionCode]:
        if self.dimensions_codes_order is not None:
            return self.dimensions_codes_order
        return sorted(
            set(self.dimensions_labels.keys()) | set(dict(self.dimensions_values_labels).keys()),
        )

    def _iter_dimension_values(
        self, dimension_code: DimensionCode
    ) -> Iterator[Tuple[DimensionValueCode, Optional[str]]]:
        values = self.dimensions_values_labels.get(dimension_code)
        if values is None:
            return
        if isinstance(values, dict):
            values = list(values.items())
        assert isinstance(values, list), values
        yield from values
