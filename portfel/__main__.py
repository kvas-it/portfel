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

"""CLI entry point."""

import argparse
import logging
import os
import sys

import portfel.data.loader as ldr
import portfel.data.repository as repo

__all__ = ['main']

parser = argparse.ArgumentParser(description='Portfolio management tool')
subparsers = parser.add_subparsers(help='sub-command help')


def command(*args, **kw):
    """Return a decorator for command functions.

    This decorator will create a subparser for the command function passing
    all the arguments of `command()` to `.add_parser()`. If no name and help
    are provided for the command, they will be taken from the function name
    and docstring (only the first line of the docstring is used) of the
    decorated function.

    """

    def decorator(func):
        nonlocal args, kw

        if not args:
            args = [func.__name__]
        if 'help' not in kw:
            kw['help'] = func.__doc__.split('\n')[0]

        cmd = subparsers.add_parser(*args, **kw)
        for arg in reversed(getattr(func, '__args__', [])):
            cmd.add_argument(*arg['args'], **arg['kw'])
        cmd.set_defaults(func=func)

        return func

    return decorator


def arg(*args, **kw):
    """Return a decorator that will add an argument to a command function.

    All parameters passed to the decorator will be passed to `.add_argument()`
    call of the subparser corresponding to the decorated function.

    """

    def decorator(func):
        nonlocal args, kw

        if not hasattr(func, '__args__'):
            func.__args__ = []
        func.__args__.append({'args': args, 'kw': kw})

        return func

    return decorator


def verbose_arg():
    """Return a decorator for --verbose option."""
    return arg('--verbose', '-v', action='count', default=0,
               help='Increase verbosity')


def repository_arg():
    """Return a decorator for --repository option."""
    default = os.getenv('PORTFEL_REPOSITORY', os.path.expanduser('~/.portfel'))
    return arg('--repository', '-y', default=default, type=repo.open,
               help='Data repository (default: {})'.format(default))


@command(aliases=['imps'])
@arg('source', help='Source data file')
@arg('--format', '-f', default='tv', type=str,
     help='File format (default: tv)')
@arg('--resolution', '-r', default='auto', type=str,
     help='Time series resolution (default: autodetect)')
@arg('--ticker', '-t', default='auto', type=str,
     help='Exchange ticker, e.g. BATS:SPY (default: autodetect)')
@repository_arg()
@verbose_arg()
def import_series(args):
    """Import time series data."""
    kw = {
        'resolution': args.resolution,
        'format': args.format,

    }
    if args.ticker != 'auto':
        kw['ticker'] = args.ticker

    series = ldr.load_series(
        args.source,
        format=args.format,
        resolution=args.resolution,
        ticker=args.ticker,
    )
    args.repository.add(series)


def _configure_logging(args):
    """Configure logging."""
    verbosity = getattr(args, 'verbose', 0)

    if verbosity == 1:
        log_level = logging.INFO
    elif verbosity >= 2:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING

    logging.basicConfig(stream=sys.stderr, level=log_level,
                        format='%(message)s')


def main():
    """Run the CLI."""
    args = parser.parse_args()
    if callable(getattr(args, 'func', None)):
        _configure_logging(args)
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)
