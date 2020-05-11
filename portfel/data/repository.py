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

"""Filesystem-based data repository."""

import csv
import os

import portfel.data.series as srs


# Field of the index file.
INDEX_FIELDS = [
    'ticker',      # Ticker
    'resolution',  # Time resolution
    'currency',    # Currency
    'source',      # Data source
    'filename',    # File name
]


class Repository:
    """Data repository."""

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            self._init()
        self._load_index()

    @property
    def _index_path(self):
        return os.path.join(self.path, 'index.csv')

    def _init(self):
        """Initialize the repository."""
        os.makedirs(self.path)
        self._save_index([])

    def _load_index(self):
        """Load repository index."""
        with open(self._index_path, 'rt', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=INDEX_FIELDS)
            self.index = [
                rec for rec in reader
                if rec['ticker'] != 'ticker'  # Skip header.
            ]

    def _save_index(self, index=None):
        """Save repository index (or other provided index)."""
        if index is None:
            index = self.index
        with open(self._index_path, 'wt', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=INDEX_FIELDS)
            writer.writeheader()
            writer.writerows(index)

    def _find_by_params(self, **params):
        """Find series in the index by parameters."""
        return [
            rec for rec in self.index
            if all(rec[p] == params[p] for p in params)
        ]

    @staticmethod
    def _series_filename(series):
        """Determine file name for the series."""
        return '{}_{}'.format(series.ticker, series.resolution)

    def add_series(self, series):
        """Add series to the repository."""
        filename = self._series_filename(series)
        series.save_rows(os.path.join(self.path, filename))
        self.index.append({
            'ticker': series.ticker,
            'resolution': series.resolution,
            'source': series.source,
            'currency': series.currency,
            'filename': filename,
        })
        self._save_index()

    def get_series(self, ticker, resolution):
        """Load and return series by exact ticker and resolution."""
        matches = [
            rec for rec in self.index
            if rec['ticker'] == ticker and rec['resolution'] == resolution
        ]
        if len(matches) == 1:
            rec = matches[0]
            ret = srs.Series(
                rec['ticker'],
                rec['resolution'],
                rec['currency'],
                rec['source'],
            )
            ret.load_rows(os.path.join(self.path, rec['filename']))
            return ret
        else:
            raise KeyError('{}@{}'.format(ticker, resolution))