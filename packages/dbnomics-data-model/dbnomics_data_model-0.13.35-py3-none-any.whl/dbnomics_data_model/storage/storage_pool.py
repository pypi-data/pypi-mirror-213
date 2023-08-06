"""StoragePool abstract class."""

import abc
import logging
from typing import Dict, Iterable, Iterator, List, Tuple

from dbnomics_data_model.model.common import DatasetCode, ProviderCode, SeriesCode

from .errors import StorageInitError, StorageTypeNotSupported
from .storage import Storage

__all__ = ["StoragePool", "series_ids_to_tree"]

logger = logging.getLogger(__name__)

SeriesId = Tuple[ProviderCode, DatasetCode, SeriesCode]


class StoragePool(abc.ABC):
    """Abstract storage pool.

    A StoragePool loads or creates Storage instances for specific providers.
    """

    @classmethod
    def create(cls, storage_type: str, **storage_pool_kwargs) -> "StoragePool":
        """Create a concrete StoragePool implementation given storage_type.

        storage_pool_kwargs are passed to the concrete StoragePool implementation.
        """
        if storage_type == "filesystem":
            from .adapters.filesystem import FileSystemStoragePool

            return FileSystemStoragePool(**storage_pool_kwargs)

        raise StorageTypeNotSupported(storage_type=storage_type)

    @abc.abstractmethod
    def create_storage_for_provider(self, provider_code: str) -> "Storage":
        """Create a Storage for the given provider.

        A concrete implementation is returned according to the storage type
        given to the create method.
        """
        pass

    def iter_series_by_storage(
        self, series_ids: List[SeriesId], *, ignore_errors: bool = False
    ) -> Iterator[Tuple[ProviderCode, Dict[DatasetCode, List[SeriesCode]], "Storage"]]:
        """Iterate over many series from different providers and datasets.

        This allows optimal series iteration across different storages.
        """
        series_ids_tree = series_ids_to_tree(series_ids)
        for provider_code, series_codes_by_dataset_code in series_ids_tree.items():
            try:
                storage = self.create_storage_for_provider(provider_code)
            except StorageInitError:
                if ignore_errors:
                    logger.exception("Could not create storage for provider %r", provider_code)
                    continue
                else:
                    raise
            yield (provider_code, series_codes_by_dataset_code, storage)

    @abc.abstractmethod
    def iter_storages(self) -> Iterator[Storage]:
        """Iterate Storage instances found in this pool."""
        pass


def series_ids_to_tree(
    series_ids: Iterable[SeriesId],
) -> Dict[ProviderCode, Dict[DatasetCode, List[SeriesCode]]]:
    """Group series IDs by provider and dataset."""
    tree: Dict[ProviderCode, Dict[DatasetCode, List[SeriesCode]]] = {}
    for provider_code, dataset_code, series_code in series_ids:
        tree.setdefault(provider_code, {}).setdefault(dataset_code, []).append(series_code)
    return tree
