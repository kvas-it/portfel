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

"""Dispatcher for loading data from external sources."""

import logging

import portfel.data.loaders.tradingview as tradingview

LOADERS = {
    'tradingview': tradingview,
}


def load_series(path, format='tradingview', resolution='auto', exchange='auto',
                ticker='auto', currency='auto'):
    """Load time series from a file."""
    loader = LOADERS[format]
    series = loader.load(path, resolution=resolution, exchange=exchange,
                         ticker=ticker, currency=currency)
    logging.info(
        'Loaded series from %s (%d records, from %s to %s, fields: %s)',
        path, len(series), series.index.min(), series.index.max(),
        ', '.join(sorted(series.keys())),
    )
    return series
