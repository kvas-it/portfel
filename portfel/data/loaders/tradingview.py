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
    'Earnings period': 'earnings-period',
    'Earnings reported': 'earnings',
    'Earnings confirmed': 'earnings',
    'Earnings estimated': 'earnings-estimate',
    'Split numerator': 'split',
    'Split denominator': 'split',
    'Dividends amount': 'dividend',
}

CURRENCY_DEFAULTS = {
    'BATS': 'USD',
    'XETR': 'EUR',
    'FWB': 'EUR',
    'SWB': 'EUR',
}


def parse_filename(filename):
    """Parse file name to extract ticker and resolution."""
    basename = os.path.basename(filename)
    base = os.path.splitext(basename)[0]
    base = base.split('(')[0]  # Browsers add (i) to copies of same file.
    ticker, resolution = base.split(',')
    ticker = ticker.replace(' ', '_')
    if '_DLY_' in ticker:  # Delayed quotes, but we don't care about that.
        ticker = ticker.replace('_DLY_', '_')
    ticker = ticker.replace('_', ':')
    resolution = resolution.strip().lower()
    prefix = ticker.split(':')[0]
    currency = CURRENCY_DEFAULTS.get(prefix, 'USD')
    return {
        'ticker': ticker,
        'resolution': resolution,
        'currency': currency,
    }


def extract_earnings(csv_row):
    """Extract earnings information from CSV row."""
    row = {}

    for k in ['Earnings period', 'Earnings reported', 'Earnings confirmed',
              'Earnings estimated']:
        if k in csv_row:
            row[FIELD_MAP[k]] = None

    if 'Earnings period' in csv_row:
        ep = csv_row['Earnings period']
        if ep.isdigit():
            ep = int(ep)
        else:
            raise ValueError('Earnings period must be a timestamp')

        if ep == 0:
            # Present but 0 earnings period means no earnings in this row.
            return row

        row['earnings-period'] = datetime.datetime.fromtimestamp(ep)

    for k in ['Earnings reported', 'Earnings confirmed', 'Earnings estimated']:
        if k in csv_row:
            e = series.load_float(csv_row[k])
            if e is not None:
                row[FIELD_MAP[k]] = e

    return row


def convert_row(csv_row):
    """Covert CSV row to standard series keys and formats."""
    row = {}

    if csv_row['time'].isdigit():
        row['time'] = datetime.datetime.fromtimestamp(int(csv_row['time']))
    else:
        raise ValueError('time must be a timestamp')

    for k in ['open', 'close', 'high', 'low', 'Volume']:
        if k in csv_row:
            row[k.lower()] = series.load_float(csv_row[k])

    row.update(extract_earnings(csv_row))

    if 'Dividends amount' in csv_row:
        row['dividend'] = series.load_float(csv_row['Dividends amount'],
                                            allow_0=False)

    if 'Split numerator' in csv_row and 'Split denominator' in csv_row:
        n = csv_row['Split numerator']
        d = csv_row['Split denominator']
        row['split'] = None
        if n.isdigit() and d.isdigit():
            n = int(n)
            d = int(d)
        if n != 0 and d != 0:
            row['split'] = '{}/{}'.format(n, d)

    return row


def load(path, resolution, ticker, currency):
    """Load time series from TradingView CSV export."""
    kw = {'source': 'TradingView'}

    if 'auto' in [resolution, ticker, currency]:
        kw.update(parse_filename(path))

    if resolution != 'auto':
        kw['resolution'] = resolution
    if ticker != 'auto':
        kw['ticker'] = ticker
    if currency != 'auto':
        kw['currency'] = currency.upper()

    with open(path, 'rt', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        kw['rows'] = [convert_row(row) for row in reader]

    return series.Series(**kw)
