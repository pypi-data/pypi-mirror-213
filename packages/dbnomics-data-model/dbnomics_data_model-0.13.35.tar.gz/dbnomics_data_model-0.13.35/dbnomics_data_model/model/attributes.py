"""Attribute model."""

from operator import attrgetter
from typing import List, Optional

from pydantic import BaseModel

from .common import AttributeCode, AttributeValueCode
from .merge_utils import iter_merged_items

__all__ = ["AttributeDef", "AttributeValueDef"]


class AttributeValueDef(BaseModel):
    """Attribute value used in a dataset."""

    code: AttributeValueCode
    label: Optional[str] = None

    def merge(self, other: "AttributeValueDef") -> "AttributeValueDef":
        """Return a copy of self merged with `other`."""
        assert self.code == other.code, (self, other)
        return self.copy(update=dict(other))


class AttributeDef(BaseModel):
    """Attribute used in a dataset."""

    code: AttributeCode
    label: Optional[str] = None
    values: List[AttributeValueDef]

    def merge(self, other: "AttributeDef") -> "AttributeDef":
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
