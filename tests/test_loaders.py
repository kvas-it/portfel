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
import portfel.data.loaders.tradingview as tv


@pytest.mark.parametrize('name,expect_params', [
    ('/a/b/BATS_SPY, 1D.csv', {'ticker': 'BATS:SPY', 'resolution': '1d'}),
    ('XETR_DLY_ALV, 1W.csv', {'ticker': 'XETR:ALV', 'resolution': '1w'}),
])
def test_tv_name_parser(name, expect_params):
    assert tv.parse_filename(name) == expect_params


@pytest.fixture()
def data_path():
    return py.path.local(__file__).dirpath('data')


def test_tv(data_path):
    """Test loading TradeView CSV export."""
    series = ldr.load_series(data_path.join('BATS_SPY, 1D.csv'), format='tv')

    assert series.ticker == 'BATS:SPY'
    assert series.resolution == '1d'
    assert series[0] == {
        'time': datetime.datetime(2002, 9, 16, 15, 30),
        'open': 5.54452519,
        'high': 5.6036668,
        'low': 5.35231499,
        'close': 5.41145659,
        'volume': 4272182,
    }
    assert len(series) == 19
