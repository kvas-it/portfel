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

import copy
import datetime

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


def test_get_missing(repo_path):
    repository = repo.Repository(repo_path)
    with pytest.raises(KeyError):
        repository.get_series('MISSING', '1d')


def test_merge_with_existing(repo_path, spy_1d):
    """Add another part of existing series (they should be merged)."""
    repository = repo.Repository(repo_path)
    spy_1d_ = copy.deepcopy(spy_1d)
    plus_14d = datetime.timedelta(days=14)
    for rec in spy_1d_:
        rec['time'] += plus_14d  # Move records 2 weeks into the future.
    repository.add_series(spy_1d_)

    spy_1d = repository.get_series('BATS:SPY', '1d')
    assert len(spy_1d) == 29
    assert spy_1d[0]['open'] == spy_1d[10]['open']  # New 1st record.
    assert spy_1d[10]['time'] - spy_1d[0]['time'] == plus_14d

    # TODO: test merging with different field sets.
    # TODO: test merging with a hole in dates.
