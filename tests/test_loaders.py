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


def test_tradingview(spy_1d):
    """Test loading TradeView CSV export."""
    assert spy_1d.exchange == 'BATS'
    assert spy_1d.ticker == 'SPY'
    assert spy_1d.resolution == '1d'
    assert spy_1d.currency == 'USD'
    assert set(spy_1d.keys()) == {'open', 'high', 'low', 'close', 'volume'}
    assert spy_1d.index[0] == datetime.datetime(2002, 9, 16, 13, 30)
    assert dict(spy_1d.iloc[0]) == {
        'open': 5.54452519,
        'high': 5.6036668,
        'low': 5.35231499,
        'close': 5.41145659,
        'volume': 4272182,
    }
    assert len(spy_1d) == 19


def test_tv_extras(alv_1d):
    """Test loading TradeView CSV export with extra fields."""
    assert alv_1d.exchange == 'FWB'
    assert alv_1d.ticker == 'ALV'
    assert alv_1d.resolution == '1d'
    assert alv_1d.currency == 'EUR'
    assert set(alv_1d.keys()) == {
        'open', 'high', 'low', 'close', 'volume',
        'earnings-period', 'earnings-estimate', 'earnings',
        'split', 'dividend',
    }

    earnings = alv_1d['earnings']
    assert (earnings.isnull() == [True, False, False, True, False]).all()
    assert earnings[1] == 4.38
    assert earnings[2] == 4.44

    split = alv_1d['split']
    assert (split.isnull() == [True, True, True, True, False]).all()
    assert split[4] == '5/7'

    dividend = alv_1d['dividend']
    assert (dividend.isnull() == [True, True, True, False, True]).all()
    assert dividend[3] == 4

    ep = alv_1d['earnings-period']
    assert (ep.isnull() == [True, False, False, True, False]).all()
    assert ep[1] == datetime.datetime(2015, 6, 30, 0)

    ee = alv_1d['earnings-estimate']
    assert (ee.isnull() == [True, False, True, True, True]).all()
    assert ee[1] == 3.9
