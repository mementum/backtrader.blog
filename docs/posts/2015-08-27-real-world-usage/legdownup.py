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

import itertools
import operator

import six
from six.moves import map, xrange, zip

import backtrader as bt
import backtrader.indicators as btind
from backtrader.utils import OrderedDict


class LegDown(bt.Indicator):
    '''
    Calculates what the current legdown has been using:
      - Current low
      - High from ``period`` bars ago
    '''
    lines = ('legdown',)
    params = (('period', 10),)

    def __init__(self):
        self.lines.legdown = self.data.high(-self.p.period) - self.data.low


class LegUp(bt.Indicator):
    '''
    Calculates what the current legup has been using:
      - Current high
      - Low from ``period`` bars ago

    If param ``writeback`` is True the value will be written
    backwards ``period`` bars ago
    '''
    lines = ('legup',)
    params = (('period', 10), ('writeback', True),)

    def __init__(self):
        self.lu = self.data.high - self.data.low(-self.p.period)
        self.lines.legup = self.lu(self.p.period * self.p.writeback)


class LegDownUpAnalyzer(bt.Analyzer):
    params = (
        # If created indicators have to be plotteda along the data
        ('plotind', True),
        # period to consider for a legdown
        ('ldown', 10),
        # periods for the following legups after a legdown
        ('lups', [5, 10, 15, 20]),
        # How to sort: date-asc, date-desc, legdown-asc, legdown-desc
        ('sort', 'legdown-desc'),
    )

    sort_options = ['date-asc', 'date-des', 'legdown-desc', 'legdown-asc']

    def __init__(self):
        # Create the legdown indicator
        self.ldown = LegDown(self.data, period=self.p.ldown)
        self.ldown.plotinfo.plot = self.p.plotind

        # Create the legup indicators indicator - writeback is not touched
        # so the values will be written back the selected period and therefore
        # be aligned with the end of the legdown
        self.lups = list()
        for lup in self.p.lups:
            legup = LegUp(self.data, period=lup)
            legup.plotinfo.plot = self.p.plotind
            self.lups.append(legup)

    def nextstart(self):
        self.start = len(self.data) - 1

    def stop(self):
        # Calculate start and ending points with values
        start = self.start
        end = len(self.data)
        size = end - start

        # Prepare dates (key in the returned dictionary)
        dtnumslice = self.strategy.data.datetime.getzero(start, size)
        dtslice = map(lambda x: bt.num2date(x).date(), dtnumslice)
        keys = dtslice

        # Prepare the values, a list for each key item
        # leg down
        ldown = self.ldown.legdown.getzero(start, size)
        # as many legs up as requested
        lups = [up.legup.getzero(start, size) for up in self.lups]

        # put legs down/up together and interleave (zip)
        vals = [ldown] + lups
        zvals = zip(*vals)

        # Prepare sorting options
        if self.p.sort == 'date-asc':
            reverse, item = False, 0
        elif self.p.sort == 'date-desc':
            reverse, item = True, 0
        elif self.p.sort == 'legdown-asc':
            reverse, item = False, 1
        elif self.p.sort == 'legdown-desc':
            reverse, item = True, 1
        else:
            # Default ordering - date-asc
            reverse, item = False, 0

        # Prepare a sorted array of 2-tuples
        keyvals_sorted = sorted(zip(keys, zvals),
                                reverse=reverse,
                                key=operator.itemgetter(item))

        # Use it to build an ordereddict
        self.ret = OrderedDict(keyvals_sorted)

    def get_analysis(self):
        return self.ret

    def print(self, *args, **kwargs):
        # Overriden to change default behavior (call pprint)
        # provides a CSV printout of the legs down/up
        header_items = ['Date', 'LegDown']
        header_items.extend(['LegUp_%d' % x for x in self.p.lups])
        header_txt = ','.join(header_items)
        print(header_txt)

        for key, vals in six.iteritems(self.ret):
            keytxt = key.strftime('%Y-%m-%d')
            txt = ','.join(itertools.chain([keytxt], map(str, vals)))
            print(txt)
