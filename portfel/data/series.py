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

"""Time series of information on a particular security.

We subclass standard Series and DataFrame classes in order to carry around
metadata like ticker name, time resolution and currency. However, we use a
different terminology here, where the 2-dimensional array of time x values is
called Series and each 1-dimensional column of it is called Column.

"""

import pandas as pd


class Column(pd.Series):
    """One column in a vector time series."""

    _metadata = ['exchange', 'ticker', 'resolution', 'currency']

    @property
    def _constructor(self):
        return self.__class__

    @property
    def _constructor_expanddim(self):
        return Series


class Series(pd.DataFrame):
    """Multi-column time series."""

    _metadata = ['exchange', 'ticker', 'resolution', 'currency']

    def __init__(self, data, *args, **kw):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        if 'time' in data:
            data.index = data['time']
            data = data.drop(columns='time')
        super().__init__(data, *args, **kw)

    @property
    def _constructor(self):
        return self.__class__

    @property
    def _constructor_sliced(self):
        return Column
