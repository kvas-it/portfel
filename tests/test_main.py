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

"""Tests for the command line interface."""

import pytest

import portfel.data.repository as repo

import conftest as ct


def test_import_series(script_runner, repo_path, data_path):
    """Import BATS:SPY as FOO and compare with the original."""
    result = script_runner.run(
        'pf', 'import_series',
        '--repository', repo_path,
        '--exchange', 'FOO',
        '--ticker', 'BAR',
        '--currency', 'BAZ',
        '--resolution', '1d',
        data_path.join(ct.DataFiles.SPY_1D).strpath,
    )
    assert result.success

    repository = repo.Repository(repo_path)
    spy = repository.get_series('BATS', 'SPY', '1d')
    foo = repository.get_series('FOO', 'BAR', '1d')

    assert foo.currency == 'BAZ'
    assert list(foo) == list(spy)  # It's the same series under different name.


# Argument parsing sets defaults when __main__.py is loaded, so we have to run
# in a subprocess to be able to pass the repo via environment variable.
@pytest.mark.script_launch_mode('subprocess')
def test_list_series(script_runner, repo_env):
    result = script_runner.run(
        'pf', 'list_series',
        env=repo_env,
    )
    assert result.success
    assert '\n' + result.stdout == """
 exchange   | ticker   | resolution   | currency
------------+----------+--------------+------------
 BATS       | SPY      | 1d           | USD
 FWB        | ALV      | 1d           | EUR
"""
