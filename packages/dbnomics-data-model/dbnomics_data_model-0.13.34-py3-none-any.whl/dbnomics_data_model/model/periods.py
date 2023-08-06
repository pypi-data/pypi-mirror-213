"""Functions manipulating time series periods and frequencies."""

import logging
import math
import re
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional

from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


class Frequency(Enum):  # noqa: D101
    ANNUAL = "annual"
    BI_ANNUAL = "bi-annual"
    BI_MONTHLY = "bi-monthly"
    QUARTERLY = "quarterly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"

    def to_dimension_code(self):  # noqa: D102
        return {
            Frequency.ANNUAL: "A",
            Frequency.BI_ANNUAL: "S",
            Frequency.BI_MONTHLY: "B",
            Frequency.QUARTERLY: "Q",
            Frequency.MONTHLY: "M",
            Frequency.WEEKLY: "W",
            Frequency.DAILY: "D",
        }[self]


day_range_re = "0[1-9]|[1-2][0-9]|3[0-1]"  # 01-31
month_range_re = "0[1-9]|1[0-2]"  # 01-12
# Cf https://docs.python.org/3/library/datetime.html#datetime.date.isocalendar
week_range_re = "0[1-9]|[1-4][0-9]|5[0-3]"  # 01-53


period_format_strict_regex_list = [
    (Frequency.ANNUAL, re.compile(r"^(\d{4})$")),
    (Frequency.BI_ANNUAL, re.compile(r"^(\d{4})-S([1-2])$")),
    (Frequency.BI_MONTHLY, re.compile(r"^(\d{4})-B([1-6])$")),
    (Frequency.QUARTERLY, re.compile(r"^(\d{4})-Q([1-4])$")),
    (
        Frequency.MONTHLY,
        re.compile(r"^(\d{{4}})-({})$".format(month_range_re)),
    ),  # YYYY-[01-12]
    (
        Frequency.WEEKLY,
        re.compile(r"^(\d{{4}})-W({})$".format(week_range_re)),
    ),  # YYYY-W[01-53]
    # YYYY-[01-12]-[01-31]
    (
        Frequency.DAILY,
        re.compile(r"^(\d{{4}})-({})-({})$".format(month_range_re, day_range_re)),
    ),
]


def iter_periods_dates(frequency: Frequency, min_date: date, max_date: Optional[date] = None):
    """Yield dates from `min_date` to `max_date` (if not `None`) by increment of `frequency`."""
    current_date = min_date
    while True:
        yield current_date
        if max_date is not None and current_date >= max_date:
            break
        current_date = next_period_date(current_date, frequency)


def next_period_date(period_date: date, frequency: Frequency):
    """Return next period date, applying an increment to `period_date` of `frequency`.

    >>> next_period_date(date(2000, 1, 1), Frequency.ANNUAL)
    datetime.date(2001, 1, 1)
    >>> next_period_date(date(2000, 1, 1), Frequency.BI_ANNUAL)
    datetime.date(2000, 7, 1)
    >>> next_period_date(date(2000, 1, 1), Frequency.BI_MONTHLY)
    datetime.date(2000, 3, 1)
    >>> next_period_date(date(2000, 1, 1), Frequency.QUARTERLY)
    datetime.date(2000, 4, 1)
    >>> next_period_date(date(2000, 1, 1), Frequency.MONTHLY)
    datetime.date(2000, 2, 1)
    >>> next_period_date(date(2000, 1, 1), Frequency.WEEKLY)
    datetime.date(2000, 1, 8)
    >>> next_period_date(date(2000, 1, 1), Frequency.DAILY)
    datetime.date(2000, 1, 2)
    """
    if frequency == Frequency.ANNUAL:
        return period_date + relativedelta(years=1)
    elif frequency == Frequency.BI_ANNUAL:
        return period_date + relativedelta(months=6)
    elif frequency == Frequency.BI_MONTHLY:
        return period_date + relativedelta(months=2)
    elif frequency == Frequency.QUARTERLY:
        return period_date + relativedelta(months=3)
    elif frequency == Frequency.MONTHLY:
        return period_date + relativedelta(months=1)
    elif frequency == Frequency.WEEKLY:
        return period_date + relativedelta(weeks=1)
    elif frequency == Frequency.DAILY:
        return period_date + timedelta(days=1)
    else:
        raise ValueError(f"Unsupported frequency: {frequency}")


def detect_frequency(period1, period2):
    """Return a tuple like `(frequency, normalize_period)` for the given `period`.

    If periods are already normalized or if `period1` and `period2` are not start days
    of the inferred frequency, `normalize_period` will be `None`.
    Otherwise it will be a function taking a period `str` and returning a normalized period `str`.

    When the format of the periods is "daily", the frequency can be different,
    depending on the interval between the days (e.g. the frequency can be "quarterly" if the interval is 3 months).
    That's the purpose of this function, compared to `detect_period_format` which takes one period only.

    See also: `detect_period_format`, `detect_period_format_strict`

    # From period format corresponding to frequency:
    >>> detect_frequency('2014', '2015')
    (<Frequency.ANNUAL: 'annual'>, None)
    >>> detect_frequency('2014', '2016')
    (<Frequency.ANNUAL: 'annual'>, None)
    >>> detect_frequency('2014-S1', '2014-S2')
    (<Frequency.BI_ANNUAL: 'bi-annual'>, None)
    >>> detect_frequency('2014-S1', '2015-S2')
    (<Frequency.BI_ANNUAL: 'bi-annual'>, None)
    >>> detect_frequency('2014-Q1', '2014-Q2')
    (<Frequency.QUARTERLY: 'quarterly'>, None)
    >>> detect_frequency('2014-Q1', '2014-Q3')
    (<Frequency.QUARTERLY: 'quarterly'>, None)
    >>> detect_frequency('2014-B1', '2014-B2')
    (<Frequency.BI_MONTHLY: 'bi-monthly'>, None)
    >>> detect_frequency('2014-B1', '2014-B3')
    (<Frequency.BI_MONTHLY: 'bi-monthly'>, None)
    >>> detect_frequency('2014-01', '2014-02')
    (<Frequency.MONTHLY: 'monthly'>, None)
    >>> detect_frequency('2014-01', '2014-03')
    (<Frequency.MONTHLY: 'monthly'>, None)
    >>> detect_frequency('2014-W01', '2014-W02')
    (<Frequency.WEEKLY: 'weekly'>, None)
    >>> detect_frequency('2014-W01', '2014-W03')
    (<Frequency.WEEKLY: 'weekly'>, None)
    >>> detect_frequency('2014-01-01', '2014-01-02')
    (<Frequency.DAILY: 'daily'>, None)
    >>> detect_frequency('2014-01-01', '2014-01-03')
    (<Frequency.DAILY: 'daily'>, None)

    # From daily period format:
    >>> detect_frequency('2014-01-01', '2015-01-01')  # doctest: +ELLIPSIS
    (<Frequency.ANNUAL: 'annual'>, ...)
    >>> detect_frequency('2014-01-01', '2014-07-01')  # doctest: +ELLIPSIS
    (<Frequency.BI_ANNUAL: 'bi-annual'>, ...)
    >>> detect_frequency('2014-01-01', '2014-04-01')  # doctest: +ELLIPSIS
    (<Frequency.QUARTERLY: 'quarterly'>, ...)
    >>> detect_frequency('1919-03-31', '1919-06-30')  # doctest: +ELLIPSIS
    (<Frequency.QUARTERLY: 'quarterly'>, ...)
    >>> detect_frequency('2014-01-01', '2014-03-01')  # doctest: +ELLIPSIS
    (<Frequency.BI_MONTHLY: 'bi-monthly'>, ...)
    >>> detect_frequency('2014-01-01', '2014-02-01')  # doctest: +ELLIPSIS
    (<Frequency.MONTHLY: 'monthly'>, ...)
    >>> detect_frequency('2014-01-15', '2014-02-15')  # doctest: +ELLIPSIS
    (<Frequency.MONTHLY: 'monthly'>, ...)
    >>> detect_frequency('2014-01-01', '2014-01-31')  # doctest: +ELLIPSIS
    (<Frequency.DAILY: 'daily'>, ...)
    >>> detect_frequency('2014-01-06', '2014-01-13')  # doctest: +ELLIPSIS
    (<Frequency.WEEKLY: 'weekly'>, ...)
    >>> detect_frequency('2014-01-07', '2014-01-14')  # doctest: +ELLIPSIS
    (<Frequency.WEEKLY: 'weekly'>, ...)
    >>> detect_frequency('2014-01-06', '2014-01-14')  # doctest: +ELLIPSIS
    (<Frequency.DAILY: 'daily'>, ...)
    >>> detect_frequency('2014-01-03', '2014-01-11')  # doctest: +ELLIPSIS
    (<Frequency.DAILY: 'daily'>, ...)

    # Invalid or different period formats:
    >>> detect_frequency('2014', '2015-02')
    (None, None)
    >>> detect_frequency('2014', '2014Z2')
    (None, None)
    >>> detect_frequency('2014Z2', '2014')
    (None, None)
    >>> detect_frequency('2014Z2', '2014Z2')
    (None, None)
    """

    def make_normalize_period(frequency: Frequency):
        def normalize_period(period: str):
            period_date = datetime.fromisoformat(period)
            if not is_start_day(period_date, frequency):
                return period
            return start_day_to_period(period_date, frequency)

        return normalize_period

    period1_format, normalize_period = detect_period_format(period1)
    period2_format, _ = detect_period_format(period2)

    if period1_format != period2_format:
        logger.error(
            "The 2 periods do not have the same format %r", ((period1, period1_format), (period2, period2_format))
        )
        return (None, None)

    elif period1_format == Frequency.DAILY:
        # Measure the interval between the two periods.
        date_1 = datetime.fromisoformat(period1)
        date_2 = datetime.fromisoformat(period2)
        date_diff = relativedelta(date_2, date_1)
        if date_diff.days == 1:
            return (Frequency.DAILY, None)
        elif date_diff.days == 7:
            return (
                Frequency.WEEKLY,
                make_normalize_period(Frequency.WEEKLY),
            )
        elif date_diff.months == 1:
            return (
                Frequency.MONTHLY,
                make_normalize_period(Frequency.MONTHLY),
            )
        elif date_diff.months == 2:
            return (
                Frequency.BI_MONTHLY,
                make_normalize_period(Frequency.BI_MONTHLY),
            )
        elif date_diff.months == 3:
            return (
                Frequency.QUARTERLY,
                make_normalize_period(Frequency.QUARTERLY),
            )
        elif date_diff.months == 6:
            return (
                Frequency.BI_ANNUAL,
                make_normalize_period(Frequency.BI_ANNUAL),
            )
        elif date_diff.years == 1:
            return (
                Frequency.ANNUAL,
                make_normalize_period(Frequency.ANNUAL),
            )
        else:
            # No specific interval detected, keep daily.
            return (Frequency.DAILY, None)

    return (period1_format, normalize_period)


def detect_period_format(period):
    """Return a tuple like `(period_format, normalize_period)` for the given `period`.

    `normalize_period` can be `None` if period is already normalized,
    or a function taking a period as `str` and returning a normalized period as `str`.

    First, the period format is detected using `detect_period_format_strict`.
    If not found, try to detect non-standard formats, among a variety of well-known invalid ones.

    Periods formats are described in [DBnomics data model](https://git.nomics.world/dbnomics/dbnomics-data-model/).

    See also: `detect_period_format_strict`, `detect_frequency`

    # Working examples:
    >>> detect_period_format("2014")
    (<Frequency.ANNUAL: 'annual'>, None)
    >>> detect_period_format("2014-S1")
    (<Frequency.BI_ANNUAL: 'bi-annual'>, None)
    >>> detect_period_format("2014-B1")
    (<Frequency.BI_MONTHLY: 'bi-monthly'>, None)
    >>> detect_period_format("2014-Q1")
    (<Frequency.QUARTERLY: 'quarterly'>, None)
    >>> detect_period_format("2014-01")
    (<Frequency.MONTHLY: 'monthly'>, None)
    >>> detect_period_format("2014-W01")
    (<Frequency.WEEKLY: 'weekly'>, None)
    >>> detect_period_format("2015-W53")
    (<Frequency.WEEKLY: 'weekly'>, None)
    >>> detect_period_format("2014-12-01")
    (<Frequency.DAILY: 'daily'>, None)
    >>> detect_period_format("2004-05-20")
    (<Frequency.DAILY: 'daily'>, None)

    # Unrecoverable overflow errors:
    >>> detect_period_format("2014-S3")
    (None, None)
    >>> detect_period_format("2014-B7")
    (None, None)
    >>> detect_period_format("2014-Q5")
    (None, None)
    >>> detect_period_format("2014-W54")
    (None, None)
    >>> detect_period_format("2014-12-32")
    (None, None)

    # Recoverable padding errors:
    >>> detect_period_format("2014-S01")  # doctest: +ELLIPSIS
    (<Frequency.BI_ANNUAL: 'bi-annual'>, ...)
    >>> detect_period_format("2014-B01")  # doctest: +ELLIPSIS
    (<Frequency.BI_MONTHLY: 'bi-monthly'>, ...)
    >>> detect_period_format("2014-Q01")  # doctest: +ELLIPSIS
    (<Frequency.QUARTERLY: 'quarterly'>, ...)
    >>> detect_period_format("2014-1")  # doctest: +ELLIPSIS
    (<Frequency.MONTHLY: 'monthly'>, ...)
    >>> detect_period_format("2014-W1")  # doctest: +ELLIPSIS
    (<Frequency.WEEKLY: 'weekly'>, ...)
    >>> detect_period_format("2014-12-1")  # doctest: +ELLIPSIS
    (<Frequency.DAILY: 'daily'>, ...)

    # Recoverable missing hyphen errors:
    >>> detect_period_format("2014S1")  # doctest: +ELLIPSIS
    (<Frequency.BI_ANNUAL: 'bi-annual'>, ...)
    >>> detect_period_format("2014B1")  # doctest: +ELLIPSIS
    (<Frequency.BI_MONTHLY: 'bi-monthly'>, ...)
    >>> detect_period_format("2014Q1")  # doctest: +ELLIPSIS
    (<Frequency.QUARTERLY: 'quarterly'>, ...)
    >>> detect_period_format("2014Q01")  # doctest: +ELLIPSIS
    (<Frequency.QUARTERLY: 'quarterly'>, ...)
    >>> detect_period_format("2014W1")  # doctest: +ELLIPSIS
    (<Frequency.WEEKLY: 'weekly'>, ...)
    >>> detect_period_format("2014W01")  # doctest: +ELLIPSIS
    (<Frequency.WEEKLY: 'weekly'>, ...)

    # Recoverable space errors:
    >>> detect_period_format("2014 S1")  # doctest: +ELLIPSIS
    (<Frequency.BI_ANNUAL: 'bi-annual'>, ...)
    >>> detect_period_format("2014 B1")  # doctest: +ELLIPSIS
    (<Frequency.BI_MONTHLY: 'bi-monthly'>, ...)
    >>> detect_period_format("2014 Q1")  # doctest: +ELLIPSIS
    (<Frequency.QUARTERLY: 'quarterly'>, ...)
    >>> detect_period_format("2014 Q01")  # doctest: +ELLIPSIS
    (<Frequency.QUARTERLY: 'quarterly'>, ...)
    >>> detect_period_format("2014 W1")  # doctest: +ELLIPSIS
    (<Frequency.WEEKLY: 'weekly'>, ...)
    >>> detect_period_format("2014 W01")  # doctest: +ELLIPSIS
    (<Frequency.WEEKLY: 'weekly'>, ...)

    # Unrecoverable missing hyphen errors:
    >>> detect_period_format("2014S3")
    (None, None)
    >>> detect_period_format("2014Q5")
    (None, None)
    >>> detect_period_format("2014Q05")
    (None, None)
    >>> detect_period_format("2014W54")
    (None, None)

    # Invalid formats:
    >>> detect_period_format("ABCDE")
    (None, None)
    >>> detect_period_format("2014Z01")
    (None, None)
    """
    # First try to detect the period format in a strict manner.

    period_format = detect_period_format_strict(period)
    if period_format is not None:
        return (period_format, None)

    # Fallback: try to detect non-standard period formats.

    def normalize_period(format_match):
        def _normalize_period(period):
            match = regex.match(period)
            return format_match(match) if match is not None else period

        return _normalize_period

    for period_format, regex, format_match in [
        (
            Frequency.BI_ANNUAL,
            re.compile(r"^(\d{4})[-\s]*[sS]0*([1-2])$"),
            lambda match: "{0}-S{1}".format(*match.groups()),
        ),
        (
            Frequency.BI_MONTHLY,
            re.compile(r"^(\d{4})[-\s]*[bB]0*([1-6])$"),
            lambda match: "{0}-B{1}".format(*match.groups()),
        ),
        (
            Frequency.QUARTERLY,
            re.compile(r"^(\d{4})[-\s]*[qQ]0*([1-4])$"),
            lambda match: "{0}-Q{1}".format(*match.groups()),
        ),
        (
            Frequency.MONTHLY,
            re.compile(r"^(\d{4})[-\s]*[mM]?0*(\d{1,2})$"),
            lambda match: "{0}-{1:>02}".format(*match.groups()),
        ),
        (
            Frequency.WEEKLY,
            re.compile(r"^(\d{4})[-\s]*[wW]0*([1-9]|[1-4][0-9]|5[0-2])$"),
            lambda match: "{0}-W{1:>02}".format(*match.groups()),
        ),
        (
            Frequency.DAILY,
            re.compile(r"^(\d{4})[-\s]*(0[1-9]|1[0-2])[-\s]*(0[1-9]|[1-9]|[1-2][0-9]|3[0-1])$"),
            lambda match: "{0}-{1:>02}-{1:>02}".format(*match.groups()),
        ),
    ]:
        match = regex.match(period)
        if match is not None:
            return (period_format, normalize_period(format_match))

    return (None, None)


def detect_period_format_strict(period):
    """Return a period format as `str` for the given `period`, or `None` if unable to detect.

    Periods formats are described in [DBnomics data model](https://git.nomics.world/dbnomics/dbnomics-data-model/).

    See also: `detect_period_format`, `detect_frequency`

    # Working examples:
    >>> detect_period_format_strict("2014")
    <Frequency.ANNUAL: 'annual'>
    >>> detect_period_format_strict("2014-S1")
    <Frequency.BI_ANNUAL: 'bi-annual'>
    >>> detect_period_format_strict("2014-B1")
    <Frequency.BI_MONTHLY: 'bi-monthly'>
    >>> detect_period_format_strict("2014-Q1")
    <Frequency.QUARTERLY: 'quarterly'>
    >>> detect_period_format_strict("2014-01")
    <Frequency.MONTHLY: 'monthly'>
    >>> detect_period_format_strict("2014-W01")
    <Frequency.WEEKLY: 'weekly'>
    >>> detect_period_format_strict("2015-W53")
    <Frequency.WEEKLY: 'weekly'>
    >>> detect_period_format_strict("2014-12-01")
    <Frequency.DAILY: 'daily'>
    >>> detect_period_format_strict("2004-05-20")
    <Frequency.DAILY: 'daily'>

    # Overflow errors:
    >>> detect_period_format_strict("2014-S0")
    >>> detect_period_format_strict("2014-S3")
    >>> detect_period_format_strict("2014-B0")
    >>> detect_period_format_strict("2014-B7")
    >>> detect_period_format_strict("2014-Q0")
    >>> detect_period_format_strict("2014-Q5")
    >>> detect_period_format_strict("2014-W00")
    >>> detect_period_format_strict("2014-W54")
    >>> detect_period_format_strict("2014-12-00")
    >>> detect_period_format_strict("2014-12-32")

    # Invalid formats:
    >>> detect_period_format_strict("ABCDE")
    >>> detect_period_format_strict("2014Z01")
    """
    assert isinstance(period, str), "{!r} should by a string; got {}".format(period, type(period))
    for period_format, regex in period_format_strict_regex_list:
        if regex.match(period):
            return period_format
    return None


def is_start_day(date: date, frequency: Frequency):  # noqa: D103
    if frequency == Frequency.ANNUAL:
        return date.day == 1 and date.month == 1
    elif frequency == Frequency.BI_ANNUAL:
        return date.day == 1 and date.month in {1, 7}
    elif frequency == Frequency.QUARTERLY:
        return date.day == 1 and date.month in {1, 4, 7, 10}
    elif frequency == Frequency.BI_MONTHLY:
        return date.day == 1 and date.month in {1, 3, 5, 7, 9, 11}
    elif frequency == Frequency.MONTHLY:
        return date.day == 1
    elif frequency == Frequency.WEEKLY:
        return date.isoweekday() == 1  # monday
    elif frequency == Frequency.DAILY:
        return True

    raise ValueError(f"Unsupported frequency: {frequency}")


def period_to_start_day(period):
    """Return the start day of `period` as ISO-8601 date string.

    >>> period_to_start_day("")
    >>> period_to_start_day("2000-W00")
    >>> period_to_start_day("2001")
    datetime.date(2001, 1, 1)
    >>> period_to_start_day("2001-S1")
    datetime.date(2001, 1, 1)
    >>> period_to_start_day("2001-S2")
    datetime.date(2001, 7, 1)
    >>> period_to_start_day("2001-B1")
    datetime.date(2001, 1, 1)
    >>> period_to_start_day("2001-B2")
    datetime.date(2001, 3, 1)
    >>> period_to_start_day("2001-B5")
    datetime.date(2001, 9, 1)
    >>> period_to_start_day("2001-B6")
    datetime.date(2001, 11, 1)
    >>> period_to_start_day("2001-Q1")
    datetime.date(2001, 1, 1)
    >>> period_to_start_day("2001-Q3")
    datetime.date(2001, 7, 1)
    >>> period_to_start_day("2001-Q4")
    datetime.date(2001, 10, 1)
    >>> period_to_start_day("2001-03")
    datetime.date(2001, 3, 1)
    >>> period_to_start_day("2001-11")
    datetime.date(2001, 11, 1)
    >>> period_to_start_day("2001-W01")
    datetime.date(2001, 1, 1)
    >>> period_to_start_day("2001-W02")
    datetime.date(2001, 1, 8)
    >>> period_to_start_day("2001-W11")
    datetime.date(2001, 3, 12)
    >>> period_to_start_day("2001-03-04")
    datetime.date(2001, 3, 4)
    >>> period_to_start_day("2001-11-12")
    datetime.date(2001, 11, 12)
    """
    for period_format, regex in period_format_strict_regex_list:
        match = regex.match(period)
        if match is not None:
            if period_format == Frequency.ANNUAL:
                year = match.group(1)
                return date(int(year), 1, 1)
            elif period_format == Frequency.BI_ANNUAL:
                year, index = match.groups()
                index = int(index)
                assert index in {1, 2}
                month = index * 6 - 5
                return date(int(year), month, 1)
            elif period_format == Frequency.BI_MONTHLY:
                year, index = match.groups()
                index = int(index)
                assert index in range(1, 7)
                month = index * 2 - 1
                return date(int(year), month, 1)
            elif period_format == Frequency.QUARTERLY:
                year, index = match.groups()
                index = int(index)
                assert index in range(1, 5)
                month = index * 3 - 2
                return date(int(year), month, 1)
            elif period_format == Frequency.MONTHLY:
                year, month = match.groups()
                return date(int(year), int(month), 1)
            elif period_format == Frequency.WEEKLY:
                return datetime.strptime("{}-1".format(period), "%G-W%V-%u").date()
            elif period_format == Frequency.DAILY:
                year, month, day = match.groups()
                return date(int(year), int(month), int(day))
            else:
                raise ValueError(f"Unsupported period format: {period_format!r}")

    return None


def start_day_to_period(period_date: date, frequency: Frequency):
    """Simplfy the `str` representation of `period_date` based on `frequency`.

    If `period_date` is the start day of the period defined by `frequency`,
    return a simpler representation of `period_date` as `str`,
    otherwise return `period_date` as ISO format.

    >>> start_day_to_period(date(2000, 1, 1), Frequency.ANNUAL)
    '2000'
    >>> start_day_to_period(date(2000, 1, 1), Frequency.BI_ANNUAL)
    '2000-S1'
    >>> start_day_to_period(date(2000, 7, 1), Frequency.BI_ANNUAL)
    '2000-S2'
    >>> start_day_to_period(date(2000, 1, 1), Frequency.BI_MONTHLY)
    '2000-B1'
    >>> start_day_to_period(date(2000, 1, 1), Frequency.QUARTERLY)
    '2000-Q1'
    >>> start_day_to_period(date(2000, 4, 1), Frequency.QUARTERLY)
    '2000-Q2'
    >>> start_day_to_period(date(2000, 1, 1), Frequency.MONTHLY)
    '2000-01'
    >>> start_day_to_period(date(2000, 1, 3), Frequency.WEEKLY)
    '2000-W01'
    >>> start_day_to_period(date(2000, 1, 1), Frequency.DAILY)
    '2000-01-01'

    # `period_date` is not the start day:
    >>> start_day_to_period(date(2000, 2, 3), Frequency.ANNUAL)
    '2000-02-03'
    >>> start_day_to_period(date(2000, 2, 3), Frequency.BI_ANNUAL)
    '2000-02-03'
    >>> start_day_to_period(date(2000, 6, 8), Frequency.BI_ANNUAL)
    '2000-06-08'
    >>> start_day_to_period(date(2000, 8, 21), Frequency.BI_ANNUAL)
    '2000-08-21'
    >>> start_day_to_period(date(2000, 12, 31), Frequency.BI_ANNUAL)
    '2000-12-31'
    >>> start_day_to_period(date(2000, 2, 3), Frequency.BI_MONTHLY)
    '2000-02-03'
    >>> start_day_to_period(date(2000, 3, 7), Frequency.BI_MONTHLY)
    '2000-03-07'
    >>> start_day_to_period(date(2000, 2, 3), Frequency.QUARTERLY)
    '2000-02-03'
    >>> start_day_to_period(date(2000, 4, 6), Frequency.QUARTERLY)
    '2000-04-06'
    >>> start_day_to_period(date(2000, 2, 3), Frequency.MONTHLY)
    '2000-02-03'
    >>> start_day_to_period(date(2000, 5, 8), Frequency.MONTHLY)
    '2000-05-08'
    >>> start_day_to_period(date(2000, 1, 1), Frequency.WEEKLY)
    '2000-01-01'
    >>> start_day_to_period(date(2000, 2, 3), Frequency.WEEKLY)
    '2000-02-03'
    """
    if not is_start_day(period_date, frequency):
        return period_date.isoformat()

    if frequency == Frequency.ANNUAL:
        return period_date.strftime("%Y")
    elif frequency == Frequency.BI_ANNUAL:
        return "{}-S{}".format(period_date.year, math.ceil(period_date.month / 6))
    elif frequency == Frequency.QUARTERLY:
        return "{}-Q{}".format(period_date.year, math.ceil(period_date.month / 3))
    elif frequency == Frequency.BI_MONTHLY:
        return "{}-B{}".format(period_date.year, math.ceil(period_date.month / 2))
    elif frequency == Frequency.MONTHLY:
        return period_date.strftime("%Y-%m")
    elif frequency == Frequency.WEEKLY:
        return period_date.strftime("%G-W%V")
    elif frequency == Frequency.DAILY:
        return period_date.isoformat()

    raise ValueError("Unsupported frequency: {}".format(frequency))
