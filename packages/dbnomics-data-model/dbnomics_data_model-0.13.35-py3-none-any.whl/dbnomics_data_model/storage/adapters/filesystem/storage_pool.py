"""File-system concrete implementation of StoragePool abstract class."""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from dbnomics_data_model.storage import StoragePool
from dbnomics_data_model.storage.errors import StoragePoolInitError

from .file_utils import iter_child_directories
from .storage import FileSystemStorage

__all__ = ["FileSystemStoragePool"]


@dataclass
class FileSystemStoragePool(StoragePool):
    """File-system concrete implementation of StoragePool."""

    # Directory containing sub-directories, each being a provider json-data.
    storage_base_dir: Path

    def __post_init__(self):  # noqa: D105
        if not self.storage_base_dir.is_dir():
            raise StoragePoolInitError(f"Could not find storage base directory: {str(self.storage_base_dir)!r}")

    def create_storage_for_provider(self, provider_code: str) -> "FileSystemStorage":
        """Create a FileSystemStorage for the given provider."""
        storage_dir = self.get_provider_storage_dir(provider_code)
        return FileSystemStorage(storage_dir=storage_dir)

    def iter_storages(self) -> Iterator[FileSystemStorage]:
        """Iterate Storage instances found in this pool."""
        for child_dir in iter_child_directories(self.storage_base_dir):
            yield FileSystemStorage(storage_dir=child_dir)

    def get_provider_storage_dir(self, provider_code: str) -> Path:
        return self.storage_base_dir / f"{provider_code.lower()}-json-data"
