"""Update a storage dir with data from another storage dir."""

import logging
from enum import Enum
from pathlib import Path

import daiquiri
import typer

from dbnomics_data_model.storage.adapters.filesystem import FileSystemStorage

app = typer.Typer()
logger = logging.getLogger(__name__)


class UpdateStrategy(Enum):
    merge = "merge"
    replace = "replace"


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    src_storage_dir: Path,
    dest_storage_dir: Path,
    category_tree_update_strategy: UpdateStrategy = typer.Option(
        UpdateStrategy.merge.value, envvar="CATEGORY_TREE_UPDATE_STRATEGY"
    ),
    dataset_update_strategy: UpdateStrategy = typer.Option(
        UpdateStrategy.replace.value, envvar="DATASET_UPDATE_STRATEGY"
    ),
    debug: bool = typer.Option(False, "--debug", help="display debug logging messages"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="display info logging messages"),
):
    """Update a storage directory with data from another storage directory."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)]
    )

    dest_storage = FileSystemStorage(dest_storage_dir)
    src_storage = FileSystemStorage(src_storage_dir)
    dest_storage.update(
        src_storage,
        category_tree_update_strategy=category_tree_update_strategy.value,
        dataset_update_strategy=dataset_update_strategy.value,
    )


if __name__ == "__main__":
    app()
