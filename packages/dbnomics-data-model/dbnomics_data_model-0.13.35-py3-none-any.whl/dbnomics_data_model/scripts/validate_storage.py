#! /usr/bin/env python3

"""Validate data of a storage directory."""

import logging
from itertools import chain
from pathlib import Path
from textwrap import indent
from typing import Final, Iterator, List, Optional

import daiquiri
import typer
import yaml
from toolz import take

from dbnomics_data_model.errors import DBnomicsDataModelError
from dbnomics_data_model.model.common import DatasetCode
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage
from dbnomics_data_model.storage.errors import (
    CategoryTreeLoadError,
    DatasetMetadataLoadError,
    ProviderMetadataLoadError,
    ReleasesMetadataLoadError,
    StorageInitError,
)
from dbnomics_data_model.validation import ValidationSettings

app = typer.Typer()
logger = logging.getLogger(__name__)

VALIDATION_YML: Final = "validation.yml"


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    storage_dir: Path,
    datasets: List[DatasetCode] = typer.Option([], envvar="DATASETS", help="Validate only those datasets"),
    debug: bool = typer.Option(False, "--debug", help="Display debug logging messages"),
    ignored_errors_log: Optional[Path] = typer.Option(
        None, envvar="IGNORED_ERRORS_LOG", help="Output log file for ignored errors"
    ),
    series_limit: Optional[int] = typer.Option(
        None,
        envvar="SERIES_LIMIT",
        help="Maximum number of series to validate per dataset. If not set, validate all series.",
    ),
    validation_yml: Optional[Path] = typer.Option(
        None, envvar="VALIDATION_YML", help=f"Path to the {VALIDATION_YML} settings file"
    ),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Display info logging messages"),
) -> None:
    """Validate data of a storage directory."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)]
    )

    if series_limit is not None and series_limit <= 0:
        logger.error("series limit must be strictly positive, got %r", series_limit)
        raise typer.Abort()

    if series_limit is not None:
        logger.debug("Validating a maximum of %r series per dataset.", series_limit)

    validation_settings = None
    if validation_yml is not None:
        validation_yml_data = yaml.safe_load(validation_yml.read_text())
        validation_settings = ValidationSettings.parse_obj(validation_yml_data)

    ignored_errors_logger = logger.getChild("ignored_errors")
    if ignored_errors_log is not None:
        file_handler = logging.FileHandler(ignored_errors_log)
        file_handler.setFormatter(daiquiri.formatter.TEXT_FORMATTER)
        ignored_errors_logger.addHandler(file_handler)

    logger.debug("Initializing storage from %r...", str(storage_dir))
    try:
        storage = FileSystemStorage(storage_dir)
    except StorageInitError:
        logger.exception("Could not initialize storage from %r", str(storage_dir))
        raise typer.Abort()

    exit_status_code = 0
    errors_iter = iter_storage_errors(storage, datasets=datasets, series_limit=series_limit)

    ignored_errors = []

    for error in errors_iter:
        if validation_settings is not None and validation_settings.is_error_ignored(error):
            ignored_errors.append(error)
        else:
            exit_status_code = 1
            typer.echo(format_error_chain(error))

    if ignored_errors:
        ignored_errors_logger.info("%d errors were ignored due to validation settings:", len(ignored_errors))
        for error in ignored_errors:
            ignored_errors_logger.info(format_error_chain(error))

    raise typer.Exit(code=exit_status_code)


def format_error_chain(error: DBnomicsDataModelError) -> str:
    """Format the error chain with all causes as a tree."""
    depth = 0
    text = repr(error)
    current_error: BaseException = error

    while True:
        cause = current_error.__cause__
        if cause is None:
            break
        current_error = cause
        depth += 1
        text += "\n" + indent(repr(current_error), " " * 2 * depth)

    return text


def iter_category_tree_errors(storage: Storage) -> Iterator[DBnomicsDataModelError]:
    """Validate category tree."""
    logger.debug("Validating category tree...")

    try:
        storage.load_category_tree()
    except CategoryTreeLoadError as exc:
        yield exc
        return

    # Cross-entity checks

    yield from storage.check_dataset_references_of_category_tree(on_error="yield")


def iter_dataset_errors(
    storage: Storage,
    *,
    dataset_codes: List[DatasetCode],
    series_limit: Optional[int] = None,
) -> Iterator[DBnomicsDataModelError]:
    """Validata datasets of Storage."""
    dataset_count = storage.get_dataset_count()
    for dataset_index, dataset_code in enumerate(sorted(storage.iter_dataset_codes(on_error="log")), start=1):
        if dataset_codes and dataset_code not in dataset_codes:
            continue

        logger.debug("Validating dataset %r (%d/%d)...", dataset_code, dataset_index, dataset_count)

        yield from iter_dataset_metadata_errors(storage, dataset_code)
        yield from iter_series_errors(storage, dataset_code, series_limit=series_limit)


def iter_dataset_metadata_errors(storage: Storage, dataset_code: DatasetCode) -> Iterator[DBnomicsDataModelError]:
    """Validate dataset metadata."""
    logger.debug("Validating metadata of dataset %r...", dataset_code)

    try:
        storage.load_dataset_metadata(dataset_code)
    except DatasetMetadataLoadError as exc:
        yield exc


def iter_provider_metadata_errors(storage: Storage) -> Iterator[DBnomicsDataModelError]:
    """Validate provider metadata."""
    logger.debug("Validating provider metadata...")

    try:
        storage.load_provider_metadata()
    except ProviderMetadataLoadError as exc:
        yield exc


def iter_releases_metadata_errors(storage: Storage):
    """Validate releases metadata."""
    logger.debug("Validating releases metadata...")

    try:
        storage.load_releases_metadata()
    except ReleasesMetadataLoadError as exc:
        yield exc
        return

    # Cross-entity checks

    yield from storage.check_dataset_references_of_releases_metadata()


def iter_storage_errors(
    storage: Storage,
    *,
    datasets: List[DatasetCode],
    series_limit: Optional[int] = None,
) -> Iterator[DBnomicsDataModelError]:
    """Validate a Storage instance."""
    yield from chain(
        iter_provider_metadata_errors(storage),
        iter_category_tree_errors(storage),
        iter_releases_metadata_errors(storage),
        iter_dataset_errors(storage, dataset_codes=datasets, series_limit=series_limit),
    )


def iter_series_errors(
    storage: Storage,
    dataset_code: DatasetCode,
    *,
    series_limit: Optional[int] = None,
) -> Iterator[DBnomicsDataModelError]:
    """Validate series of a dataset, metadata and observations."""
    logger.debug("Validating series of dataset %r...", dataset_code)

    series_iter = storage.iter_dataset_series(dataset_code, on_error="yield", include_observations=True)

    if series_limit is not None:
        series_iter = take(series_limit, series_iter)

    yield from storage.check_dataset_series(dataset_code, series_iter)


if __name__ == "__main__":
    app()
