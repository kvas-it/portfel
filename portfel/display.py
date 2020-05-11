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

"""Formatting and pretty-printing."""

import tabulate as tbl


def print_table(rows, columns=None):
    """Print a nice table with data."""
    if not rows:
        print('-- no data --')
        return

    if columns is None:
        columns = {k: k for k in rows[0].keys()}

    data = {
        name: [row[key] for row in rows]
        for name, key in columns.items()
    }

    print(tbl.tabulate(data, headers=columns.keys()))
