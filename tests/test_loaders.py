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

"""Tests for the data loader."""

import datetime

import py
import pytest

import portfel.data.loader as ldr


@pytest.fixture()
def data_path():
    return py.path.local(__file__).dirpath('data')


def test_tradingview(data_path):
    """Test loading TradeView CSV export."""
    path = data_path.join('BATS_SPY, 1D.csv').strpath
    series = ldr.load_series(path, 'tradingview')

    assert series.ticker == 'BATS:SPY'
    assert series.resolution == '1d'
    assert series.currency == 'USD'
    assert series.source == 'TradingView'
    assert series.fields == {'time', 'open', 'high', 'low', 'close', 'volume'}
    assert series[0] == {
        'time': datetime.datetime(2002, 9, 16, 15, 30),
        'open': 5.54452519,
        'high': 5.6036668,
        'low': 5.35231499,
        'close': 5.41145659,
        'volume': 4272182,
    }
    assert len(series) == 19


def test_tv_extras(data_path):
    """Test loading TradeView CSV export with extra fields."""
    path = data_path.join('FWB_DLY_ALV, 1D.csv').strpath
    series = ldr.load_series(path, 'tradingview')

    assert series.ticker == 'FWB:ALV'
    assert series.resolution == '1d'
    assert series.currency == 'EUR'
    assert series.source == 'TradingView'
    assert series.fields == {'time', 'open', 'high', 'low', 'close', 'volume',
                             'earnings-period', 'earnings-estimate',
                             'earnings', 'split', 'dividend'}

    assert series[0]['earnings'] is None
    assert series[0]['earnings-period'] is None
    assert series[0]['earnings-estimate'] is None
    assert series[0]['dividend'] is None
    assert series[0]['split'] is None
    assert series[1]['dividend'] is None
    assert series[1]['earnings-period'] == datetime.datetime(2015, 6, 30, 2, 0)
    assert series[1]['earnings'] == 4.38
    assert series[1]['earnings-estimate'] == 3.90
    assert series[2]['earnings'] == 4.44
    assert series[2]['earnings-estimate'] is None
    assert series[3]['dividend'] == 4
    assert series[4]['split'] == '5/7'
