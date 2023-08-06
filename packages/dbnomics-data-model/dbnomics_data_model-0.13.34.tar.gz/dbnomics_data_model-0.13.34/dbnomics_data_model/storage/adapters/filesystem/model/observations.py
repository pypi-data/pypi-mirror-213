"""Functions manipulating time series observations."""

from toolz import mapcat
from toolz.curried import get

from dbnomics_data_model.model.periods import detect_frequency, detect_period_format
from dbnomics_data_model.storage.adapters.filesystem.tsv_utils import NOT_AVAILABLE, value_to_float


def align_series_list(series_list):
    """Align many series.

    Many series are aligned if they share a common list of periods.

    Alignment is done by doing the union of the periods of all series, sorting them,
    then iterating over series adding NA values when necessary.
    """
    if not series_list:
        return []
    if len(series_list) == 1:
        return series_list

    # Build all_periods: a set containing all dates of all series given in series_list
    all_periods = sorted(set(mapcat(lambda pair: pair[0], series_list)))

    # Build aligned_series_list
    aligned_series_list = []
    for periods, values in series_list:
        value_by_period = dict(zip(periods, values))
        aligned_values = [value_by_period.get(period) or NOT_AVAILABLE for period in all_periods]
        aligned_series_list.append((all_periods, aligned_values))

    return aligned_series_list


def normalize_observations(observations):
    r"""Return a `tuple` like `(frequency, normalized_observations)`.

    - `frequency` is a `str` guessed from values
    - `normalized_observations` is a `list` like `[period, value, attribute1, attribute2, ...]` where:
        - `period` is a `str`, normalized
        - `values` is a `float` or a `str` if conversion to `float` failed
        - `attributeN` is a `str`

    `observations` parameter is a `list` of observations. Observations values can be `str`, `int` or `float`.

    >>> normalize_observations([])
    (None, [])
    >>> normalize_observations([['PERIOD', 'VALUE']])
    (None, [['PERIOD', 'VALUE']])

    # Convert to float:
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010', '1'], ['2011', '2']])
    (<Frequency.ANNUAL: 'annual'>, [['PERIOD', 'VALUE'], ['2010', 1.0], ['2011', 2.0]])
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010', 1], ['2011', 2]])
    (<Frequency.ANNUAL: 'annual'>, [['PERIOD', 'VALUE'], ['2010', 1.0], ['2011', 2.0]])

    # Different number of cells:
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010']])
    (<Frequency.ANNUAL: 'annual'>, [['PERIOD', 'VALUE'], ['2010', 'NA']])

    # Invalid period formats:
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010 Q2', 1], ['2010 Q3', 2]])
    (<Frequency.QUARTERLY: 'quarterly'>, [['PERIOD', 'VALUE'], ['2010-Q2', 1.0], ['2010-Q3', 2.0]])
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010Z2', 1], ['2010Z3', 2]])
    (None, [['PERIOD', 'VALUE'], ['2010Z2', 1.0], ['2010Z3', 2.0]])

    # Invalid value:
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010', 'Z']])
    (<Frequency.ANNUAL: 'annual'>, [['PERIOD', 'VALUE'], ['2010', 'Z']])

    # Observations attributes:
    >>> normalize_observations([['PERIOD', 'VALUE', 'FLAG'], ['2010', 1, ""], ['2011', 2, 'E']])
    (<Frequency.ANNUAL: 'annual'>, [['PERIOD', 'VALUE', 'FLAG'], ['2010', 1.0, ''], ['2011', 2.0, 'E']])
    >>> normalize_observations([['PERIOD', 'VALUE', 'FLAG'], ['2010', 1, None], ['2011', 2, 'E']])
    (<Frequency.ANNUAL: 'annual'>, [['PERIOD', 'VALUE', 'FLAG'], ['2010', 1.0, ''], ['2011', 2.0, 'E']])

    # Period format different than frequency:
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010-01-01', 1], ['2010-04-01', 2]])
    (<Frequency.QUARTERLY: 'quarterly'>, [['PERIOD', 'VALUE'], ['2010-Q1', 1.0], ['2010-Q2', 2.0]])
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010-01-01', 1], ['2010-01-08', 2]])
    (<Frequency.WEEKLY: 'weekly'>, [['PERIOD', 'VALUE'], ['2010-01-01', 1.0], ['2010-01-08', 2.0]])
    >>> normalize_observations([['PERIOD', 'VALUE'], ['2010-01-04', 1], ['2010-01-11', 2]])
    (<Frequency.WEEKLY: 'weekly'>, [['PERIOD', 'VALUE'], ['2010-W01', 1.0], ['2010-W02', 2.0]])
    """
    if not observations:
        return (None, [])

    header = observations[0]
    if len(observations) < 2:
        return (None, observations)

    observation1 = observations[1]
    period1 = observation1[0]
    if len(observations) == 2:
        frequency, normalize_period = detect_period_format(period1)
    else:
        observation2 = observations[2]
        period2 = observation2[0]
        frequency, normalize_period = detect_frequency(period1, period2)

    def normalize_row(row):
        period = normalize_period(row[0]) if normalize_period is not None else row[0]
        value = value_to_float(get(1, row, None))
        attributes = [
            get(index, row, None) or ""
            for index, column_name in enumerate(header[2:], start=2)  # Skip period and value, already processed.
        ]
        return [period, value] + attributes

    rows = observations[1:]
    normalized_rows = list(map(normalize_row, rows))

    return (frequency, [header] + normalized_rows)
