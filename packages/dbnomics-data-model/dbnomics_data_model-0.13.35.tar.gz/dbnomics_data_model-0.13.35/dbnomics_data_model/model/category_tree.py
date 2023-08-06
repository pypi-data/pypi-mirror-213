"""Category tree model."""

import dataclasses
import re
from dataclasses import asdict, dataclass, field
from typing import Iterator, Optional, Union

from dbnomics_data_model.errors import DBnomicsDataModelError, DBnomicsValidationError

from .common import CategoryCode, DatasetCode
from .merge_utils import iter_merged_items

__all__ = [
    "Category",
    "CategoryTree",
    "CategoryTreeNode",
    "DatasetReference",
    "DatasetReferenceError",
]

category_code_regex = re.compile("^[-0-9A-Za-z._]+$")


@dataclass
class DatasetReference:
    """Represents a dataset node of a category tree."""

    code: str
    name: Optional[str] = None

    def _get_merge_key(self) -> str:
        """Return a unique identifier for the dataset reference."""
        return self.code

    def merge(self, other: "DatasetReference") -> "DatasetReference":
        """Return a copy of self merged with `other`."""
        if self.code != other.code:
            raise ValueError(f"Both instances must have the same code. Got {self.code=} and {other.code=}.")
        return dataclasses.replace(self, **asdict(other))


class DatasetReferenceError(DBnomicsDataModelError):  # noqa: D101
    dataset_code: DatasetCode

    def __init__(self, message: str, *, dataset_code: DatasetCode):  # noqa: D107
        super().__init__(message)
        self.dataset_code = dataset_code

    def __repr__(self):  # noqa: D105
        return f"{self.__class__.__name__}({str(self)!r}, dataset_code={self.dataset_code!r})"


@dataclass
class Category:
    """Represents a category node of a category tree."""

    children: list["CategoryTreeNode"] = field(default_factory=list)
    code: Optional[CategoryCode] = None
    name: Optional[str] = None
    doc_href: Optional[str] = None

    def __post_init__(self):
        """Run validation checks after instance initialization."""
        self.validate()

    def _get_merge_key(self) -> str:
        """Return a unique identifier for the category."""
        if self.code is not None:
            return self.code
        assert self.name is not None  # Because of check_code_or_name_is_defined
        return self.name

    def check_code(self):
        """Check that the Category code respects the regex."""
        if self.code is not None and category_code_regex.match(self.code) is None:
            raise DBnomicsValidationError(f"Invalid code for {self.__class__.__name__}, got {self.code=}")

    def check_code_or_name_is_defined(self):
        """Check that either code or name is defined."""
        if self.code is None and self.name is None:
            raise DBnomicsValidationError(
                f'One of "code" or "name" attributes must be defined for {self.__class__.__name__}'
            )

    def merge(self, other: "Category") -> "Category":
        """Return a copy of the instance merged with `other`."""
        if self.code != other.code:
            raise ValueError(f"Both instances must have the same code. Got {self.code=} and {other.code=}.")
        return dataclasses.replace(
            self,
            **(
                asdict(other)
                | {
                    "children": list(
                        iter_merged_items(self.children, other.children, key=lambda node: node._get_merge_key())
                    )
                }
            ),
        )

    def validate(self):
        """Run validation checks on instance."""
        self.check_code_or_name_is_defined()
        if self.code is not None:
            self.check_code()


CategoryTreeNode = Union[Category, DatasetReference]


@dataclass
class CategoryTree:
    """A category tree referencing datasets."""

    children: list[CategoryTreeNode]

    def iter_dataset_references(self) -> Iterator[DatasetReference]:
        """Yield datasets referenced by the category tree recursively."""
        yield from iter_dataset_references(self.children)

    def merge(self, other: "CategoryTree") -> "CategoryTree":
        """Return a copy of the instance merged with `other`."""
        return CategoryTree(
            children=list(iter_merged_items(self.children, other.children, key=lambda node: node._get_merge_key()))
        )


def iter_dataset_references(nodes: list[CategoryTreeNode]) -> Iterator[DatasetReference]:
    """Yield datasets referenced by the nodes recursively."""
    for node_index, node in enumerate(nodes):
        if isinstance(node, Category):
            yield from iter_dataset_references(node.children)
        elif isinstance(node, DatasetReference):
            yield node
        else:
            # Should never happen because Pydantic checks types.
            raise ValueError(f"Invalid node type at index {node_index!r}: {node!r}")
