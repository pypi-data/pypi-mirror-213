"""Storage errors."""

from dataclasses import dataclass
from logging import Logger
from typing import Iterator, Literal, Optional, TypeVar

from dbnomics_data_model.errors import DBnomicsDataModelError
from dbnomics_data_model.model.common import DatasetCode

__all__ = [
    "CategoryTreeLoadError",
    "CategoryTreeSaveError",
    "DatasetDeleteError",
    "DatasetMetadataLoadError",
    "DatasetMetadataSaveError",
    "DatasetNotFoundError",
    "ObservationsLoadError",
    "OnError",
    "process_error",
    "ProviderMetadataLoadError",
    "ProviderMetadataSaveError",
    "ReleasesMetadataLoadError",
    "ReleasesMetadataSaveError",
    "SeriesDeleteError",
    "SeriesLoadError",
    "SeriesMetadataLoadError",
    "SeriesSaveError",
    "StorageDeleteError",
    "StorageError",
    "StorageInitError",
    "StoragePoolInitError",
    "StorageTypeNotSupported",
    "UpdateStrategyNotSupported",
]


@dataclass
class UpdateStrategyNotSupported(DBnomicsDataModelError, ValueError):
    """Update strategy not supported."""

    update_strategy: str


@dataclass
class StorageTypeNotSupported(DBnomicsDataModelError, ValueError):
    """Storage type not supported."""

    storage_type: str


class StorageError(DBnomicsDataModelError):
    """Error about reading or writing DBnomics data."""

    pass


class StorageDeleteError(StorageError):
    """Error deleting data of the provider corresponding to this Storage instance."""

    pass


class StorageInitError(StorageError):
    """Error creating Storage concrete instance."""

    pass


class StoragePoolInitError(StorageError):
    """Error creating StoragePool concrete instance."""

    pass


class CategoryTreeLoadError(StorageError):
    """Error loading category tree in a Storage instance."""

    pass


class CategoryTreeSaveError(StorageError):
    """Error saving category tree to a Storage instance."""

    pass


class DatasetDeleteError(StorageError):
    """Error deleting a dataset in a Storage instance."""

    dataset_code: DatasetCode


class DatasetMetadataLoadError(StorageError):
    """Error loading dataset metadata in a Storage instance."""

    pass


class DatasetMetadataNotFound(DatasetMetadataLoadError):
    """Could not find dataset metadata in a Storage instance."""

    pass


class DatasetMetadataSaveError(StorageError):
    """Error saving dataset metadata to a Storage instance."""

    pass


class DatasetNotFoundError(StorageError):
    """Error finding a dataset in a Storage instance."""

    pass


class ProviderMetadataLoadError(StorageError):
    """Error loading provider metadata in a Storage instance."""

    pass


class ProviderMetadataNotFound(ProviderMetadataLoadError):
    """Could not find provider metadata in a Storage instance."""

    pass


class ProviderMetadataSaveError(StorageError):
    """Error saving provider metadata to a Storage instance."""

    pass


class ReleasesMetadataLoadError(StorageError):
    """Error loading releases metadata in a Storage instance."""

    pass


class ReleasesMetadataSaveError(StorageError):
    """Error saving releases metadata to a Storage instance."""

    pass


class SeriesDeleteError(StorageError):
    """Error deleting a series in a Storage instance."""

    pass


class SeriesLoadError(StorageError):
    """Error loading a series in a Storage instance."""

    pass


class SeriesMetadataLoadError(SeriesLoadError):
    """Error loading series metadata in a Storage instance."""

    pass


class SeriesSaveError(StorageError):
    """Error saving a series to a Storage instance."""

    pass


class ObservationsLoadError(SeriesLoadError):
    """Error loading series observations in a Storage instance."""

    pass


# Error handling in iterators

OnError = Literal["log", "raise", "yield"]


E = TypeVar("E", bound=Exception)


def process_error(error: E, *, logger: Logger, on_error: OnError, from_exc: Optional[Exception] = None) -> Iterator[E]:
    """Process an error raised by an iterator using one of the OnError strategies.

    OnError allows 3 strategies:
    - log: ignore and log the error, allowing the caller to continue
    - raise: raise the error, aborting the caller
    - yield: yield the error, allowing the caller to continue

    If from_error is given, attach it as the cause of the error. This is useful when on_error equals `raise` or `yield`.
    """
    if from_exc is not None:
        error.__cause__ = from_exc

    if on_error == "log":
        # Log repr(error) for compatibility with exception child classes being also dataclasses.
        if error.__traceback__ is not None:
            logger.exception(repr(error))
        else:
            logger.error(repr(error))
    elif on_error == "raise":
        raise error
    elif on_error == "yield":
        yield error
    else:
        raise ValueError(f"Invalid value for on_error: {on_error!r}")
