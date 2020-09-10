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

"""Calculate the distribution of drops from the all time high."""

import collections
import os

import portfel.data.repository as r


if __name__ == '__main__':
    SERIES = 'BATS:TSLA'

    repo_path = os.path.expanduser('~/.portfel')
    repo = r.Repository(repo_path)
    series = repo.get_series(SERIES, '1d')[1200:]

    high = series[0]['high']
    low = series[0]['low']
    drop = None
    drops = []

    for day in series:
        if day['low'] < low:
            low = day['low']
            drop = (high, low)
        if day['high'] > high:
            high = day['high']
            low = day['low']  # Reset the low.
            if drop is not None:
                drops.append(drop)
                drop = None

    drop_freq = collections.defaultdict(int)

    for high, low in drops:
        mag = int(100 * (high - low) / high)
        drop_freq[mag] += 1

    print('Drops since', series[0]['time'])
    for mag in sorted(drop_freq):
        print('{:2}%'.format(mag), '*' * drop_freq[mag])
