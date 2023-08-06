from __future__ import annotations

import datetime


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


class date(datetime.date):
    """Date with time zone."""

    __slots__ = "_tzinfo"

    def __new__(
        cls, year=0, month=0, day=0, tzinfo: datetime.tzinfo | None = None
    ):  # pylint: disable=signature-differs
        """Constructor.

        Arguments:

        year, month, day, tzinfo (required, base 1)
        """
        self = datetime.date.__new__(cls, year=year, month=month, day=day)
        _check_tzinfo_arg(tzinfo)
        self._tzinfo = tzinfo
        return self

    # Read-only field accessors

    @property
    def tzinfo(self) -> datetime.tzinfo | None:
        """timezone info object"""
        return self._tzinfo

    # Comparisons of date objects with other.

    def __eq__(self, other):
        if isinstance(other, date):
            return self._cmp(other) == 0
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, date):
            return self._cmp(other) != 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, date):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, date):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) > 0
        return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, date)
        y, m, d, tz = self.year, self.month, self.day, self.tzinfo
        y2, m2, d2, tz2 = other.year, other.month, other.day, other.tzinfo

        offset1 = (tz or datetime.timezone.utc).utcoffset(None) or datetime.timedelta(0)
        offset2 = (tz2 or datetime.timezone.utc).utcoffset(None) or datetime.timedelta(0)

        return _cmp((y, m, d, -offset1), (y2, m2, d2, -offset2))


def _check_tzinfo_arg(tz):
    if tz is not None and not isinstance(tz, datetime.tzinfo):
        raise TypeError("tzinfo argument must be None or of a tzinfo subclass")
