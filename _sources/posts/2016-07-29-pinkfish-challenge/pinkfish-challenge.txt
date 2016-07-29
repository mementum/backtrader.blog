
.. post:: Jul 29, 2016
   :author: mementum
   :image: 1

Pinkfish Challenge
##################

(Sample and changes added to release ``1.7.1.93``)

Along the way *backtrader* has gotten maturity, new features and of course
complexity. Many of the new features have been introduced after requests,
comments, questions from users. Small challenges which have proven that most of
the design decisions were at least not that wrong even if some things could
have been done in many other ways, sometimes probably in a better way.

As such it seems that those small challenges are pushes to test the flexibility
and adaptability of the platform to new unplanned and unpexpected situations
and the *pinkfish* challenge is yet another one. *pinkfish* is another Python
backtesting framework (listed in the ``README``) which can be found under:
`pinkfish <http://fja05680.github.io/pinkfish/>`_. The site contains what has
been the challenge to solve:

  - *'buying on the close' on the SAME day a 'new 20 day high is set' were not
    allowed*

One of the *features* gives a hint as how the platform operates for such a
feat:

  - *uses daily data (vs minute or tick data) for intraday trading*

The author was additionally *put off* by the complexity of the, back then, of
the existing backtesting libraries. Whether that holds true for *backtrader*
(in its infancy back then) is a question to be answered by the *pinkfish*
author himself.

No mod solution
***************

*backtrader* supports filters for data feeds and one existed that allows
 breaking a *daily bar* in 2 parts to let people buy after having seen only the
 opening price. The 2nd part of the day (high, low, close) is evaluated in a
 2nd tick. This effectively achieves the *uses daily data (vs minute or tick
 data) for intraday trading*.

This filter tries to make a complete *replay* action without involving the
built-in replayer.

An obvious evolution of this filter breaks the daily bar in 2 bars with an
(open, high, low) first and then a 2nd complete bar (open, high, low, close).

The *buying on the close* is achieved by issuing an order with
``backtrader.Order.Close`` as execution type.

This is in the sample available with ``-no-replay``. An execution::

  $ ./pinkfish-challenge.py --no-replay

Part of the output::

  ...
  0955,0478,0478,2006-11-22T00:00:00,27.51,28.56,27.29,28.49,16027900.00,0.00
  High 28.56 > Highest 28.56
  LAST 19 highs: array('d', [25.33, 25.6, 26.4, 26.7, 26.62, 26.6, 26.7, 26.7, 27.15, 27.25, 27.65, 27.5, 27.62,   27.5, 27.5, 27.33, 27.05, 27.04, 27.34])
  -- BUY on date: 2006-11-22
  -- BUY Completed on: 2006-11-22
  -- BUY Price: 28.49
  0956,0478,0478,2006-11-22T23:59:59.999989,27.51,28.56,27.29,28.49,32055800.00,0.00
  ...

It works ...

  - After seeing the 1st part of the day (Line: ``0955``)
  - If a new 20 day high is in place a ``Close`` order is issued
  - And the order gets executed with the *closing* price of the 2nd part of the
    day (Line: ``0956``)

    The closing price is ``28.49`` which is the *BUY Price* seen in
    ``notify_order`` in the strategy

The output contains rather verbose parts simply for identification of the last
``20`` highs. The sample sells also very quickly, to let the behavior be tested
several times. But the holding period can be altered with ``--sellafter N``,
where ``N`` is the number of bars to hold before cancelling (see *Usage* at the
end)


The problem with the ``no mod`` solution
========================================

This is not really a **replay** solution and this can be seen if the *execution
type* of the order is changed from ``Close`` to ``Market``. A new execution::

  $ ./pinkfish-challenge.py --no-replay --market

Now the output for the same period as above::

  ...
  0955,0478,0478,2006-11-22T00:00:00,27.51,28.56,27.29,28.49,16027900.00,0.00
  High 28.56 > Highest 28.56
  LAST 19 highs: array('d', [25.33, 25.6, 26.4, 26.7, 26.62, 26.6, 26.7, 26.7, 27.15, 27.25, 27.65, 27.5, 27.62, 27.5, 27.5, 27.33, 27.05, 27.04, 27.34])
  -- BUY on date: 2006-11-22
  -- BUY Completed on: 2006-11-22
  -- BUY Price: 27.51
  0956,0478,0478,2006-11-22T23:59:59.999989,27.51,28.56,27.29,28.49,32055800.00,0.00
  ...

And the problem can be easily identified

  - Instead of the *closing* price the order is executing with the *opening*
    price, because the *Market* order takes the 1st price available in the 2nd
    bar, namely ``27.51``, which is unfortunately the *opening* price of the
    day and no longer *available*.

    This is due to the fact that the filter is not really *replaying* but
    rather breaking up the bar in two parts and doing a soft *replaying*


The right "mod" solution
************************

Getting also the ``Market`` order to pick the *closing* price.

This comprises:

  - A filter which breaks the bar in two parts

  - And is compatible with the standard *replay* functionality available in *backtrader*

    In this case the 2nd bar would be made up of just the ``close`` price and
    even if the display shows a complete bar, the internal machinery only
    matches orders against the *tick*

Chaining filters in *backtrader* was already possible but this use case had not
been taken into account:

  - Made 2 data "heartbeats" out of a single data "heartbeat"

    Before this challenge it was about getting bars *merged* into larger bars.

A small extension into the core mechanism loading bars allows for a filter to
add the 2nd part of the bar to an internal stash for re-processing before a new
data *heartbeat* is taken into account. And because it is an *extension* and
not a *modification* it has no impact.

The challenge has also given the chance to:

  - Look again into the early-age code written at the very beginning of
    *backtrader* for ``Close`` orders.

    And here a couple of lines and ``if`` conditions have been reworked to make
    matching ``Close`` orders more logical and if possible to deliver them
    instantly to the system (before the delivery of matching would mostly be
    done with a 1-bar delay, even if matched to the right bar)

One good thing after these changes:

  - The logic in the filter is a lot easier, because there is no subtle
    *replay* attempt. Replay is done by the *replay* filter.

The anatomy of the filter for the 1st part of the broken bar:

  #. Copy the incoming data bar
  #. Make a copy as the *OHL* bar (no Close)
  #. Change the time to be *date* + *sessionstart* time
  #. Remove part of the volume (specified with parameter *closevol* to the
     filter)
  #. Nullify ``OpenInterest`` (available at the end of the day)
  #. Remove the ``close`` price and replace it with the average of *OHL*
  #. Add the bar to the internal *stack* for immediate processing by the next
     filter or strategy (the *replay* filter will take over)

The anatomy for the 2nd part of the broken bar:

  #. Copy the incoming data bar
  #. Replace OHL prices with the ``Close`` price
  #. Change the time to be *date* + *sessionend* time
  #. Remove the other part of the volume (specified with parameter *closevol*
     to the filter)
  #. Set ``OpenInterest``
  #. Add the bar to the internal *stash* for delayed processing as the next
     data heartbeat, rather than fetching prices from the data

The code:

.. literalinclude:: ./pinkfish-challenge.py
   :language: python
   :lines: 131-167

Executing without disabling *replay* and ``Close`` (let's add plotting)::

  $ ./pinkfish-challenge.py --plot

The output for the same period::

  ...
  0955,0478,0478,2006-11-22T00:00:00,27.51,28.56,27.29,27.79,16027900.00,0.00
  High 28.56 > Highest 28.56
  LAST 19 highs: array('d', [25.33, 25.6, 26.4, 26.7, 26.62, 26.6, 26.7, 26.7, 27.15, 27.25, 27.65, 27.5, 27.62, 27.5, 27.5, 27.33, 27.05, 27.04, 27.34])
  -- BUY on date: 2006-11-22
  -- BUY Completed on: 2006-11-22
  -- BUY Price: 28.49
  0956,0478,0478,2006-11-22T23:59:59.999989,27.51,28.56,27.29,28.49,32055800.00,0.00
  ...

Everything is ok and the *closing* price of ``28.49`` has been taken.

And the chart.

.. thumbnail:: pinkfish-challenge.png

And last but not least to check the modifications have made sense::

  $ ./pinkfish-challenge.py --market

The output for the same period::

  ...
  0955,0478,0478,2006-11-22T00:00:00,27.51,28.56,27.29,27.79,16027900.00,0.00
  High 28.56 > Highest 28.56
  LAST 19 highs: array('d', [25.33, 25.6, 26.4, 26.7, 26.62, 26.6, 26.7, 26.7, 27.15, 27.25, 27.65, 27.5, 27.62, 27.5, 27.5, 27.33, 27.05, 27.04, 27.34])
  -- BUY on date: 2006-11-22
  -- BUY Completed on: 2006-11-22
  -- BUY Price: 28.49
  0956,0478,0478,2006-11-22T23:59:59.999989,27.51,28.56,27.29,28.49,32055800.00,0.00
  ..

And now the ``Market`` orders are picking the same price of ``28.49`` as the
``Close`` orders, which in this particular use case was the expectation,
because *replaying* is happening and the 2nd part of the broken daily bar has a
single *tick*: ``28.49`` which is the *closing* price

Usage of the sample
*******************
::

  $ ./pinkfish-challenge.py --help
  usage: pinkfish-challenge.py [-h] [--data DATA] [--fromdate FROMDATE]
                               [--todate TODATE] [--cash CASH]
                               [--sellafter SELLAFTER] [--highperiod HIGHPERIOD]
                               [--no-replay] [--market] [--oldbuysell]
                               [--plot [kwargs]]

  Sample for pinkfish challenge

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA           Data to be read in (default:
                          ../../datas/yhoo-1996-2015.txt)
    --fromdate FROMDATE   Starting date in YYYY-MM-DD format (default:
                          2005-01-01)
    --todate TODATE       Ending date in YYYY-MM-DD format (default: 2006-12-31)
    --cash CASH           Cash to start with (default: 50000)
    --sellafter SELLAFTER
                          Sell after so many bars in market (default: 2)
    --highperiod HIGHPERIOD
                          Period to look for the highest (default: 20)
    --no-replay           Use Replay + replay filter (default: False)
    --market              Use Market exec instead of Close (default: False)
    --oldbuysell          Old buysell plot behavior - ON THE PRICE (default:
                          False)
    --plot [kwargs], -p [kwargs]
                          Plot the read data applying any kwargs passed For
                          example (escape the quotes if needed): --plot
                          style="candle" (to plot candles) (default: None)

And the code itself
*******************

.. literalinclude:: ./pinkfish-challenge.py
   :language: python
   :lines: 21-
