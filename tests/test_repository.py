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

import pandas as pd
import pytest

import portfel.data.repository as repo


def test_get_series(repo_path, alv_1d):
    repository = repo.Repository(repo_path)
    alv_1d_ = repository.get_series('FWB', 'ALV', '1d')

    assert alv_1d_.exchange == 'FWB'
    assert alv_1d_.ticker == 'ALV'
    assert alv_1d_.resolution == '1d'
    assert alv_1d_.currency == 'EUR'
    assert (alv_1d_.index == alv_1d.index).all()
    assert (alv_1d.keys() == alv_1d_.keys()).all()

    for k in alv_1d:
        col = alv_1d[k]
        col_ = alv_1d_[k]
        nulls = col.isnull()
        nulls_ = col_.isnull()
        assert (nulls == nulls_).all()
        assert (col[~nulls] == col_[~nulls_]).all()


def test_get_missing(repo_path):
    repository = repo.Repository(repo_path)
    with pytest.raises(KeyError):
        repository.get_series('BATS', 'MISSING', '1d')


def test_merge_with_existing(repo_path, spy_1d):
    """Add another part of existing series (they should be merged)."""
    repository = repo.Repository(repo_path)
    spy_1d_ = copy.deepcopy(spy_1d)
    # Move records 2 weeks into the future.
    spy_1d_.index = spy_1d_.index + pd.Timedelta(days=14)
    repository.add_series(spy_1d_)

    spy_1d = repository.get_series('BATS', 'SPY', '1d')
    assert len(spy_1d) == 29
    assert spy_1d.iloc[0]['open'] == spy_1d.iloc[10]['open']  # New 1st record.
    assert spy_1d.index[10] - spy_1d.index[0] == pd.Timedelta(days=14)

    # TODO: test merging with different field sets.
    # TODO: test merging with a hole in dates.
