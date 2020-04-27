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

"""Tests for Series class."""

import portfel.data.series as series


def test_save_load_rows(spy_1d, alv_1d, tmpdir):
    tmpfile = tmpdir.join('series.csv').strpath
    for s in [spy_1d, alv_1d]:
        s.save_rows(tmpfile)
        s_copy = series.Series(s.ticker, s.resolution, s.currency, s.source)
        s_copy.load_rows(tmpfile)

        assert s_copy == s
