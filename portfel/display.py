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

TABLE_FORMAT = "presto"


def print_table(data, columns=None, sort_by=None):
    """Print a nice table with data."""
    if len(data) == 0:
        print('-- no data --')
        return

    if sort_by is not None:
        data = data.sort_values(by=sort_by)
    if columns is not None:
        data = data[columns]

    print(tbl.tabulate(
        data,
        headers='keys',
        showindex=False,
        tablefmt=TABLE_FORMAT
    ))
