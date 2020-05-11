# This file is part of Portfel,
# Copyright (C) 2020 Vasily Kuznetsov
#
# Portfel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Portfel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Portfel. If not, see <http://www.gnu.org/licenses/>.

"""Time series."""

import csv
import datetime


def load_int(v, allow_0=True):
    """Convert int value after loading from a CSV file."""
    if v.lower() in ['nan', '']:
        return None
    v = int(v)
    if v == 0 and not allow_0:
        return None
    return v


def load_float(v, allow_0=True):
    """Convert float value after loading from a CSV file."""
    if v.lower() in ['nan', '']:
        return None
    v = float(v)
    if v == 0 and not allow_0:
        return None
    return v


def load_timestamp(v):
    """Convert timestamp after loading from a CSV file."""
    v = load_int(v, allow_0=False)
    if v is not None:
        return datetime.datetime.fromtimestamp(v)
    # else, return None


def load_nonempty(v):
    """Return None if v == ''."""
    if v != '':
        return v


def save_timestamp(v):
    """Convert timestamp for saving in CSV file."""
    if v is None:
        return v
    return int(v.timestamp())


# Functions to use for loading specific fields.
FIELD_LOADERS = {
    'time': load_timestamp,
    'earnings-period': load_timestamp,
    'earnings': load_float,
    'earnings-estimate': load_float,
    'dividend': load_float,
    'open': load_float,
    'high': load_float,
    'low': load_float,
    'close': load_float,
    'volume': load_float,
    'split': load_nonempty,
}

# Functions to use for saving specific fields.
FIELD_SAVERS = {
    'time': save_timestamp,
    'earnings-period': save_timestamp,
}


def _time_step(resolution):
    """Return time step by resolution."""
    if resolution == '1d':
        return datetime.timedelta(days=1)

    raise ValueError('Unsupported resolution: ' + resolution)


def _time_round(t, resolution, high=False):
    if resolution == '1d':
        if high:
            return t.replace(hour=23, minute=59, second=59, microsecond=0)
        else:
            return t.replace(hour=0, minute=0, second=0, microsecond=0)

    raise ValueError('Unsupported resolution: ' + resolution)


def merge(a, b):
    """Merge two series into one (b has precedence)."""
    # TODO: check that parameters match?

    result = Series(a.ticker, a.resolution, a.currency, a.source)
    result.fields = a.fields | b.fields

    a_recs = {_time_round(r['time'], a.resolution): r for r in a}
    b_recs = {_time_round(r['time'], a.resolution): r for r in b}

    start = _time_round(min(a[0]['time'], b[0]['time']), a.resolution)
    end = _time_round(max(a[-1]['time'], b[-1]['time']), a.resolution,
                      high=True)
    step = _time_step(a.resolution)

    date = start
    while date < end:  # range() can't work with dates so we iterate manually.
        rec = {}
        if date in a_recs:
            rec.update(a_recs[date])
        if date in b_recs:
            rec.update(b_recs[date])
        if rec:
            result.append(rec)
        date += step

    return result


class Series(list):
    """Time series data."""

    def __init__(self, ticker, resolution, currency, source, rows=[]):
        list.__init__(self, rows)
        self.ticker = ticker
        self.resolution = resolution
        self.currency = currency
        self.source = source
        if rows:
            self.fields = set(rows[0].keys())
        else:
            self.fields = None

    def save_rows(self, csv_path):
        """Save the rows of this series to a CSV file."""
        with open(csv_path, 'wt', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(self.fields))
            writer.writeheader()
            for row in self:
                adjusted_row = {
                    k: v if k not in FIELD_SAVERS else FIELD_SAVERS[k](v)
                    for k, v in row.items()
                }
                writer.writerow(adjusted_row)

    def load_rows(self, csv_path):
        """Load the rows from a CSV file."""
        if len(self) > 0:
            raise ValueError('This series already has rows')

        with open(csv_path, 'rt', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.append({
                    k: v if k not in FIELD_LOADERS else FIELD_LOADERS[k](v)
                    for k, v in row.items()
                })

        if len(self) > 0:
            self.fields = set(self[0].keys())

    def __eq__(self, other):
        """Is this the same series with the same rows?"""
        return (
            self.ticker == other.ticker and
            self.resolution == other.resolution and
            self.currency == other.currency and
            self.source == other.source and
            self.fields == other.fields and
            all(a == b for (a, b) in zip(self, other))
        )
