"""File utils."""

from io import BufferedWriter
from pathlib import Path
from typing import Any, BinaryIO, Iterable, Iterator, Union

import orjson
import simdjson


def iter_child_directories(directory: Path) -> Iterator[Path]:
    """Iterate over child directories of a directory."""
    for child in directory.iterdir():
        if child.is_dir():
            yield child


def iter_lines_with_offsets(fp: BinaryIO) -> Iterator[tuple[bytes, int]]:
    """Iterate over lines of a file, yielding the line and the offset of the first character of the line."""
    offset = fp.tell()
    for line in fp:
        yield (line, offset)
        offset = fp.tell()


def load_json_file(path: Path) -> Any:
    """Return data from the JSON file.

    Raise a FileNotFoundError if file was not found.
    Raise a ValueError if JSON data could not be parsed.
    """
    with path.open("rb") as fd:
        return simdjson.load(fd)  # type:ignore


def parse_json_text(text: bytes) -> Any:
    """Parse a JSON document inside text bytes.

    Raise a ValueError if JSON data could not be parsed.
    """
    try:
        return simdjson.loads(text)  # type:ignore
    except ValueError as exc:
        raise ValueError(f"Could not parse JSON text: {text!r}") from exc


def save_json_file(file_path: Path, data: Any):
    """Save a JSON file to path."""
    data_bytes = serialize_json(data)
    file_path.write_bytes(data_bytes)


def save_jsonl_file(path_or_fp: Union[Path, BinaryIO], items: Iterable[Any], *, mode="wb"):
    """Save items to a JSON Lines file, from a file path or a file object."""

    def _save_to_fp(fp):
        for item in items:
            item_bytes = serialize_json_line(item)
            fp.write(item_bytes)
            fp.write(b"\n")

    if isinstance(path_or_fp, Path):
        with path_or_fp.open(mode) as fp:
            _save_to_fp(fp)
    elif isinstance(path_or_fp, BufferedWriter):
        _save_to_fp(path_or_fp)
    else:
        raise TypeError(path_or_fp)


def serialize_json(data: Any) -> bytes:  # noqa: D103
    return orjson.dumps(data, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)


def serialize_json_line(data: Any) -> bytes:  # noqa: D103
    return orjson.dumps(data, option=orjson.OPT_SORT_KEYS)
