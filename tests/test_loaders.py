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

import portfel.data.loader as ldr


def test_tradingview(spy_1d):
    """Test loading TradeView CSV export."""
    assert spy_1d.ticker == 'BATS:SPY'
    assert spy_1d.resolution == '1d'
    assert spy_1d.currency == 'USD'
    assert spy_1d.source == 'TradingView'
    assert spy_1d.fields == {'time', 'open', 'high', 'low', 'close', 'volume'}
    assert spy_1d[0] == {
        'time': datetime.datetime(2002, 9, 16, 15, 30),
        'open': 5.54452519,
        'high': 5.6036668,
        'low': 5.35231499,
        'close': 5.41145659,
        'volume': 4272182,
    }
    assert len(spy_1d) == 19


def test_tv_extras(alv_1d):
    """Test loading TradeView CSV export with extra fields."""
    assert alv_1d.ticker == 'FWB:ALV'
    assert alv_1d.resolution == '1d'
    assert alv_1d.currency == 'EUR'
    assert alv_1d.source == 'TradingView'
    assert alv_1d.fields == {'time', 'open', 'high', 'low', 'close', 'volume',
                              'earnings-period', 'earnings-estimate',
                              'earnings', 'split', 'dividend'}

    assert alv_1d[0]['earnings'] is None
    assert alv_1d[0]['earnings-period'] is None
    assert alv_1d[0]['earnings-estimate'] is None
    assert alv_1d[0]['dividend'] is None
    assert alv_1d[0]['split'] is None
    assert alv_1d[1]['dividend'] is None
    assert alv_1d[1]['earnings-period'] == datetime.datetime(2015, 6, 30, 2)
    assert alv_1d[1]['earnings'] == 4.38
    assert alv_1d[1]['earnings-estimate'] == 3.90
    assert alv_1d[2]['earnings'] == 4.44
    assert alv_1d[2]['earnings-estimate'] is None
    assert alv_1d[3]['dividend'] == 4
    assert alv_1d[4]['split'] == '5/7'
