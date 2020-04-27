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

# Field of the index file.
INDEX_FIELDS = [
    'ticker',      # Ticker
    'resolution',  # Time resolution
    'source',      # Data source
    'start',       # Timestamp of the first record
    'end',         # Timestamp of the last record
    'count',       # Total number of records
    'fields',      # Field names, sorted and space-separated
    'filename',    # File name
]


class Repository:
    """Data repository."""

    def __init__(self, path):
        self.path = path
        if not os.path.exist(path):
            self._init()
        self._load_index()

    @property
    def _index_path(self):
        return os.path.join(self.path, 'index.csv')

    def _init(self):
        """Initialize the repository."""
        os.makedirs(os.path)
        self._save_index([])

    def _load_index(self):
        """Load repository index."""
        with open(self._index_path, 'rt', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=INDEX_FIELDS)
            self.index = list(reader)

    def _save_index(self, index=None):
        """Save repository index (or other provided index)."""
        if index is None:
            index = self.index
        with open(self._index_path, 'wt', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=INDEX_FIELDS)
            writer.writeheader()
            for item in index:
                writer.writerow(item)

    def _find_by_params(self, **params):
        """Find series in the index by parameters."""
        return [
            rec for rec in self.index
            if all(rec[p] == params[p] for p in params)
        ]

    def add_series(self, series):
        """Add series to the repository."""
