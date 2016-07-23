
.. post:: Jul 23, 2016
   :author: mementum
   :image: 1

*Sizers* Smart Staking
######################

Release ``1.6.4.93`` marks a major milestone in *backtrader* even if the change
in version numbering is a minor one.

*Position Sizing* is one of the things that actually set the foundation for
this project after reading `Trade Your Way To Financial Freedom
<https://www.amazon.com/Trade-Your-Way-Financial-Freedom/dp/007147871X>`_
from *Van K. Tharp*.

This is not the book in which *Van K. Tharp* details his approach to *Position
Sizing* but the topic is presented and discussed in the book. One of the
examples with regards to this had this setup

  - If not in the market, toss a coin to decide whether to enter or not

  - If already in the market, control the position with a Stop which is 2 x ATR
    and which gets updated if the price moves favorably to the taken position

The important parts about this:

  - Entering the market is random

  - The approach is tested with different *Sizing* schemes and this together
    with having a dynamic stop, makes the system profitable

And following the principles to set up your own "system" (wether
manual/automated/computerized, technical/fundamental, ...) *backtrader* was
born to one day test this scenario.

This could have been tested with any of the existing platforms, but there would
have been no fun along the way and the many challenges solved, which were not
even considered when kick-starting *backtrader*

*Sizers* were in the platform from the very beginning, but hidden because many
other things including *Live Trading* started getting in the way. But this is
now over and the *Van K. Tharp* scenario will be tested. Rather sooner than
later.

In the meantime a couple of *Sizers* for a sample test.

*Sizers* to control positioning
*******************************

The sample shows a potential use case in which *Sizers* alter the behavior of a
strategy by controlling the *sizing*. Check the docs at
*backtrader.readthedocs.io* to understand the *sizing interface*.

The 2 sizers:

  - ``LongOnly``: will return a fixed size position if the current position is 0
    and will return the same fixed size to close it if already in the market.

    .. literalinclude:: ./sizertest.py
       :language: python
       :lines: 46-59

  - ``FixedReverser``: will return a fixed size stake if not in the market and
    a doubled fixed size stake if already in the market to allow for a reversal

    .. literalinclude:: ./sizertest.py
       :language: python
       :lines: 61-68

These 2 *Sizers* will be combined with a very simple strategy.

.. literalinclude:: ./sizertest.py
   :language: python
   :lines: 31-44

Notice how the strategy uses a *Close-SMA* crossover signal to issue *buy* and
*sell* commands with an important thing to consider:

  - No check of positioning is done in the *strategy*

The same strategy as seen in the executions below changes behavior from
*long-only* to *long-short* by simply changing the *sizer* with this code in
the sample (controlled with the switch ``--longonly``)

.. literalinclude:: ./sizertest.py
   :language: python
   :lines: 90-94

Long-Only Execution
*******************

Done with the command::

  $ ./sizertest.py --longonly --plot

And this output.

.. thumbnail:: sizer-long-only.png

Long-Short Execution
********************

Done with the command::

  $ ./sizertest.py --plot

And this output.

.. thumbnail:: sizer-fixedreverser.png

Which immediate shows:

  - The number of trades has doubled

  - The cash (except at the beginning) never equals the *value* because the
    strategy is always in the market

Sample Usage
************
::

  $ ./sizertest.py --help
  usage: sizertest.py [-h] [--data0 DATA0] [--fromdate FROMDATE]
                      [--todate TODATE] [--cash CASH] [--longonly]
                      [--stake STAKE] [--period PERIOD] [--plot [kwargs]]

  Sample for sizer

  optional arguments:
    -h, --help            show this help message and exit
    --data0 DATA0         Data to be read in (default:
                          ../../datas/yhoo-1996-2015.txt)
    --fromdate FROMDATE   Starting date in YYYY-MM-DD format (default:
                          2005-01-01)
    --todate TODATE       Ending date in YYYY-MM-DD format (default: 2006-12-31)
    --cash CASH           Cash to start with (default: 50000)
    --longonly            Use the LongOnly sizer (default: False)
    --stake STAKE         Stake to pass to the sizers (default: 1)
    --period PERIOD       Period for the Simple Moving Average (default: 15)
    --plot [kwargs], -p [kwargs]
                          Plot the read data applying any kwargs passed For
                          example: --plot style="candle" (to plot candles)
                          (default: None)


The Full code
=============

.. literalinclude:: ./sizertest.py
   :language: python
   :lines: 21-
