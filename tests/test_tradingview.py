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

"""Tests for the TradingView loader."""

import pytest

import portfel.data.loaders.tradingview as tv


@pytest.mark.parametrize('name,expect_params', [
    ('/a/b/BATS_SPY, 1D.csv', {'ticker': 'BATS:SPY', 'resolution': '1d',
                               'currency': 'USD'}),
    ('XETR_DLY_ALV, 1W.csv', {'ticker': 'XETR:ALV', 'resolution': '1w',
                              'currency': 'EUR'}),
    ('XETR_DLY ALV, 1W.csv', {'ticker': 'XETR:ALV', 'resolution': '1w',
                              'currency': 'EUR'}),
    ('XETR_DLY ALV, 1W(2).csv', {'ticker': 'XETR:ALV', 'resolution': '1w',
                                 'currency': 'EUR'}),
])
def test_tv_name_parser(name, expect_params):
    assert tv.parse_filename(name) == expect_params
