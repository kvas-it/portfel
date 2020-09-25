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

import os

import py
import pytest

import portfel.data.loader as ldr
import portfel.data.repository as repo


class DataFiles:
    SPY_1D = 'BATS_SPY, 1D.csv'
    ALV_1D = 'FWB_DLY_ALV, 1D.csv'


@pytest.fixture()
def data_path():
    """Path to the test data files."""
    return py.path.local(__file__).dirpath('data')


@pytest.fixture()
def spy_1d(data_path):
    """BATS:SPY OHLC series at 1D resolution."""
    path = data_path.join(DataFiles.SPY_1D).strpath
    return ldr.load_series(path, 'tradingview')


@pytest.fixture()
def alv_1d(data_path):
    """FWB:ALY OHLC series at 1D resolution."""
    path = data_path.join(DataFiles.ALV_1D).strpath
    return ldr.load_series(path, 'tradingview')


@pytest.fixture()
def repo_path(tmpdir, spy_1d, alv_1d):
    path = tmpdir.join('repo').strpath
    repository = repo.Repository(path)
    repository.add_series(spy_1d)
    repository.add_series(alv_1d)
    return path


@pytest.fixture()
def repo_env(repo_path):
    env = dict(os.environ)
    env['PORTFEL_REPOSITORY'] = repo_path
    return env
