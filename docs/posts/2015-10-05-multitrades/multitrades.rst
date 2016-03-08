
.. post:: Oct 5, 2015
   :author: mementum
   :image: 1

MultiTrades
###########

Following a request at `Tick Data and Resampling
<https://disqus.com/home/discussion/backtrader/tick_data_and_resampling/?utm_source=digest&utm_medium=email&utm_content=replies>`_
release 1.1.12.88 of ``backtrader`` support "MultiTrades", ie: the ability to
assign a ``tradeid`` to orders. This id is passed on to ``Trades`` which makes
it possible to have different categories of trades and have them simultaneously
open.

The ``tradeid`` can be specified when:

  - Calling Strategy.buy/sell/close with kwarg ``tradeid``

  - Calling Broker.buy/sell with kwarg ``tradeid``

  - Creating an Order instance with kwarg ``tradeid``

If not specified the default value is:

  - ``tradeid = 0``

To test a small script has been implemented, visualizing the result with the
implementation of a custom ``MTradeObserver`` which assigns different markers on
the plot according ``tradeid`` (for the test values 0, 1 and 2 are used)

The script supports using the three ids (0, 1, 2) or simply use 0 (default)

An execution without enabling multiple ids::

  $ ./multitrades.py --plot

With the resulting chart showing all Trades carry id ``0`` and therefore cannot
be diferentiated.

.. thumbnail:: ./multitrades-disabled.png

A second execution enables multitrades by cycling amongs 0, 1 and 2::

  $ ./multitrades.py --plot --mtrade

And now 3 different markers alternate showing each Trade can be distinguished
using the ``tradeid`` member.

.. thumbnail:: ./multitrades-enabled.png

.. note::

   ``backtrader`` tries to use models which mimic reality. Therefore "trades"
   are not calculated by the ``Broker`` instance which only takes care of
   oders.

   Trades are calculated by the Strategy.

   And hence ``tradeid`` (or something similar) may not be supported by a real
   life broker in which case manually keeping track of the unique orde id
   assigned by the broker would be needed.


Now, the code for the custom observer

.. literalinclude:: ./mtradeobserver.py
   :language: python
   :lines: 21-

The main script usage::

  $ ./multitrades.py --help
  usage: multitrades.py [-h] [--data DATA] [--fromdate FROMDATE]
                        [--todate TODATE] [--mtrade] [--period PERIOD]
                        [--onlylong] [--cash CASH] [--comm COMM] [--mult MULT]
                        [--margin MARGIN] [--stake STAKE] [--plot]
                        [--numfigs NUMFIGS]

  MultiTrades

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA, -d DATA  data to add to the system
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format
    --todate TODATE, -t TODATE
                          Starting date in YYYY-MM-DD format
    --mtrade              Activate MultiTrade Ids
    --period PERIOD       Period to apply to the Simple Moving Average
    --onlylong, -ol       Do only long operations
    --cash CASH           Starting Cash
    --comm COMM           Commission for operation
    --mult MULT           Multiplier for futures
    --margin MARGIN       Margin for each future
    --stake STAKE         Stake to apply in each operation
    --plot, -p            Plot the read data
    --numfigs NUMFIGS, -n NUMFIGS
                          Plot using numfigs figures

The code for the script.

.. literalinclude:: ./multitrades.py
   :language: python
   :lines: 21-
