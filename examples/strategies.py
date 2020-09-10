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

"""Investment strategy search.

Here we take some simple strategies like "invest X every month" or "invest Y%
of available cash every time it drops by 5%" and backtest them on index data.

For simplicity we assume 2% dividend that's paid in 4 installments at the end
of each quarter.

"""

import collections
import datetime
import os

import portfel.data.repository as r


def add_quarterly_dividends(series, div_yield):
    """Add quarterly dividends of opening price * div_yield / 4."""
    for day in series:
        t = day['time']
        if t.month in {3, 6, 9, 12} and t.day == 30:
            day['dividend'] = day['open'] * div_yield / 4


def process_orders(state, day):
    """Execute any orders that match that day."""
    remaining = []

    for order in state['orders']:
        count, price = order

        if count < -state['shares']:
            raise ValueError("Can't sell {} shares, only have {}"
                             .format(-count, state['shares']))
        if price is None:
            price = day['open']
        if count > state['cash'] / price:
            raise ValueError("Can't buy {} shares, only have money for {}"
                             .format(count, state['cash'] / price))

        if (
            count > 0 and price >= day['low'] or
            count < 0 and price <= day['high']
        ):
            state['shares'] += count
            state['cash'] -= count * price
            # print(day['time'], count, 'at', price,
            #       'cash=', state['cash'], 'shares=', state['shares'])
        else:
            remaining.append(order)

    state['orders'] = remaining


def run_strategy(strategy, series, starting_cash, monthly_cash):
    """Run strategy on the series."""
    invested_cash = starting_cash
    state = {
        'cash': starting_cash,
        'shares': 0,
        'orders': [],
    }

    for day in series:
        if day['time'].day == 1:
            state['cash'] += monthly_cash
            invested_cash += monthly_cash
        strategy(state, day['open'])
        process_orders(state, day)
        if day['dividend'] is not None:
            state['cash'] += state['shares'] * day['dividend']

    return {
        'state': state,
        'total_in': invested_cash,
        'total_out': state['shares'] * day['close'],
    }


def get_slice(series, offset, period_length):
    """Get specified slice from the series."""
    end = series[offset]['time'] + period_length
    return [
        r for r in series[offset:]
        if r['time'] <= end
    ]


def sequential_slices(series, period_length, step=1):
    """Yield all possible slices of given length in chronological order."""
    for offset in range(0, len(series), step):
        slc = get_slice(series, offset, period_length)
        yield slc
        if slc[-1] == series[-1]:
            return


def averaging_strategy(state, open_price):
    """Buy when have money."""
    if state['cash'] > 1:
        state['orders'] = [((state['cash'] - 1) / open_price, open_price)]


class BuyDipStrategy:
    """Buy when the market goes below all time high by X%."""

    hi = None  # All time high.

    def __init__(self, dip_pct, invest_pct):
        self.dip_size = dip_pct / 100.0
        self.inv_size = invest_pct / 100.0

    def __call__(self, state, open_price):
        if self.hi is None:
            state['orders'] = [((state['cash'] - 1) / open_price, open_price)]
            self.hi = open_price
        elif open_price > self.hi:
            self.hi = open_price
        if open_price < self.hi * (1 - self.dip_size):  # Dip!
            self.hi = open_price
            to_invest = state['cash'] * self.inv_size
            state['orders'] = [(to_invest / open_price, open_price)]


if __name__ == '__main__':
    # General parameters.
    DIV_YIELD = 0.02
    STARTING_CASH = 80000
    MONTHLY_CASH = 3000
    YEARS = 10
    PERIOD_LENGTH = datetime.timedelta(YEARS * 365)
    SERIES = 'BATS:SPY'
    # SERIES = 'XETR:DAX'
    # SERIES = 'TVC:SPX'
    # SERIES = 'BATS:VYM'
    # SERIES = 'BATS:AGNC'
    # SERIES = 'BATS:VNQ'

    repo_path = os.path.expanduser('~/.portfel')
    repo = r.Repository(repo_path)

    series = repo.get_series(SERIES, '1d')
    # series = series[850:]
    series = series[3878:]
    # series = series[5850:]
    # add_quarterly_dividends(series, DIV_YIELD)

    gain_distr = collections.defaultdict(int)
    asum = 0
    aprod = 1
    for slc in sequential_slices(series, PERIOD_LENGTH, step=27):
        strategy = averaging_strategy
        # strategy = BuyDipStrategy(3, 99)
        result = run_strategy(
            strategy,
            slc,
            STARTING_CASH,
            MONTHLY_CASH,
        )
        gain = result['total_out'] / result['total_in'] - 1
        print(slc[0]['time'], 'to', slc[-1]['time'],
              '{:.2%}'.format(gain),
              result['total_in'], '->', result['total_out'])

        gain_distr[round(gain, 1)] += 1
        asum += gain
        aprod *= gain + 1

    total = sum(gain_distr.values())

    mean = asum / total
    ann_mean = (1 + mean) ** (1 / YEARS) - 1
    print('mean: {:.2%}, pa: {:.2%}'.format(mean, ann_mean))

    logmean = aprod ** (1 / total) - 1
    ann_logmean = (1 + logmean) ** (1 / YEARS) - 1
    print('log-mean: {:.2%}, pa: {:.2%}'.format(logmean, ann_logmean))

    for g in sorted(gain_distr):
        pct_gain = '{:.0%}'.format(g)
        prob = int(gain_distr[g] * 100 / total)
        print('{:6}'.format(pct_gain), '*' * prob)
