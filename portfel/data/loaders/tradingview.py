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

"""TradingView CSV exports."""

import csv
import datetime
import os

import portfel.data.series as series

FIELD_MAP = {
    'time': 'time',
    'open': 'open',
    'high': 'high',
    'low': 'low',
    'Volume': 'volume',
    'Earnings Period': 'earnings-period',
    'Earnings Reported': 'earnings',
    'Earnings Confirmed': 'earnings',
    'Split numerator': 'split',
    'Split denominator': 'split',
    'Dividends amount': 'dividend',
}


def parse_filename(filename):
    """Parse file name to extract ticker and resolution."""
    basename = os.path.basename(filename)
    base = os.path.splitext(basename)[0]
    ticker, resolution = base.split(',')
    if '_DLY_' in ticker:  # Delayed quotes, but we don't care about that.
        ticker = ticker.replace('_DLY_', '_')
    ticker = ticker.replace('_', ':')
    resolution = resolution.strip().lower()
    return {
        'ticker': ticker,
        'resolution': resolution,
    }


def convert_row(csv_row):
    """Covert CSV row to standard series keys and formats."""
    row = {}

    if csv_row['time'].isdigit():
        row['time'] = datetime.datetime.fromtimestamp(int(csv_row['time']))

    for k in ['open', 'close', 'high', 'low', 'Volume']:
        if k in csv_row:
            row[k.lower()] = float(csv_row[k])

    return row


def load(path, resolution, ticker):
    """Load time series from TradingView CSV export."""
    if resolution == 'auto' or ticker == 'auto':
        metadata = parse_filename(path)
    else:
        metadata = {}

    if resolution != 'auto':
        metadata['resolution'] = resolution
    if ticker != 'auto':
        metadata['ticker'] = ticker

    with open(path, 'rt', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [convert_row(row) for row in reader]

    return series.Series(rows, metadata)
