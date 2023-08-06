"""TSV utils."""


import csv
import math
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, Iterator, Literal, Set, Union

from toolz import pipe

from dbnomics_data_model.model.common import AttributeCode
from dbnomics_data_model.model.series import Observation, ObservationValue

__all__ = ["NOT_AVAILABLE", "TsvError", "InvalidTsvObservations", "InvalidTsvObservationValue", "save_tsv_file"]

NOT_AVAILABLE = "NA"


def iter_tsv_parsed_rows(raw_rows):  # noqa: D103
    for index, row in enumerate(raw_rows):
        if index > 0 and len(row) > 1:
            row = row[:]  # Do a shallow copy of row
            row[1] = value_to_float(row[1])
        yield row


def iter_tsv_rows(tsv_io):
    r"""Yield rows from a TSV as `StringIO`.

    Each row is a `list` like `[period, value, attribute1, attribute2, ...]`.
    The first row is the header. Attributes are optional.

    Examples:
    >>> from io import StringIO
    >>> def test(s): return list(iter_tsv_rows(StringIO(s)))
    >>> test("")
    []
    >>> test("     ")
    [['     ']]
    >>> test("period\tvalue")
    [['period', 'value']]
    >>> test("period\tvalue\n")
    [['period', 'value']]
    >>> test("period\tvalue\n2018\t0.2")
    [['period', 'value'], ['2018', '0.2']]
    >>> test("period\tvalue\n\n2018\t0.2")
    [['period', 'value'], ['2018', '0.2']]
    >>> test("period\tvalue\tattribute1\n2018\t0.2\tZ\n")
    [['period', 'value', 'attribute1'], ['2018', '0.2', 'Z']]
    >>> test("period\tvalue\tstatus\n\n2017\t0.1\t\n2018\t0.2\tE")
    [['period', 'value', 'status'], ['2017', '0.1', ''], ['2018', '0.2', 'E']]
    >>> test("period\tvalue\n2018\tNaN")
    [['period', 'value'], ['2018', 'NaN']]
    """
    for line in tsv_io:
        line = line.strip("\n")
        if not line:
            continue
        cells = line.split("\t")
        yield cells


class TsvError(ValueError):
    """Error with TSV data."""


class InvalidTsvObservations(TsvError):
    """Invalid observations in TSV data."""


class InvalidTsvObservationValue(TsvError):
    """Invalid observation value in TSV data."""


def iter_observations(observations_text: str) -> Iterator[Observation]:
    """Yield Observation model entities from TSV."""
    with StringIO(observations_text) as fp:
        rows_iter = pipe(fp, iter_tsv_rows, iter_tsv_parsed_rows)
        try:
            header = next(rows_iter)
        except StopIteration:
            return
        if len(header) < 2 or header[0] != "PERIOD" or header[1] != "VALUE":
            raise InvalidTsvObservations(f"Invalid header: {header}")
        for row in rows_iter:
            attributes = {code: value for code, value in zip(header[2:], row[2:]) if value}
            yield Observation(attributes=attributes, period=row[0], value=row[1])


def observation_to_tsv_row(observation: Observation) -> Dict[str, str]:
    """Transform an Observation instance to a dict representing the corresponding TSV row."""
    return {
        **observation.attributes,
        # Define PERIOD and VALUE after attributes to avoid an attribute
        # named PERIOD or VALUE to overwrite the period or the value.
        "PERIOD": observation.period,
        "VALUE": observation_value_to_str(observation.value),
    }


def observation_value_to_str(observation_value: ObservationValue) -> str:
    """Transform an observation value to a string usable in a TSV file."""
    if isinstance(observation_value, str):
        if observation_value == NOT_AVAILABLE:
            return NOT_AVAILABLE
        else:
            raise InvalidTsvObservationValue(observation_value)
    observation_value_str = str(observation_value)
    if observation_value_str.endswith(".0"):
        observation_value_str = observation_value_str[:-2]
    return observation_value_str


def save_tsv_file(
    tsv_path: Path,
    observations: Iterable[Observation],
):
    """Save observations to a TSV file."""
    # Observations will be iterated twice, so ensure it's a list
    observations = list(observations)

    # Get all observation attributes
    attribute_codes: Set[AttributeCode] = set()
    for observation in observations:
        if observation.attributes:
            attribute_codes |= observation.attributes.keys()

    with tsv_path.open("wt", newline="") as fp:
        fieldnames = ["PERIOD", "VALUE"] + sorted(attribute_codes)
        writer = csv.DictWriter(fp, fieldnames=fieldnames, delimiter="\t", quotechar='"')
        writer.writeheader()
        for observation in observations:
            tsv_row = observation_to_tsv_row(observation)
            writer.writerow(tsv_row)


def value_to_float(value) -> Union[float, str, Literal["NA"]]:
    """Try to convert a value to a `float`.

    Otherwise return "NA" if empty, or else original value.

    >>> value_to_float(None)
    'NA'
    >>> value_to_float(0.1)
    0.1
    >>> value_to_float("")
    'NA'
    >>> value_to_float(" ")
    'NA'
    >>> value_to_float("0")
    0.0
    >>> value_to_float("0.11")
    0.11
    >>> value_to_float(" -0.11 ")
    -0.11
    >>> value_to_float("NA")
    'NA'
    >>> value_to_float("NaN")
    'NaN'
    >>> value_to_float("ZZZ")
    'ZZZ'
    """
    if value is None:
        return NOT_AVAILABLE
    if isinstance(value, str):
        value = value.strip()
        if not value or value == NOT_AVAILABLE:
            return NOT_AVAILABLE
    try:
        float_value = float(value)
    except ValueError:
        return value
    if math.isfinite(float_value):
        return float_value
    return value
