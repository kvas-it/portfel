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

"""Tests for the Repository module."""

import pytest

import portfel.data.repository as repo


@pytest.fixture()
def repo_path(tmpdir, spy_1d):
    path = tmpdir.join('repo').strpath
    repository = repo.Repository(path)
    repository.add_series(spy_1d)
    return path


def test_get_series(repo_path):
    repository = repo.Repository(repo_path)
    spy_1d = repository.get_series('BATS:SPY', '1d')
    assert len(spy_1d) == 19
    assert spy_1d[0]['open'] == 5.54452519


def test_add_existing(repo_path, spy_1d):
    # Add an existing series: what should happen?
    pass
