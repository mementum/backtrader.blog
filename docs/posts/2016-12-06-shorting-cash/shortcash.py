#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2016 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt


class MACrossOver(bt.SignalStrategy):
    params = (('ma', bt.ind.MovAv.SMA), ('p1', 10), ('p2', 30),)

    def __init__(self):
        ma1, ma2 = self.p.ma(period=self.p.p1), self.p.ma(period=self.p.p2)
        self.signal_add(bt.SIGNAL_LONGSHORT, bt.ind.CrossOver(ma1, ma2))


def runstrat(args=None):
    args = parse_args(args)

    cerebro = bt.Cerebro()

    # Data feed
    data0 = bt.feeds.BacktraderCSVData(dataname=args.data)
    cerebro.adddata(data0)

    # Broker
    kwargs = eval('dict(' + args.broker + ')')
    cerebro.broker = bt.brokers.BackBroker(**kwargs)

    # Sizer
    kwargs = eval('dict(' + args.sizer + ')')
    cerebro.addsizer(bt.sizers.FixedSize, **kwargs)

    # Strategy
    kwargs = eval('dict(' + args.strat + ')')
    cerebro.addstrategy(MACrossOver, **kwargs)

    # better net liquidation value view
    cerebro.addobserver(bt.observers.Value)

    # Execute
    cerebro.run(**(eval('dict(' + args.cerebro + ')')))

    if args.plot:  # Plot if requested to
        cerebro.plot(**(eval('dict(' + args.plot + ')')))


def parse_args(pargs=None):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='shortcash testing ...')

    parser.add_argument('--data', default='../../datas/2005-2006-day-001.txt',
                        required=False, help='Data to read in')

    parser.add_argument('--cerebro', required=False, action='store',
                        default='', help='kwargs in key=value format')

    parser.add_argument('--broker', required=False, action='store',
                        default='', help='kwargs in key=value format')

    parser.add_argument('--sizer', required=False, action='store',
                        default='', help='kwargs in key=value format')

    parser.add_argument('--strat', required=False, action='store',
                        default='', help='kwargs in key=value format')

    parser.add_argument('--plot', '-p', nargs='?', required=False,
                        metavar='kwargs', const='{}',
                        help=('Plot the read data applying any kwargs passed\n'
                              '\n'
                              'For example:\n'
                              '\n'
                              '  --plot style="candle" (to plot candles)\n'))

    return parser.parse_args(pargs)


if __name__ == '__main__':
    runstrat()
