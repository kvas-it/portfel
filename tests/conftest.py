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

"""Common testing setup."""

import py
import pytest

import portfel.data.loader as ldr


@pytest.fixture()
def data_path():
    """Path to the test data files."""
    return py.path.local(__file__).dirpath('data')


@pytest.fixture()
def spy_1d(data_path):
    """BATS:SPY OHLC series at 1D resolution."""
    path = data_path.join('BATS_SPY, 1D.csv').strpath
    return ldr.load_series(path, 'tradingview')


@pytest.fixture()
def alv_1d(data_path):
    """FWB:ALY OHLC series at 1D resolution."""
    path = data_path.join('FWB_DLY_ALV, 1D.csv').strpath
    return ldr.load_series(path, 'tradingview')
