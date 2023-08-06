"""Releases metadata model."""

import re
from dataclasses import dataclass
from operator import attrgetter
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field, validator

from dbnomics_data_model.errors import DBnomicsDataModelError
from dbnomics_data_model.model.merge_utils import iter_merged_items
from dbnomics_data_model.utils import find

from .common import DatasetCode

__all__ = [
    "NoReleaseError",
    "ReleaseCode",
    "LATEST_RELEASE",
    "RELEASE_CODE_PATTERN",
    "RELEASE_CODE_RE",
    "DatasetRelease",
    "DatasetReleasesItem",
    "ReleasesMetadata",
    "parse_dataset_release",
]

LATEST_RELEASE = "latest"

RELEASE_CODE_PATTERN = r"[-0-9A-Za-z._]+"
RELEASE_CODE_RE = re.compile(RELEASE_CODE_PATTERN)


@dataclass
class NoReleaseError(DBnomicsDataModelError):
    """No release is defined for this dataset."""

    dataset_code: DatasetCode


class ReleaseCode(str):
    """Code of a release."""

    def __init__(self, v):  # noqa: D107
        ReleaseCode.validate(v)
        super().__init__()

    @classmethod
    def __get_validators__(cls):  # noqa: D105
        yield cls.validate

    @classmethod
    def validate(cls, v):  # noqa: D102
        if not isinstance(v, str):
            raise TypeError("string required")
        if RELEASE_CODE_RE.fullmatch(v) is None:
            raise ValueError(f"Release code {v!r} does not conform to pattern {RELEASE_CODE_PATTERN!r}")
        return v


class DatasetRelease(BaseModel):
    """Release of a dataset."""

    code: ReleaseCode

    @validator("code")
    def check_not_latest(cls, v):  # noqa: D102, N805
        if v == LATEST_RELEASE:
            raise ValueError(f"Release code of a dataset must not be {LATEST_RELEASE!r}")
        return v

    def merge(self, other: "DatasetRelease") -> "DatasetRelease":
        """Return a copy of the instance merged with `other`."""
        return self.copy(update=dict(other))


class DatasetReleasesItem(BaseModel):
    """Releases of a dataset."""

    dataset_code_prefix: str
    releases: List[DatasetRelease]
    name: Optional[str] = None

    def find_latest_release_code(self) -> ReleaseCode:
        """Find the code of the latest release of this dataset."""
        return self.releases[-1].code

    def format_release(self, release_code: str) -> str:
        """Return a dataset code with a specific release code."""
        return f"{self.dataset_code_prefix}:{release_code}"

    def merge(self, other: "DatasetReleasesItem") -> "DatasetReleasesItem":
        """Return a copy of the instance merged with `other`."""
        return self.copy(
            update={
                **dict(other),
                "releases": list(
                    iter_merged_items(
                        self.releases,
                        other.releases,
                        key=attrgetter("code"),
                        sort_by_key=True,
                    )
                ),
            }
        )


class ReleasesMetadata(BaseModel):
    """Releases metadata of datasets."""

    dataset_releases: List[DatasetReleasesItem] = Field([], description="List of dataset releases")

    def find_dataset_releases_item(self, dataset_code_prefix: str) -> Optional[DatasetReleasesItem]:
        """Find the dataset releases item corresponding to the given code prefix."""
        return find(
            lambda item: item.dataset_code_prefix == dataset_code_prefix,
            self.dataset_releases,
        )

    def merge(self, other: "ReleasesMetadata") -> "ReleasesMetadata":
        """Return a copy of the instance merged with `other`."""
        return self.copy(
            update={
                **dict(other),
                "dataset_releases": list(
                    iter_merged_items(
                        self.dataset_releases,
                        other.dataset_releases,
                        key=attrgetter("dataset_code_prefix"),
                        sort_by_key=True,
                    )
                ),
            }
        )

    def resolve_release_code(self, dataset_code: DatasetCode) -> str:
        """Resolve the release code of a dataset.

        Some release codes are reserved, like "latest" that references an actual release code.

        If dataset_code references a reserved release code, replace it by the actual one.
        """
        dataset_code_prefix, release_code = parse_dataset_release(dataset_code)

        if release_code is None or release_code != LATEST_RELEASE:
            return dataset_code

        dataset_releases_item = self.find_dataset_releases_item(dataset_code_prefix)
        if dataset_releases_item is None:
            raise NoReleaseError(dataset_code)

        latest_release_code = dataset_releases_item.find_latest_release_code()
        if latest_release_code is None:
            raise NoReleaseError(dataset_code)

        return dataset_releases_item.format_release(latest_release_code)


def parse_dataset_release(dataset_code: DatasetCode) -> Tuple[str, Optional[str]]:
    """Parse a dataset code that may contain a release code.

    Return (dataset_code_prefix, release_code).

    >>> parse_dataset_release('foo')
    ('foo', None)
    >>> parse_dataset_release('foo:bar')
    ('foo', 'bar')
    >>> parse_dataset_release('foo:latest')
    ('foo', 'latest')
    >>> parse_dataset_release('foo:')
    Traceback (most recent call last):
        ...
    ValueError: Release code '' does not conform to pattern '[-0-9A-Za-z._]+'
    >>> parse_dataset_release('foo: ')
    Traceback (most recent call last):
        ...
    ValueError: Release code ' ' does not conform to pattern '[-0-9A-Za-z._]+'
    """
    if ":" not in dataset_code:
        return dataset_code, None
    dataset_code_prefix, release_code = dataset_code.split(":", 1)
    release_code = ReleaseCode(release_code)
    return dataset_code_prefix, release_code
