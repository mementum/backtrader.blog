#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015 Daniel Rodriguez
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

import time

from six.moves import xrange

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds


class OptimizeStrategy(bt.Strategy):
    params = (('smaperiod', 15),
              ('macdperiod1', 12),
              ('macdperiod2', 26),
              ('macdperiod3', 9),
              )

    def __init__(self):
        # Add indicators to add load

        btind.SMA(period=self.p.smaperiod)
        btind.MACD(period_me1=self.p.macdperiod1,
                   period_me2=self.p.macdperiod2,
                   period_signal=self.p.macdperiod3)


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro(maxcpus=None)

    # Add a strategy
    cerebro.optstrategy(
        OptimizeStrategy,
        smaperiod=xrange(5, 40),
        macdperiod1=xrange(12, 20),
        macdperiod2=xrange(26, 30),
        macdperiod3=xrange(9, 15),
    )

    # Create a Data Feed
    datapath = ('../datas/2006-day-001.txt')
    data = bt.feeds.BacktraderCSVData(dataname=datapath)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # clock the start of the process
    tstart = time.clock()

    # Run over everything
    stratruns = cerebro.run()

    # clock the end of the process
    tend = time.clock()

    print('==================================================')
    for stratrun in stratruns:
        print('**************************************************')
        for strat in stratrun:
            print('--------------------------------------------------')
            print(strat.p._getkwargs())
    print('==================================================')

    # print out the result
    print('Time used:', str(tend - tstart))
