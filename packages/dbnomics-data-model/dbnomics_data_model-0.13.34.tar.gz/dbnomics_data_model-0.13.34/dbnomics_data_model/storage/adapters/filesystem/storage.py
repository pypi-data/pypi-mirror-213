"""File-system concrete implementation of Storage abstract class."""

import logging
import shutil
import typing
from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    overload,
)

import dirsync
from pydantic import ValidationError

from dbnomics_data_model.errors import DBnomicsDataModelError
from dbnomics_data_model.model.category_tree import CategoryTree
from dbnomics_data_model.model.common import DatasetCode, SeriesCode
from dbnomics_data_model.model.dataset_metadata import DatasetMetadata
from dbnomics_data_model.model.provider_metadata import ProviderMetadata
from dbnomics_data_model.model.releases_metadata import ReleasesMetadata
from dbnomics_data_model.model.series import Observation, Series
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.errors import (
    CategoryTreeLoadError,
    CategoryTreeSaveError,
    DatasetDeleteError,
    DatasetMetadataLoadError,
    DatasetMetadataNotFound,
    DatasetMetadataSaveError,
    DatasetNotFoundError,
    ObservationsLoadError,
    OnError,
    ProviderMetadataLoadError,
    ProviderMetadataNotFound,
    ProviderMetadataSaveError,
    ReleasesMetadataLoadError,
    ReleasesMetadataSaveError,
    SeriesDeleteError,
    SeriesLoadError,
    SeriesSaveError,
    StorageDeleteError,
    StorageError,
    StorageInitError,
    process_error,
)
from dbnomics_data_model.storage.storage import SaveMode, save_modes

from .file_utils import iter_lines_with_offsets, load_json_file, parse_json_text, save_json_file, save_jsonl_file
from .model import (
    BaseDatasetJson,
    CategoryTreeJson,
    JsonLinesDatasetJson,
    JsonLinesSeriesItem,
    TsvDatasetJson,
    TsvSeriesJson,
)
from .tsv_utils import InvalidTsvObservations, TsvError, iter_observations, save_tsv_file

__all__ = ["FileSystemStorage", "SeriesJsonLinesOffset", "StorageVariant"]

DATASET_JSON = "dataset.json"
CATEGORY_TREE_JSON = "category_tree.json"
PROVIDER_JSON = "provider.json"
RELEASES_JSON = "releases.json"
SERIES_JSONL = "series.jsonl"

logger = logging.getLogger(__name__)

GetSeriesOffsets = Callable[[Iterable[SeriesCode]], Dict[SeriesCode, int]]
SeriesJsonLinesOffset = int
StorageVariant = Literal["jsonl", "tsv"]
DetectableStorageVariant = Literal["detect", StorageVariant]

DatasetJsonT = TypeVar("DatasetJsonT", bound=BaseDatasetJson)


@dataclass
class FileSystemStorage(Storage):
    """File-system concrete implementation of Storage."""

    storage_dir: Path

    get_series_offsets: Optional[GetSeriesOffsets] = None

    storage_variant: DetectableStorageVariant = "detect"
    # default_storage_variant is used if storage_variant == "detect", and detection could not be done.
    # For example, when a dataset is empty.
    default_storage_variant: StorageVariant = "jsonl"

    warn_when_scanning_jsonl_series: bool = False

    def __enter__(self) -> "FileSystemStorage":
        """Initialize file objects cache that enables keeping many series.jsonl files open."""
        self._series_jsonl_file_objects: Dict[DatasetCode, BinaryIO] = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close all cached file objects."""
        for fp in self._series_jsonl_file_objects.values():
            fp.close()

    def __post_init__(self):
        """Validate dataclass attributes."""
        if not self.storage_dir.is_dir():
            raise StorageInitError(f"Could not find storage directory: {str(self.storage_dir)!r}")

    def delete(self):
        """Delete all data of the provider corresponding to this Storage instance."""
        try:
            shutil.rmtree(self.storage_dir)
        except Exception as exc:
            raise StorageDeleteError() from exc

    def delete_dataset(self, dataset_code: DatasetCode, missing_ok: bool = False):
        """Delete a dataset and its series in this Storage instance if found."""
        dataset_dir = self.get_dataset_dir(dataset_code)
        if not dataset_dir.is_dir():
            if not missing_ok:
                raise DatasetNotFoundError(dataset_code)
            return
        try:
            shutil.rmtree(dataset_dir)
        except Exception as exc:
            raise DatasetDeleteError(dataset_code) from exc

    def delete_dataset_series(self, dataset_code: DatasetCode):
        storage_variant = self.get_storage_variant(dataset_code)
        if storage_variant == "jsonl":
            self._delete_dataset_series_jsonl_variant(dataset_code)
        elif storage_variant == "tsv":
            self._delete_dataset_series_tsv_variant(dataset_code)
        else:
            raise ValueError(storage_variant)

    def detect_storage_variant(self, dataset_code: DatasetCode) -> Optional[StorageVariant]:
        """Detect the storage variant of a dataset.

        Return None if detection could not be done.
        This can happen when a dataset is empty, for example.
        """
        is_jsonl = self._get_series_jsonl_path(dataset_code).is_file()
        if is_jsonl:
            # We're sure this dataset uses the JSON Lines variant.
            return "jsonl"

        dataset_dir = self.get_dataset_dir(dataset_code)
        is_tsv = any(dataset_dir.glob("*.tsv"))
        if is_tsv:
            # We're sure this dataset uses the TSV variant.
            return "tsv"

        return None

    def has_dataset(self, dataset_code: DatasetCode) -> bool:
        """Return True if dataset exists in this Storage instance."""
        return self.get_dataset_dir(dataset_code).is_dir()

    def get_category_tree_json_path(self) -> Path:
        return self.storage_dir / CATEGORY_TREE_JSON

    def get_dataset_dir(self, dataset_code: DatasetCode) -> Path:
        return self.storage_dir / dataset_code

    def get_dataset_json_path(self, dataset_code: DatasetCode) -> Path:
        return self.get_dataset_dir(dataset_code) / DATASET_JSON

    def get_provider_json_path(self) -> Path:
        return self.storage_dir / PROVIDER_JSON

    def get_releases_json_path(self) -> Path:
        return self.storage_dir / RELEASES_JSON

    def get_storage_variant(self, dataset_code: DatasetCode) -> StorageVariant:
        """Get the storage variant of a dataset.

        If the storage variant of the class instance is "detect", first detect the storage variant of the dataset.
        If detection could not be done, return the default storage variant of the FileSystemStorage instance.

        Otherwise, return the storage variant of the class instance.
        """
        if self.storage_variant == "detect":
            detected_storage_variant = self.detect_storage_variant(dataset_code)
            storage_variant = (
                self.default_storage_variant if detected_storage_variant is None else detected_storage_variant
            )
        else:
            storage_variant = self.storage_variant
        return storage_variant

    @overload
    def iter_dataset_codes(  # noqa: D102
        self,
        *,
        on_error: Literal["log", "raise"] = "raise",
    ) -> Iterator[DatasetCode]:
        pass

    @overload
    def iter_dataset_codes(  # noqa: D102
        self,
        *,
        on_error: Literal["yield"],
    ) -> Iterator[Union[DatasetCode, StorageError]]:
        pass

    def iter_dataset_codes(
        self,
        *,
        on_error: OnError = "raise",
    ) -> Union[Iterator[DatasetCode], Iterator[Union[DatasetCode, StorageError]]]:
        """Yield the code of each dataset in this Storage instance.

        Raise StorageError if it fails to load the dataset codes.
        """
        for child in self.storage_dir.iterdir():
            if child.is_dir() and not child.name.startswith("."):
                if not (child / DATASET_JSON).is_file():
                    yield from process_error(
                        StorageError(f"Directory {str(child)!r} does not contain a {DATASET_JSON!r} file"),
                        logger=logger,
                        on_error=on_error,
                    )
                    continue

                yield child.name

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

    def iter_dataset_series(
        self,
        dataset_code: DatasetCode,
        *,
        include_observations: bool = True,
        on_error: OnError = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Union[Iterator[Series], Iterator[Union[Series, DBnomicsDataModelError]]]:
        """Yield series of a dataset.

        Observations are included by default and can be disabled.

        Series can be stored in the file-system with 2 variants:
        - TSV: series metadata is in `dataset.json` under the `series` array property,
          and observations are in TSV files
        - JSON lines: series metadata and observations are in `series.jsonl`
        """
        storage_variant = self.get_storage_variant(dataset_code)

        dataset_json = self.load_dataset_json(dataset_code, storage_variant=storage_variant)

        if storage_variant == "jsonl":
            assert isinstance(dataset_json, JsonLinesDatasetJson)
            for data_or_exc in self.iter_series_jsonl_variant(
                dataset_code,
                dataset_json=dataset_json,
                include_observations=include_observations,
                on_error=on_error,
                series_codes=series_codes,
            ):
                if isinstance(data_or_exc, DBnomicsDataModelError):
                    yield data_or_exc
                    continue
                series, _ = data_or_exc
                yield series
        elif storage_variant == "tsv":
            assert isinstance(dataset_json, TsvDatasetJson)
            yield from self._iter_series_tsv_variant(
                dataset_code,
                dataset_json=dataset_json,
                include_observations=include_observations,
                on_error=on_error,
                series_codes=series_codes,
            )
        else:
            raise ValueError(storage_variant)

    def load_category_tree(self) -> Optional[CategoryTree]:
        """Return the category tree defined in this Storage instance.

        If not found return None because category tree is optional.
        """
        category_tree_json = self.load_category_tree_json()
        if category_tree_json is None:
            return None
        return category_tree_json.to_domain_model()

    def load_category_tree_json(self) -> Optional[CategoryTreeJson]:
        """Return the model representing the category tree JSON file.

        If not found return None because category tree is optional.
        """
        category_tree_json_path = self.get_category_tree_json_path()

        try:
            category_tree_json = load_json_file(category_tree_json_path)
        except FileNotFoundError:
            return None
        except ValueError as exc:
            raise CategoryTreeLoadError(f"Could not parse JSON file: {str(category_tree_json_path)}") from exc

        try:
            return CategoryTreeJson.parse_obj(category_tree_json)
        except ValidationError as exc:
            raise CategoryTreeLoadError(
                f"Could not build model instance from JSON file: {str(category_tree_json_path)}"
            ) from exc

    @overload
    def load_dataset_json(
        self, dataset_code: DatasetCode, *, storage_variant: Literal["detect"] = "detect"
    ) -> BaseDatasetJson:  # noqa: D102
        ...

    @overload
    def load_dataset_json(
        self, dataset_code: DatasetCode, *, storage_variant: Literal["jsonl"]
    ) -> JsonLinesDatasetJson:  # noqa: D102
        ...

    @overload
    def load_dataset_json(
        self, dataset_code: DatasetCode, *, storage_variant: Literal["tsv"]
    ) -> TsvDatasetJson:  # noqa: D102
        ...

    def load_dataset_json(
        self, dataset_code: DatasetCode, *, storage_variant: DetectableStorageVariant = "detect"
    ) -> BaseDatasetJson:
        if storage_variant == "detect":
            storage_variant = self.get_storage_variant(dataset_code)
        parser_class = self._get_dataset_json_parser_class(storage_variant)
        dataset_json = self.parse_dataset_json(dataset_code, parser_class=parser_class)
        self._check_code_in_dataset_json_matches_directory_name(
            dataset_json_code=dataset_json.code, directory_name=dataset_code
        )
        return dataset_json

    def load_dataset_json_data(self, dataset_code: DatasetCode) -> Any:
        dataset_json_path = self.get_dataset_json_path(dataset_code)

        try:
            return load_json_file(dataset_json_path)
        except FileNotFoundError as exc:
            raise DatasetMetadataNotFound(f"File not found: {str(dataset_json_path)}") from exc
        except ValueError as exc:
            raise DatasetMetadataLoadError(f"Could not parse JSON file: {str(dataset_json_path)}") from exc

    def load_dataset_metadata(self, dataset_code: DatasetCode) -> DatasetMetadata:
        """Return metadata about the dataset in this Storage instance.

        Raise:
        - DatasetMetadataNotFound if not found
        - DatasetMetadataLoadError if JSON file could not be parsed or model instance could not be constructed
        """
        dataset_json = self.load_dataset_json(dataset_code)
        return dataset_json.to_dataset_metadata()

    def load_provider_json_data(self) -> Any:
        provider_json_path = self.get_provider_json_path()

        try:
            return load_json_file(provider_json_path)
        except FileNotFoundError as exc:
            raise ProviderMetadataNotFound(f"File not found: {str(provider_json_path)}") from exc
        except ValueError as exc:
            raise ProviderMetadataLoadError(f"Could not parse JSON file: {str(provider_json_path)}") from exc

    def load_provider_metadata(self) -> ProviderMetadata:
        """Return metadata about the provider in this Storage instance.

        Raise:
        - ProviderMetadataNotFound if not found
        - ProviderMetadataLoadError if JSON file could not be parsed or model instance could not be constructed
        """
        provider_json_path = self.get_provider_json_path()
        provider_json_data = self.load_provider_json_data()

        try:
            return ProviderMetadata.parse_obj(provider_json_data)
        except ValidationError as exc:
            raise ProviderMetadataLoadError(
                f"Could not build model instance from JSON file: {str(provider_json_path)}"
            ) from exc

    def load_releases_metadata(self) -> Optional[ReleasesMetadata]:
        """Return releases metadata defined in this Storage instance.

        If not found return None because releases are optional.
        """
        releases_json_path = self.get_releases_json_path()

        try:
            releases_json = load_json_file(releases_json_path)
        except FileNotFoundError:
            return None
        except ValueError as exc:
            raise ReleasesMetadataLoadError(f"Could not parse JSON file: {str(releases_json_path)}") from exc

        try:
            return ReleasesMetadata.parse_obj(releases_json)
        except ValidationError as exc:
            raise ReleasesMetadataLoadError(
                f"Could not build model instance from JSON file: {str(releases_json_path)}"
            ) from exc

    def parse_dataset_json(self, dataset_code: DatasetCode, *, parser_class: Type[DatasetJsonT]) -> DatasetJsonT:
        dataset_json_data = self.load_dataset_json_data(dataset_code)
        try:
            return parser_class.parse_obj(dataset_json_data)
        except ValidationError as exc:
            dataset_json_path = self.get_dataset_json_path(dataset_code)
            raise DatasetMetadataLoadError(
                f"Could not build model instance from JSON file: {str(dataset_json_path)}"
            ) from exc

    def replace_dataset(self, dataset_code: DatasetCode, other_storage: Storage):
        """Replace the given dataset of this Storage by the one in other_storage.

        Optimization: the directories are synchronized at the file-system level if the following conditions are met:

        - the `other_storage` instance must also be a `FileSystemStorage`
        - the dataset must use the same storage variant in both storages
        """

        def is_same_variant(other_fs_storage: FileSystemStorage) -> bool:
            other_variant = other_fs_storage.get_storage_variant(dataset_code)
            variant = self.detect_storage_variant(dataset_code)
            if variant is None:
                variant = other_variant
            return variant == other_variant

        if isinstance(other_storage, FileSystemStorage) and is_same_variant(other_storage):
            dataset_dir = self.get_dataset_dir(dataset_code)
            other_dataset_dir = other_storage.get_dataset_dir(dataset_code)
            dirsync.sync(
                action="sync",
                # Compare file contents when syncing directories, do not rely on file modification time.
                # For example, a file from an older revision may have a more recent time because it may have been
                # "git cloned" just now.
                content=True,
                create=True,
                logger=logger.getChild("dirsync"),
                purge=True,
                sourcedir=other_dataset_dir,
                targetdir=dataset_dir,
            )
        else:
            super().replace_dataset(dataset_code, other_storage)

    def save_category_tree(self, category_tree: CategoryTree):
        """Save a category tree to this Storage instance.

        If any error raise CategoryTreeSaveError.
        """
        self.save_category_tree_json(CategoryTreeJson.from_domain_model(category_tree))

    def save_category_tree_json(self, category_tree_json: CategoryTreeJson):
        """Save the category tree to a JSON file."""
        category_tree_json_path = self.get_category_tree_json_path()
        try:
            # Do not use .dict() because category root type is a list.
            save_json_file(category_tree_json_path, category_tree_json.to_json())
        except Exception as exc:
            raise CategoryTreeSaveError(f"Error saving file: {str(category_tree_json_path)}") from exc

    def save_dataset_json(self, dataset_json: BaseDatasetJson) -> None:
        dataset_json_path = self.get_dataset_json_path(dataset_json.code)
        dataset_json_dict = dataset_json.dict()
        try:
            save_json_file(dataset_json_path, dataset_json_dict)
        except Exception as exc:
            raise DatasetMetadataSaveError(f"Error saving file: {str(dataset_json_path)}") from exc

    def save_dataset_metadata(self, dataset_metadata: DatasetMetadata):
        """Save metadata about the dataset to this Storage instance.

        If any error raise DatasetMetadataSaveError.

        With TSV variant, keep the existing series metadata if there are some defined in dataset.json.
        """
        dataset_code = dataset_metadata.code
        dataset_dir = self.get_dataset_dir(dataset_code)
        dataset_dir.mkdir(exist_ok=True)
        dataset_json = self._get_dataset_json_from_dataset_metadata(dataset_metadata)
        self.save_dataset_json(dataset_json)

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
        if mode not in save_modes:
            raise ValueError(mode)

        dataset_dir = self.get_dataset_dir(dataset_code)
        dataset_dir.mkdir(exist_ok=True)

        # Read storage variant before deleting all series.
        storage_variant = self.get_storage_variant(dataset_code)

        if mode == "replace_all":
            self.delete_dataset_series(dataset_code)

        series_iter = [series] if isinstance(series, Series) else series

        if storage_variant == "jsonl":
            self._save_dataset_series_jsonl_variant(dataset_code, series_iter, mode=mode)
        elif storage_variant == "tsv":
            self._save_dataset_series_tsv_variant(dataset_code, series_iter, mode=mode)
        else:
            raise ValueError(storage_variant)

    def save_provider_metadata(self, provider_metadata: ProviderMetadata):
        """Save metadata about the dataset to this Storage instance.

        If any error raise ProviderMetadataSaveError.
        """
        provider_json_path = self.get_provider_json_path()
        try:
            save_json_file(provider_json_path, provider_metadata.dict())
        except Exception as exc:
            raise ProviderMetadataSaveError(f"Error saving file: {str(provider_json_path)}") from exc

    def save_releases_metadata(self, releases_metadata: ReleasesMetadata):
        """Save a releases metadata to this Storage instance.

        If any error raise ReleasesMetadataSaveError.
        """
        releases_json_path = self.get_releases_json_path()
        try:
            save_json_file(releases_json_path, releases_metadata.dict())
        except Exception as exc:
            raise ReleasesMetadataSaveError(f"Error saving file: {str(releases_json_path)}") from exc

    # Private methods

    def _check_code_in_dataset_json_matches_directory_name(
        self, dataset_json_code: DatasetCode, directory_name: DatasetCode
    ) -> None:
        """Check that the code in dataset.json matches the directory name."""
        if dataset_json_code != directory_name:
            raise DatasetMetadataLoadError(
                f"Dataset code {dataset_json_code!r} in {DATASET_JSON} is different from "
                f"the directory name {directory_name!r}"
            )

    def _delete_dataset_series_jsonl_variant(self, dataset_code: DatasetCode):
        series_jsonl_path = self._get_series_jsonl_path(dataset_code)
        series_jsonl_path.unlink(missing_ok=True)

    def _delete_dataset_series_tsv_variant(self, dataset_code: DatasetCode):
        """Delete all dataset series for TSV variant.

        Delete all TSV files, remove "series" property of `dataset.json`.
        """
        # Delete series metadata
        dataset_json_path = self.get_dataset_json_path(dataset_code)
        try:
            dataset_json_data = load_json_file(dataset_json_path)
        except FileNotFoundError:
            pass
        else:
            if "series" in dataset_json_data:
                del dataset_json_data["series"]
                try:
                    save_json_file(dataset_json_path, dataset_json_data)
                except Exception as exc:
                    raise SeriesDeleteError(
                        f"Error saving file {str(dataset_json_path)} for deleting "
                        f"all series of dataset {dataset_code!r}"
                    ) from exc

        # Delete series observations
        dataset_dir = self.get_dataset_dir(dataset_code)
        for tsv_file in dataset_dir.glob("*.tsv"):
            tsv_file.unlink()

    def _get_dataset_json_from_dataset_metadata(
        self, dataset_metadata: DatasetMetadata, *, storage_variant: DetectableStorageVariant = "detect"
    ) -> BaseDatasetJson:
        dataset_code = dataset_metadata.code
        if storage_variant == "detect":
            storage_variant = self.get_storage_variant(dataset_code)

        if storage_variant == "tsv":
            return self._get_dataset_json_from_dataset_metadata_tsv_variant(dataset_metadata)
        if storage_variant == "jsonl":
            return self._get_dataset_json_from_dataset_metadata_jsonl_variant(dataset_metadata)
        raise ValueError(storage_variant)

    def _get_dataset_json_from_dataset_metadata_jsonl_variant(
        self, dataset_metadata: DatasetMetadata
    ) -> JsonLinesDatasetJson:
        return JsonLinesDatasetJson.from_dataset_metadata(dataset_metadata)

    def _get_dataset_json_from_dataset_metadata_tsv_variant(self, dataset_metadata: DatasetMetadata) -> TsvDatasetJson:
        dataset_code = dataset_metadata.code

        tsv_dataset_json = TsvDatasetJson.from_dataset_metadata(dataset_metadata)

        # Keep the existing series metadata if there are some defined in dataset.json.
        series_metadata_from_dataset_json = self._load_series_metadata_tsv_variant(dataset_code)
        if series_metadata_from_dataset_json:
            tsv_dataset_json.series = series_metadata_from_dataset_json

        return tsv_dataset_json

    def _get_dataset_json_parser_class(self, storage_variant: StorageVariant) -> Type[BaseDatasetJson]:
        if storage_variant == "jsonl":
            return JsonLinesDatasetJson
        if storage_variant == "tsv":
            return TsvDatasetJson
        raise ValueError(storage_variant)

    def _get_series_jsonl_file_object(self, dataset_code: DatasetCode) -> BinaryIO:
        fp = self._series_jsonl_file_objects.get(dataset_code)
        if fp is None:
            series_jsonl_path = self._get_series_jsonl_path(dataset_code)
            fp = series_jsonl_path.open("ab")
            self._series_jsonl_file_objects[dataset_code] = fp
        return fp

    def _get_series_jsonl_path(self, dataset_code: DatasetCode) -> Path:
        return self.get_dataset_dir(dataset_code) / SERIES_JSONL

    def _get_tsv_path(self, dataset_code: DatasetCode, series_code: SeriesCode) -> Path:
        return self.get_dataset_dir(dataset_code) / f"{series_code}.tsv"

    @overload
    def iter_series_jsonl_variant(
        self,
        dataset_code: DatasetCode,
        *,
        dataset_json: JsonLinesDatasetJson,
        include_observations: bool = True,
        on_error: Literal["log", "raise"] = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Iterator[tuple[Series, SeriesJsonLinesOffset]]:
        ...

    @overload
    def iter_series_jsonl_variant(
        self,
        dataset_code: DatasetCode,
        *,
        dataset_json: JsonLinesDatasetJson,
        include_observations: bool = True,
        on_error: Literal["yield"],
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Iterator[Union[tuple[Series, SeriesJsonLinesOffset], DBnomicsDataModelError]]:
        ...

    def iter_series_jsonl_variant(
        self,
        dataset_code: DatasetCode,
        *,
        dataset_json: JsonLinesDatasetJson,
        include_observations: bool = True,
        on_error: OnError = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Union[
        Iterator[tuple[Series, SeriesJsonLinesOffset]],
        Iterator[Union[tuple[Series, SeriesJsonLinesOffset], DBnomicsDataModelError]],
    ]:
        series_jsonl_path = self._get_series_jsonl_path(dataset_code)
        if not series_jsonl_path.is_file():
            return

        for series_index, data_or_exc in enumerate(
            self._iter_series_jsonl_data(
                dataset_code, include_observations=include_observations, on_error=on_error, series_codes=series_codes
            )
        ):
            if isinstance(data_or_exc, DBnomicsDataModelError):
                yield data_or_exc
                continue

            series_json_data, offset = data_or_exc

            try:
                series_json = JsonLinesSeriesItem.parse_obj(series_json_data)
            except ValidationError as exc:
                yield from process_error(
                    SeriesLoadError(
                        f"Could not build model instance from item #{series_index!r} "
                        f"of JSON Lines file: {str(series_jsonl_path)}"
                    ),
                    from_exc=exc,
                    logger=logger,
                    on_error=on_error,
                )
                continue

            series = series_json.to_series(dimensions_codes_order=dataset_json.dimensions_codes_order)
            yield series, offset

    @overload
    def _iter_series_jsonl_data(
        self,
        dataset_code: DatasetCode,
        *,
        include_observations: bool = True,
        on_error: Literal["log", "raise"] = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Iterator[tuple[dict, SeriesJsonLinesOffset]]:
        ...

    @overload
    def _iter_series_jsonl_data(
        self,
        dataset_code: DatasetCode,
        *,
        include_observations: bool = True,
        on_error: Literal["yield"],
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Iterator[Union[Iterator[tuple[dict, SeriesJsonLinesOffset]], DBnomicsDataModelError]]:
        ...

    def _iter_series_jsonl_data(
        self,
        dataset_code: DatasetCode,
        *,
        include_observations: bool = True,
        on_error: OnError = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Union[
        Iterator[tuple[dict, SeriesJsonLinesOffset]],
        Iterator[Union[Iterator[tuple[dict, SeriesJsonLinesOffset]], DBnomicsDataModelError]],
    ]:
        """Yield series `dict`s from `series.jsonl`.

        First try to find series by seeking in the JSON lines file using offsets
        previously indexed in Solr.

        Then, if any series remains (meaning Solr is not up to date), find them
        by scanning the JSON lines file.
        """
        series_jsonl_path = self._get_series_jsonl_path(dataset_code)
        remaining_series_codes = None if series_codes is None else set(series_codes)

        if remaining_series_codes is not None and remaining_series_codes and self.get_series_offsets is not None:
            yield from self._iter_series_jsonl_by_seeking(
                series_jsonl_path,
                remaining_series_codes,
                include_observations=include_observations,
                on_error=on_error,
            )

        if remaining_series_codes is None or remaining_series_codes:
            if self.warn_when_scanning_jsonl_series:
                logger.warning(
                    "%s of the dataset %r are about to be loaded by scanning its JSON Lines file, "
                    "this is a performance bottleneck",
                    "All the series" if remaining_series_codes is None else f"{len(remaining_series_codes)} series",
                    dataset_code,
                )
            yield from self._iter_series_jsonl_by_scanning(
                series_jsonl_path,
                remaining_series_codes,
                include_observations=include_observations,
                on_error=on_error,
            )

        if remaining_series_codes is not None and remaining_series_codes:
            yield from process_error(
                SeriesLoadError(
                    f"{len(remaining_series_codes)!r} series codes are still remaining "
                    f"after seeking and scanning: {remaining_series_codes!r}"
                ),
                logger=logger,
                on_error=on_error,
            )

    @overload
    def _iter_series_jsonl_by_scanning(
        self,
        series_jsonl_path: Path,
        remaining_series_codes: Optional[Set[SeriesCode]],
        *,
        include_observations: bool = True,
        on_error: Literal["log", "raise"] = "raise",
    ) -> Iterator[tuple[dict, SeriesJsonLinesOffset]]:
        ...

    @overload
    def _iter_series_jsonl_by_scanning(
        self,
        series_jsonl_path: Path,
        remaining_series_codes: Optional[Set[SeriesCode]],
        *,
        include_observations: bool = True,
        on_error: Literal["yield"],
    ) -> Iterator[Union[Iterator[tuple[dict, SeriesJsonLinesOffset]], DBnomicsDataModelError]]:
        ...

    def _iter_series_jsonl_by_scanning(
        self,
        series_jsonl_path: Path,
        remaining_series_codes: Optional[Set[SeriesCode]],
        *,
        include_observations: bool = True,
        on_error: OnError = "raise",
    ) -> Union[
        Iterator[tuple[dict, SeriesJsonLinesOffset]],
        Iterator[Union[Iterator[tuple[dict, SeriesJsonLinesOffset]], DBnomicsDataModelError]],
    ]:
        with series_jsonl_path.open("rb") as fp:
            for line_index, (line, offset) in enumerate(iter_lines_with_offsets(fp)):
                try:
                    series_json_data = parse_json_text(line)
                except ValueError as exc:
                    yield from process_error(
                        SeriesLoadError(f"Could not parse series in {str(series_jsonl_path)} at line {line_index!r}"),
                        from_exc=exc,
                        logger=logger,
                        on_error=on_error,
                    )
                    continue

                try:
                    series_code = series_json_data["code"]
                except KeyError as exc:
                    yield from process_error(
                        SeriesLoadError(
                            f"Could not find code property in {str(series_jsonl_path)} at line {line_index!r}"
                        ),
                        from_exc=exc,
                        logger=logger,
                        on_error=on_error,
                    )
                    continue

                if remaining_series_codes is not None and series_code not in remaining_series_codes:
                    continue

                if not include_observations and "observations" in series_json_data:
                    del series_json_data["observations"]

                yield series_json_data, offset

                if remaining_series_codes is not None:
                    remaining_series_codes.remove(series_code)
                    if not remaining_series_codes:
                        break

    @overload
    def _iter_series_jsonl_by_seeking(
        self,
        series_jsonl_path: Path,
        remaining_series_codes: Set[SeriesCode],
        *,
        include_observations: bool = True,
        on_error: Literal["log", "raise"] = "raise",
    ) -> Iterator[tuple[dict, SeriesJsonLinesOffset]]:
        ...

    @overload
    def _iter_series_jsonl_by_seeking(
        self,
        series_jsonl_path: Path,
        remaining_series_codes: Set[SeriesCode],
        *,
        include_observations: bool = True,
        on_error: Literal["yield"],
    ) -> Iterator[Union[tuple[dict, SeriesJsonLinesOffset], DBnomicsDataModelError]]:
        ...

    def _iter_series_jsonl_by_seeking(
        self,
        series_jsonl_path: Path,
        remaining_series_codes: Set[SeriesCode],
        *,
        include_observations: bool = True,
        on_error: OnError = "raise",
    ) -> Union[
        Iterator[tuple[dict, SeriesJsonLinesOffset]],
        Iterator[Union[tuple[dict, SeriesJsonLinesOffset], DBnomicsDataModelError]],
    ]:
        assert self.get_series_offsets is not None  # Checked by the caller

        offsets = self.get_series_offsets(remaining_series_codes)

        with series_jsonl_path.open("rb") as fp:
            for series_code, offset in offsets.items():
                fp.seek(offset)

                try:
                    line = next(fp)
                except StopIteration as exc:
                    yield from process_error(
                        SeriesLoadError(f"Could not load text line for series {series_code!r} at offset {offset!r}"),
                        from_exc=exc,
                        logger=logger,
                        on_error=on_error,
                    )
                    continue

                try:
                    series_json_data = parse_json_text(line)
                except ValueError as exc:
                    yield from process_error(
                        SeriesLoadError(f"Could not parse series in {str(series_jsonl_path)} at offset {offset!r}"),
                        from_exc=exc,
                        logger=logger,
                        on_error=on_error,
                    )
                    continue

                try:
                    series_json_code = series_json_data["code"]
                except KeyError as exc:
                    yield from process_error(
                        SeriesLoadError(
                            f"Could not find code property in {str(series_jsonl_path)} at offset {offset!r}"
                        ),
                        from_exc=exc,
                        logger=logger,
                        on_error=on_error,
                    )
                    continue

                if series_code != series_json_code:
                    yield from process_error(
                        SeriesLoadError(
                            f"Found code {series_json_code!r} in {str(series_jsonl_path)}"
                            f" at offset {offset!r} for series {series_code!r}"
                        ),
                        logger=logger,
                        on_error=on_error,
                    )
                    continue

                if not include_observations and "observations" in series_json_data:
                    del series_json_data["observations"]

                yield series_json_data, offset

                if remaining_series_codes is not None:
                    remaining_series_codes.remove(series_code)

    @overload
    def _iter_series_tsv_variant(
        self,
        dataset_code: DatasetCode,
        *,
        dataset_json: TsvDatasetJson,
        include_observations: bool = True,
        on_error: Literal["log", "raise"] = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Iterator[Series]:
        ...

    @overload
    def _iter_series_tsv_variant(
        self,
        dataset_code: DatasetCode,
        *,
        dataset_json: TsvDatasetJson,
        include_observations: bool = True,
        on_error: Literal["yield"],
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Iterator[Union[Series, DBnomicsDataModelError]]:
        ...

    def _iter_series_tsv_variant(
        self,
        dataset_code: DatasetCode,
        *,
        dataset_json: TsvDatasetJson,
        include_observations: bool = True,
        on_error: OnError = "raise",
        series_codes: Optional[Iterable[SeriesCode]] = None,
    ) -> Union[Iterator[Series], Iterator[Union[Series, DBnomicsDataModelError]]]:
        """Yield Series objects from a dataset stored using TSV variant.

        Start by reading series metadata in dataset.json `series` property,
        and for each one read the corresponding TSV file for observations.
        """
        for series_json in dataset_json.series:
            series_code = series_json.code
            if series_codes is not None and series_code not in series_codes:
                continue

            series = series_json.to_series(dimensions_codes_order=dataset_json.dimensions_codes_order)

            if include_observations:
                try:
                    observations = sorted(
                        self._iter_observations_from_tsv(dataset_code, series_code),
                        key=attrgetter("period"),
                    )
                except ObservationsLoadError as exc:
                    yield from process_error(exc, logger=logger, on_error=on_error)
                    continue
                series.observations = observations

            yield series

    def _iter_observations_from_tsv(self, dataset_code: DatasetCode, series_code: SeriesCode) -> Iterator[Observation]:
        observations_tsv_path = self._get_tsv_path(dataset_code, series_code)

        try:
            observations_text = observations_tsv_path.read_text()
        except FileNotFoundError as exc:
            raise ObservationsLoadError(f"File not found: {str(observations_tsv_path)}") from exc

        try:
            yield from iter_observations(observations_text)
        except InvalidTsvObservations as exc:
            raise ObservationsLoadError(f"Invalid observations in TSV file: {str(observations_tsv_path)}") from exc

    def _load_series_metadata_tsv_variant(self, dataset_code: DatasetCode) -> List[TsvSeriesJson]:
        dataset_json_path = self.get_dataset_json_path(dataset_code)
        try:
            current_dataset_json_data = load_json_file(dataset_json_path)
        except FileNotFoundError:
            return []
        return current_dataset_json_data.get("series", [])

    def _save_dataset_series_jsonl_variant(
        self,
        dataset_code: DatasetCode,
        series_iter: Iterable[Series],
        *,
        mode: SaveMode = "create_or_replace",
    ):
        if mode == "create_or_replace" and self.dataset_has_series(dataset_code):
            raise NotImplementedError(
                '"create_or_replace" mode is not supported when using the JSON Lines dataset storage variant'
            )

        series_jsonl_path = self._get_series_jsonl_path(dataset_code)
        series_data_iter = (JsonLinesSeriesItem.from_series(series).dict() for series in series_iter)

        if mode == "append":
            if not hasattr(self, "_series_jsonl_file_objects"):
                raise RuntimeError(f"{self} must be used with from a context manager when using {mode!r} mode")
            fp = self._get_series_jsonl_file_object(dataset_code)
            try:
                save_jsonl_file(fp, series_data_iter)
            except Exception as exc:
                raise SeriesSaveError(f"Error saving file: {str(series_jsonl_path)}") from exc

        elif mode in {"create_or_replace", "replace_all"}:
            # For replace_all mode, deletion of all series has been done in calling function.
            try:
                save_jsonl_file(series_jsonl_path, series_data_iter)
            except Exception as exc:
                raise SeriesSaveError(f"Error saving file: {str(series_jsonl_path)}") from exc

    def _save_dataset_series_tsv_variant(
        self,
        dataset_code: DatasetCode,
        series_iter: Iterable[Series],
        *,
        mode: SaveMode = "create_or_replace",
    ):
        try:
            tsv_dataset_json = typing.cast(TsvDatasetJson, self.load_dataset_json(dataset_code, storage_variant="tsv"))
        except DatasetMetadataNotFound as exc:
            raise SeriesSaveError(
                "Could not save series before saving dataset metadata with TSV storage variant"
            ) from exc

        for series in series_iter:
            # Collect series metadata
            if mode == "create_or_replace":
                tsv_dataset_json.create_or_replace_series_metadata(series.metadata)
            elif mode in {"append", "replace_all"}:
                # For replace_all mode, deletion of all series has been done in calling function.
                tsv_dataset_json.series.append(TsvSeriesJson.from_series_metadata(series.metadata))

            # Save series observations
            series_code = series.metadata.code
            tsv_path = self._get_tsv_path(dataset_code, series_code)
            try:
                save_tsv_file(tsv_path, series.observations)
            except TsvError as exc:
                raise SeriesSaveError(f"Could not save TSV file {str(tsv_path)!r} for series {series_code!r}") from exc

        # Save series metadata via updated dataset.json
        self.save_dataset_json(tsv_dataset_json)
