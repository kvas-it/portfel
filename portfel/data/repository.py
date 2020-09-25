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

"""Filesystem-based data repository that uses CSV files."""

import os

import pandas as pd

import portfel.data.convert as conv
import portfel.data.series as ds

# Field of the index file.
INDEX_FIELDS = [
    'exchange',    # Exchange
    'ticker',      # Ticker
    'resolution',  # Time resolution
    'currency',    # Currency
    'filename',    # File name
    'first-time',  # Timestamp of the earliest record
    'last-time',   # Timestamp of the latest record
]

# Converters for loading time series from CSV files.
CONVERTERS = {
    'time': conv.to_timestamp,
    'earnings-period': conv.to_timestamp,
}


class Repository:
    """Data repository."""

    def __init__(self, path):
        self.path = path
        self._index_path = os.path.join(self.path, 'index.csv')
        if os.path.exists(path):
            self._load_index()
        else:
            self._init()

    def _init(self):
        """Initialize the repository."""
        os.makedirs(self.path)
        self.index = pd.DataFrame({f: [] for f in INDEX_FIELDS})
        self._save_index()

    def _load_index(self):
        """Load the index of available securities."""
        self.index = pd.read_csv(self._index_path)

    def _save_index(self):
        """Save the index of available securities."""
        self.index.to_csv(self._index_path)

    @staticmethod
    def _series_filename(series):
        """Determine file name for the series."""
        return '{}_{}_{}.csv'.format(series.exchange,
                                     series.ticker,
                                     series.resolution)

    def add_series(self, series):
        """Add series to the repository."""
        rec = self._get_index_record(series.exchange, series.ticker,
                                     series.resolution)

        if rec is None:
            rec = {
                'exchange': series.exchange,
                'ticker': series.ticker,
                'resolution': series.resolution,
                'currency': series.currency,
                'filename': self._series_filename(series),
                'first-time': series.index.min(),
                'last-time': series.index.max(),
            }
            self.index = self.index.append([rec])
        else:
            print(rec)
            existing = self._load_series(rec)
            print(existing.index)
            print(series.index)
            # series = pd.merge(existing, series, on='time')
            series = pd.concat([existing, series])
            series = series[~series.index.duplicated(keep='last')]
            print(series)
            rec['first-time'] = series.index.min()
            rec['last-time'] = series.index.max()

        self._save_index()
        self._save_series(rec, series)

    def _get_index_record(self, exchange, ticker, resolution):
        """Get index record by ticker and resolution."""
        matches = self.index[
            (self.index['exchange'] == exchange)
            & (self.index['ticker'] == ticker)
            & (self.index['resolution'] == resolution)
        ]
        if len(matches) == 1:
            return matches.iloc[0]
        elif len(matches) > 1:
            raise Exception('Multiple index records for {}@{} - repo corrupt?'
                            .format(ticker, resolution))
        # otherwise return None

    def _load_series(self, index_record):
        """Load series by index_record."""
        data_path = os.path.join(self.path, index_record['filename'])
        data = pd.read_csv(data_path, converters=CONVERTERS,
                           float_precision='high')
        # High precision float converter above is necessary to avoid drift of
        # the floating point values. test_get_series fails without it.
        ret = ds.Series(data)
        for key in ret._metadata:
            setattr(ret, key, index_record[key])
        return ret

    def _save_series(self, index_record, series):
        """Save series using the index_record."""
        data_path = os.path.join(self.path, index_record['filename'])
        series.to_csv(data_path)

    def get_series(self, exchange, ticker, resolution):
        """Load and return series by exact ticker and resolution."""
        rec = self._get_index_record(exchange, ticker, resolution)
        if rec is None:
            raise KeyError('{}:{}@{}'.format(exchange, ticker, resolution))
        return self._load_series(rec)
