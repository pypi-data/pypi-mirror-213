"""Physical model representing a category tree."""

from typing import Any, List, Optional, Union

from pydantic import BaseModel, constr

from dbnomics_data_model.model.category_tree import Category, CategoryTree, CategoryTreeNode, DatasetReference

__all__ = [
    "CategoryJson",
    "CategoryTreeJson",
    "CategoryTreeNodeJson",
    "DatasetReferenceJson",
]


class DatasetReferenceJson(BaseModel):
    """Model for a dataset reference of category_tree.json."""

    code: str
    name: Optional[str]

    def to_domain_model(self) -> DatasetReference:
        """Convert physical model to logical model."""
        return DatasetReference(code=self.code, name=self.name)


class CategoryJson(BaseModel):
    """Model for a category node of category_tree.json."""

    children: List["CategoryTreeNodeJson"]
    code: Optional[constr(regex="^[-0-9A-Za-z._]+$")]  # type:ignore # noqa: F722
    name: Optional[str]
    doc_href: Optional[str]

    def to_domain_model(self) -> Category:
        """Convert physical model to logical model."""
        return Category(
            children=[node.to_domain_model() for node in self.children],
            code=self.code,
            name=self.name,
            doc_href=self.doc_href,
        )


CategoryTreeNodeJson = Union[CategoryJson, DatasetReferenceJson]


def node_from_domain_model(node: CategoryTreeNode) -> CategoryTreeNodeJson:
    if isinstance(node, Category):
        return CategoryJson(
            children=[node_from_domain_model(child) for child in node.children],
            code=node.code,
            name=node.name,
            doc_href=node.doc_href,
        )
    elif isinstance(node, DatasetReference):
        return DatasetReferenceJson(code=node.code, name=node.name)
    else:
        raise ValueError(f"Unexpected type for {node=}")


# Call this after "Category" and "CategoryTreeNode" are defined because they depend on each other.
CategoryJson.update_forward_refs()


class CategoryTreeJson(BaseModel):
    """A category tree referencing datasets."""

    __root__: List[CategoryTreeNodeJson]

    @classmethod
    def from_domain_model(cls, category_tree: CategoryTree) -> "CategoryTreeJson":
        """Convert logical model to physical model."""
        return CategoryTreeJson(__root__=[node_from_domain_model(node) for node in category_tree.children])

    def to_domain_model(self) -> CategoryTree:
        """Convert physical model to logical model."""
        return CategoryTree(children=[node.to_domain_model() for node in self.__root__])

    def to_json(self) -> list[Any]:
        """Return JSON-like data for this instance."""
        return [node.dict() for node in self.__root__]
