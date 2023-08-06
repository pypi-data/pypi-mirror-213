"""Storage abstract class."""

import abc
import logging
from operator import attrgetter
from typing import Iterable, Iterator, Literal, Optional, Union, overload

from toolz import count

from dbnomics_data_model.errors import DBnomicsDataModelError
from dbnomics_data_model.model.category_tree import CategoryTree, DatasetReferenceError
from dbnomics_data_model.model.common import DatasetCode, SeriesCode
from dbnomics_data_model.model.dataset_metadata import DatasetMetadata
from dbnomics_data_model.model.merge_utils import iter_merged_items
from dbnomics_data_model.model.provider_metadata import ProviderMetadata
from dbnomics_data_model.model.releases_metadata import ReleasesMetadata
from dbnomics_data_model.model.series import DuplicateSeriesError, Series

from .errors import (
    DatasetMetadataLoadError,
    OnError,
    ProviderMetadataNotFound,
    StorageError,
    StorageTypeNotSupported,
    UpdateStrategyNotSupported,
    process_error,
)

__all__ = ["Storage", "SaveMode", "save_modes", "UpdateStrategy", "update_strategies"]

logger = logging.getLogger(__name__)

SaveMode = Literal["append", "create_or_replace", "replace_all"]
save_modes = {"append", "create_or_replace", "replace_all"}

UpdateStrategy = Literal["merge", "replace"]
update_strategies = {"merge", "replace"}


class Storage(abc.ABC):
    """Abstract storage.

    A storage contains data for a specific provider.
    """

    def __enter__(self) -> "Storage":
        """Do nothing by default, can be overloaded in concrete Storage implementations."""
        return self

    @classmethod
    def create(cls, storage_type: str, **storage_kwargs) -> "Storage":
        """Create a concrete Storage implementation given storage_type.

        storage_kwargs are passed to the concrete Storage implementation.
        """
        if storage_type == "filesystem":
            from .adapters.filesystem import FileSystemStorage

            return FileSystemStorage(**storage_kwargs)

        raise StorageTypeNotSupported(storage_type=storage_type)

    def check_dataset_references_of_category_tree(
        self, *, on_error: OnError = "raise"
    ) -> Iterator[DatasetReferenceError]:
        """Check dataset references of category tree in both ways.

        Check that all datasets referenced in category tree exist in storage.

        Check that all the datasets of storage are referenced in the category tree, except for discontinued datasets.

        Skip checks if category tree does not exist.

        Raise CategoryTreeLoadError if category tree exists but could not be loaded.
        """
        category_tree = self.load_category_tree()
        if category_tree is None:
            return

        storage_dataset_codes = set(self.iter_dataset_codes(on_error="log"))
        category_tree_dataset_references = list(category_tree.iter_dataset_references())

        # Check that all datasets referenced in category tree exist in storage.

        for dataset_reference in category_tree_dataset_references:
            if dataset_reference.code in storage_dataset_codes:
                continue
            dataset_code = dataset_reference.code
            error = DatasetReferenceError(
                f"Dataset {dataset_code!r} is referenced in category tree but was not found in storage",
                dataset_code=dataset_code,
            )
            yield from process_error(error, logger=logger, on_error=on_error)

        # Check that all the datasets of storage are referenced in the category tree, except for discontinued datasets.

        category_tree_dataset_codes = {dataset_reference.code for dataset_reference in category_tree_dataset_references}
        for dataset_code in storage_dataset_codes:
            if dataset_code in category_tree_dataset_codes:
                continue

            try:
                dataset_metadata = self.load_dataset_metadata(dataset_code)
            except DatasetMetadataLoadError:
                logger.exception(
                    "Could not load metadata of dataset %r, skipping checking if it's discontinued", dataset_code
                )
            else:
                # Ignore discontinued dataset because they are allowed be absent from category tree.
                if dataset_metadata.discontinued:
                    continue

            error = DatasetReferenceError(
                f"Dataset {dataset_code!r} was found in storage but was not referenced in category tree",
                dataset_code=dataset_code,
            )
            yield from process_error(error, logger=logger, on_error=on_error)

    def check_dataset_references_of_releases_metadata(self) -> Iterator[DatasetReferenceError]:
        """Check that all datasets referenced in releases metadata exist in storage.

        Skip checks if releases metadata do not exist.

        Raise ReleasesMetadataLoadError if releases metadata exist but could not be loaded.
        """
        releases_metadata = self.load_releases_metadata()
        if releases_metadata is None:
            return

        storage_dataset_codes = set(self.iter_dataset_codes(on_error="log"))

        for dataset_releases_item in releases_metadata.dataset_releases:
            for release in dataset_releases_item.releases:
                dataset_code = dataset_releases_item.format_release(release.code)
                if dataset_code not in storage_dataset_codes:
                    yield DatasetReferenceError(
                        f"Dataset {dataset_code!r} is referenced in releases metadata but was not found in storage",
                        dataset_code=dataset_code,
                    )

    def check_dataset_series(
        self, dataset_code: DatasetCode, series_iter: Iterator[Union[Series, DBnomicsDataModelError]]
    ) -> Iterator[DBnomicsDataModelError]:
        """Perform expensive checks on the series of a given dataset.

        Check that series:
        - have a unique code (and name if defined)
        - use dimension codes and dimension value codes that are defined in dataset metadata

        If errors occur while loading series, yield them also.
        """
        seen_series_codes = set()
        seen_series_names = set()

        for series_or_exc in series_iter:
            if isinstance(series_or_exc, DBnomicsDataModelError):
                yield series_or_exc
                continue

            series = series_or_exc
            series_code = series.metadata.code

            # Check that series has a unique code

            if series_code in seen_series_codes:
                yield DuplicateSeriesError(
                    f"Series code {series_code!r} is not unique in the dataset {dataset_code!r}",
                    error_code="DUPLICATE_SERIES_CODE",
                    dataset_code=dataset_code,
                    series_code=series_code,
                )
            else:
                seen_series_codes.add(series_code)

            # Check that series has a unique name, if defined

            if series.metadata.name is not None:
                if series.metadata.name in seen_series_names:
                    yield DuplicateSeriesError(
                        f"Series name {series.metadata.name!r} is not unique in the dataset {dataset_code!r}",
                        error_code="DUPLICATE_SERIES_NAME",
                        dataset_code=dataset_code,
                        series_code=series_code,
                    )
                else:
                    seen_series_names.add(series.metadata.name)

            # Run expensive checks on series
            series.check_observations_are_sorted()
            series.check_observations_are_unique()
            series.check_observation_periods()

    def dataset_has_series(self, dataset_code: DatasetCode) -> bool:
        """Return True if the dataset exists in this Storage."""
        first_series = next(self.iter_dataset_series(dataset_code, include_observations=False), None)
        return first_series is not None

    @abc.abstractmethod
    def delete(self):
        """Delete all data of the provider corresponding to this Storage instance.

        If any error raise StorageDeleteError.
        """
        pass

    @abc.abstractmethod
    def delete_dataset(self, dataset_code: DatasetCode, missing_ok: bool = False):
        """Delete a dataset and its series in this Storage.

        Raise DatasetNotFoundError if dataset doesn't exist and missing_ok = False
        """
        pass

    def get_dataset_count(self) -> int:
        """Return the number of datasets in this Storage instance."""
        return count(self.iter_dataset_codes(on_error="log"))

    @abc.abstractmethod
    def has_dataset(self, dataset_code: DatasetCode) -> bool:
        """Return True if dataset exists in this Storage instance."""
        pass

    @abc.abstractmethod
    @overload
    def iter_dataset_codes(  # noqa: D102
        self,
        *,
        on_error: Literal["log", "raise"] = "raise",
    ) -> Iterator[DatasetCode]:
        pass

    @abc.abstractmethod
    @overload
    def iter_dataset_codes(  # noqa: D102
        self,
        *,
        on_error: Literal["yield"],
    ) -> Iterator[Union[DatasetCode, StorageError]]:
        pass

    @abc.abstractmethod
    def iter_dataset_codes(
        self,
        *,
        on_error: OnError = "raise",
    ) -> Union[Iterator[DatasetCode], Iterator[Union[DatasetCode, StorageError]]]:
        """Yield the code of each dataset in this Storage instance.

        Raise StorageError if it fails to load the dataset codes.
        """

    @abc.abstractmethod
    @overload
    def iter_dataset_series(  # noqa: D102
        self,
        dataset_code: DatasetCode,
        *,
        include_observations: bool = True,
        on_error: Literal["log", "raise"] = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Iterator[Series]:
        ...

    @abc.abstractmethod
    @overload
    def iter_dataset_series(  # noqa: D102
        self,
        dataset_code: DatasetCode,
        *,
        include_observations: bool = True,
        on_error: Literal["yield"],
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Iterator[Union[Series, DBnomicsDataModelError]]:
        ...

    @abc.abstractmethod
    def iter_dataset_series(
        self,
        dataset_code: DatasetCode,
        *,
        include_observations: bool = True,
        on_error: OnError = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Union[Iterator[Series], Iterator[Union[Series, DBnomicsDataModelError]]]:
        """Yield series of the given dataset.

        Observations are included by default in yielded series, but can be disabled.

        If an error occurs while loading a series, by default the error will be raised.
        But if `on_error == "log"`, errors will be ignored and logged,
        and if `on_error == "yield"`, errors will be yielded, allowing the caller to process it and continue.

        Series can be filtered by code by using `series_codes`.
        Note: yielded series are not guaranteed to follow the order of `series_codes`.
        The caller needs to reorder them if needed.
        """
        pass

    @abc.abstractmethod
    def load_category_tree(self) -> Optional[CategoryTree]:
        """Return the category tree defined in this Storage instance.

        If not found return None because category tree is optional.
        """
        pass

    @abc.abstractmethod
    def load_dataset_metadata(self, dataset_code: DatasetCode) -> DatasetMetadata:
        """Return metadata about the dataset in this Storage instance.

        Raise:
        - DatasetMetadataNotFound if not found
        - DatasetMetadataLoadError if it could not be loaded
        """
        pass

    @abc.abstractmethod
    def load_provider_metadata(self) -> ProviderMetadata:
        """Return metadata about the provider in this Storage instance.

        Raise:
        - ProviderMetadataNotFound if not found
        - ProviderMetadataLoadError if it could not be loaded
        """
        pass

    @abc.abstractmethod
    def load_releases_metadata(self) -> Optional[ReleasesMetadata]:
        """Return releases metadata defined in this Storage instance.

        If not found return None because releases are optional.
        """
        pass

    def merge_category_tree(self, other_storage: "Storage"):
        """Merge the category tree of this storage with the one in other_storage."""
        other_category_tree = other_storage.load_category_tree()
        if other_category_tree is None:
            return

        category_tree = self.load_category_tree()
        if category_tree is None:
            self.save_category_tree(other_category_tree)
            return

        merged_category_tree = category_tree.merge(other_category_tree)
        self.save_category_tree(merged_category_tree)

    def merge_dataset(self, dataset_code: DatasetCode, other_storage: "Storage"):
        """Merge the given dataset of this Storage with the one in other_storage.

        Merge dataset metadata, then merge all series (metadata and observations).
        """
        if not self.has_dataset(dataset_code):
            self.replace_dataset(dataset_code, other_storage)
            return

        # Merge dataset metadata
        dataset_metadata = self.load_dataset_metadata(dataset_code)
        other_dataset_metadata = other_storage.load_dataset_metadata(dataset_code)
        merged_dataset_metadata = dataset_metadata.merge(other_dataset_metadata)

        # Merge all series
        series_iter = self.iter_dataset_series(dataset_code, include_observations=True)
        other_series_iter = other_storage.iter_dataset_series(dataset_code, include_observations=True)
        merged_series_iter = list(
            iter_merged_items(
                series_iter,
                other_series_iter,
                key=attrgetter("metadata.code"),
            )
        )

        # Do the save
        self.save_dataset_metadata(merged_dataset_metadata)
        self.save_dataset_series(dataset_code, merged_series_iter, mode="replace_all")

    def merge_releases_metadata(self, other_storage: "Storage"):
        """Merge the releases metadata of this storage with the one in other_storage."""
        other_releases_metadata = other_storage.load_releases_metadata()
        if other_releases_metadata is None:
            return

        releases_metadata = self.load_releases_metadata()
        if releases_metadata is None:
            self.save_releases_metadata(other_releases_metadata)
            return

        merged_releases_metadata = releases_metadata.merge(other_releases_metadata)
        self.save_releases_metadata(merged_releases_metadata)

    def replace_category_tree(self, other_storage: "Storage"):
        """Replace the category of this Storage instance by the one in other_storage, if it exists."""
        other_category_tree = other_storage.load_category_tree()
        if other_category_tree is None:
            return
        self.save_category_tree(other_category_tree)

    def replace_dataset(self, dataset_code: DatasetCode, other_storage: "Storage"):
        """Replace the given dataset of this Storage by the one in other_storage.

        This is a reference implementation that can be overloaded by concrete
        sub-classes.
        """
        self.delete_dataset(dataset_code, missing_ok=True)

        other_dataset_metadata = other_storage.load_dataset_metadata(dataset_code)
        other_series_iter = other_storage.iter_dataset_series(dataset_code, include_observations=True)

        # Do the save
        self.save_dataset_metadata(other_dataset_metadata)
        self.save_dataset_series(dataset_code, other_series_iter)

    def replace_provider_metadata(
        self,
        other_storage: "Storage",
    ):
        """Replace provider metadata of this Storage instance with the one in other storage."""
        try:
            other_provider_metadata = other_storage.load_provider_metadata()
        except ProviderMetadataNotFound:
            return

        self.save_provider_metadata(other_provider_metadata)

    @abc.abstractmethod
    def save_category_tree(self, category_tree: CategoryTree):
        """Save a category tree to this Storage instance.

        If any error raise CategoryTreeSaveError.
        """
        pass

    @abc.abstractmethod
    def save_dataset_metadata(self, dataset_metadata: DatasetMetadata):
        """Save metadata about the dataset to this Storage instance.

        If any error raise DatasetMetadataSaveError.
        """
        pass

    @abc.abstractmethod
    def save_dataset_series(
        self,
        dataset_code: DatasetCode,
        series: Union[Series, Iterable[Series]],
        *,
        mode: SaveMode = "create_or_replace",
    ):
        """Save series to a dataset of this Storage instance.

        If any error raise SeriesSaveError.

        Mode can be:
        - "append": append the series to the dataset, but if one already exists, it may be duplicated depending on
          the chosen Storage adapter
        - "create_or_replace" (default): keep existing series and for each series, create it if it does not exist,
          or replace the existing one by the new one (matching is done on series code)
        - "replace_all": replace all the existing series by the new ones
        """
        pass

    @abc.abstractmethod
    def save_provider_metadata(self, provider_metadata: ProviderMetadata):
        """Save metadata about the dataset to this Storage instance.

        If any error raise ProviderMetadataSaveError.
        """
        pass

    @abc.abstractmethod
    def save_releases_metadata(self, releases_metadata: ReleasesMetadata):
        """Save a releases metadata to this Storage instance.

        If any error raise ReleasesMetadataSaveError.
        """
        pass

    def update(
        self,
        other_storage: "Storage",
        *,
        category_tree_update_strategy: UpdateStrategy = "merge",
        dataset_update_strategy: UpdateStrategy = "replace",
    ):
        """Update this Storage instance with data from other storage.

        Update provider metadata, category tree, releases metadata,
        and for all datasets: their metadata and series with metadata and observations.
        """
        if category_tree_update_strategy not in update_strategies:
            raise ValueError(category_tree_update_strategy)
        if dataset_update_strategy not in update_strategies:
            raise ValueError(dataset_update_strategy)

        self.replace_provider_metadata(other_storage)
        self.update_category_tree(other_storage, update_strategy=category_tree_update_strategy)
        self.update_releases_metadata(other_storage)
        self.update_datasets(other_storage, update_strategy=dataset_update_strategy)

    def update_category_tree(
        self,
        other_storage: "Storage",
        *,
        update_strategy: UpdateStrategy = "merge",
    ):
        """Update category tree of this Storage instance with the one in other storage."""
        if update_strategy not in update_strategies:
            raise ValueError(update_strategy)

        logger.info(
            "Updating category tree of %r with the one of %r using strategy %r",
            self,
            other_storage,
            update_strategy,
        )
        if update_strategy == "replace":
            return self.replace_category_tree(other_storage)
        elif update_strategy == "merge":
            return self.merge_category_tree(other_storage)
        raise UpdateStrategyNotSupported(update_strategy=update_strategy)

    def update_dataset(
        self,
        dataset_code: DatasetCode,
        other_storage: "Storage",
        *,
        update_strategy: UpdateStrategy = "replace",
    ):
        """Update the given dataset of this Storage instance with the same one in other storage.

        The update strategy can be "replace" (default) or "merge".

        With the "replace" strategy, dataset metadata and series are replaced by the
        dataset taken in the other storage.

        With the "merge" strategy, dataset metadata and series are merged with the
        dataset taken in the other storage.
        """
        if update_strategy not in update_strategies:
            raise ValueError(update_strategy)

        logger.info(
            "Updating dataset %r of %r from the one in %r using strategy %r",
            str(dataset_code),
            self,
            other_storage,
            update_strategy,
        )
        if update_strategy == "replace":
            return self.replace_dataset(dataset_code, other_storage)
        elif update_strategy == "merge":
            return self.merge_dataset(dataset_code, other_storage)
        raise UpdateStrategyNotSupported(update_strategy=update_strategy)

    def update_datasets(
        self,
        other_storage: "Storage",
        *,
        update_strategy: UpdateStrategy = "replace",
    ):
        """Update the datasets of this Storage instance with the ones of other storage."""
        if update_strategy not in update_strategies:
            raise ValueError(update_strategy)

        for dataset_code in other_storage.iter_dataset_codes(on_error="log"):
            self.update_dataset(dataset_code, other_storage, update_strategy=update_strategy)

    def update_releases_metadata(
        self,
        other_storage: "Storage",
        *,
        update_strategy: UpdateStrategy = "merge",
    ):
        """Update releases metadata of this Storage instance with the one in other storage."""
        if update_strategy not in update_strategies:
            raise ValueError(update_strategy)

        logger.info(
            "Updating releases metadata of %r with the one of %r using strategy %r",
            self,
            other_storage,
            update_strategy,
        )
        if update_strategy == "merge":
            return self.merge_releases_metadata(other_storage)
        raise UpdateStrategyNotSupported(update_strategy=update_strategy)
