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

"""Data loading dispatcher."""

import portfel.data.loaders.tradingview as tv

LOADERS = {
    'tv': tv,
}


def load_series(path, resolution='auto', format='tv', ticker='auto'):
    """Load time series from a file."""
    loader = LOADERS[format]
    return loader.load(path, resolution=resolution, ticker=ticker)
