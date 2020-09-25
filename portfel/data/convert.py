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

"""Converters for data loading."""

import pandas as pd


def to_float(v, allow_0=True):
    """Convert float value after loading from a CSV file."""
    if v.lower() in ['nan', '']:
        return None
    v = float(v)
    if v == 0 and not allow_0:
        return None
    return v


def to_timestamp(t):
    """Convert timestamp value."""
    if isinstance(t, int):
        return pd.Timestamp(t, unit='s')
    else:
        return pd.Timestamp(t)
