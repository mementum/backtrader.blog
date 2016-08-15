
.. post:: Aug 15, 2016
   :author: mementum
   :image: 1

Stock Screening
###############

Looking for some other things I came across a question on one of the
*StackOverlow* family sites: *Quantitative Finance* aka *Quant
StackExchange*. The question:

  - `Open source software for stock screening and scanning using technical
    analysis?
    <http://quant.stackexchange.com/questions/27559/open-source-software-for-stock-screening-and-scanning-using-technical-analysis>`_

It is tagged as *Python*, so it is worth seeing if *backtrader* is up to the
task.

The Analyzer itself
-------------------

The problem seems appropriate for an easy analyzer. Although the problem just
wants those above the moving average, we'll keep extra information like the
stocks which don't meet the criteria, to make sure the grain is being actually
separated from the chaff.

.. literalinclude:: st-screener.py
   :language: python
   :lines: 30-46

.. note:: Of course one also needs ``import backtrader as bt``

That pretty much solves the problem. Analysis of the *Analyzer*:

  - Have the ``period`` as a parameter to have a flexible analyzer

  - ``start`` method

    For each *data* in the system make a *Simple Moving Average* (``SMA``) for
    it.

  - ``stop`` method

    Look which *data* (``close`` if nothing else is specified) is above its
    *sma* and store that in a *list* under the key ``over`` in the returns
    (``rets``)

      The member ``rets`` is standard in *analyzers* and happens to be a
      ``collections.OrderedDict``. Created by the base class.

    Keep the ones that doesn't meet the criteria under a key ``under``

The issue now: getting the analyzer up and running.

.. note:: We assume the code has been put in a file named ``st-screener.py``

Approach 1
----------

*backtrader* includes, since almost the beginning of time, an automated script
running called ``btrun``, which can load strategies, indicators, analyzers from
python modules, parse arguments and of course plot.

Let's do a run::

  $ btrun --format yahoo --data YHOO --data IBM --data NVDA --data TSLA --data ORCL --data AAPL --fromdate 2016-07-15 --todate 2016-08-13 --analyzer st-screener:Screener_SMA --cerebro runonce=0 --writer --nostdstats
  ===============================================================================
  Cerebro:
    -----------------------------------------------------------------------------
    - Datas:
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data0:
        - Name: YHOO
        - Timeframe: Days
        - Compression: 1
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data1:
        - Name: IBM
        - Timeframe: Days
        - Compression: 1
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data2:
        - Name: NVDA
        - Timeframe: Days
        - Compression: 1
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data3:
        - Name: TSLA
        - Timeframe: Days
        - Compression: 1
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data4:
        - Name: ORCL
        - Timeframe: Days
        - Compression: 1
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data5:
        - Name: AAPL
        - Timeframe: Days
        - Compression: 1
    -----------------------------------------------------------------------------
    - Strategies:
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Strategy:
        *************************************************************************
        - Params:
        *************************************************************************
        - Indicators:
          .......................................................................
          - SMA:
            - Lines: sma
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Params:
              - period: 10
        *************************************************************************
        - Observers:
        *************************************************************************
        - Analyzers:
          .......................................................................
          - Value:
            - Begin: 10000.0
            - End: 10000.0
          .......................................................................
          - Screener_SMA:
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Params:
              - period: 10
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Analysis:
              - over: ('ORCL', 41.09, 41.032), ('IBM', 161.95, 161.221), ('YHOO', 42.94, 39.629000000000005), ('AAPL', 108.18, 106.926), ('NVDA', 63.04, 58.327)
              - under: ('TSLA', 224.91, 228.423)

We have used a set of well known tickers:

  - ``AAPL``, ``IBM``, ``NVDA``, ``ORCL``, ``TSLA``, ``YHOO``

And the only one that happens to be under the ``10`` days *Simple Moving
Average* is ``TSLA``.

Let's try a ``50`` days period. Yes, this can also be controlled with
``btrun``. The run (output shortened)::

  $ btrun --format yahoo --data YHOO --data IBM --data NVDA --data TSLA --data ORCL --data AAPL --fromdate 2016-05-15 --todate 2016-08-13 --analyzer st-screener:Screener_SMA:period=50 --cerebro runonce=0 --writer --nostdstats
  ===============================================================================
  Cerebro:
    -----------------------------------------------------------------------------
    - Datas:
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data0:
  ...
  ...
  ...
          - Screener_SMA:
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Params:
              - period: 50
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Analysis:
              - over: ('ORCL', 41.09, 40.339), ('IBM', 161.95, 155.0356), ('YHOO', 42.94, 37.9648), ('TSLA', 224.91, 220.4784), ('AAPL', 108.18, 98.9782), ('NVDA', 63.04, 51.4746)
              - under:

Notice how the ``50`` days period has been specified in the command line:

  - ``st-screener:Screener_SMA:period=50``

    In the previous run this was ``st-screener:Screener_SMA`` and the default
    ``10`` from the code was used.

We also needed to adjust ``fromdate`` to make sure there were enough bars to
consider for the calculation of the *Simple Moving Averages*

In this case all tickers are *above* the ``50`` days moving average.

Approach 2
----------

Craft a small script (see below for the full code) to have finer control of
what we do. But the results are the same.

The core is rather small:

.. literalinclude:: st-screener.py
   :language: python
   :lines: 58-65

Being the rest about argument parsing mostly.

For ``10`` days (again shortening the output)::

  $ ./st-screener.py
  ===============================================================================
  Cerebro:
  ...
  ...
  ...
          - Screener_SMA:
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Params:
              - period: 10
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Analysis:
              - over: (u'NVDA', 63.04, 58.327), (u'AAPL', 108.18, 106.926), (u'YHOO', 42.94, 39.629000000000005), (u'IBM', 161.95, 161.221), (u'ORCL', 41.09, 41.032)
              - under: (u'TSLA', 224.91, 228.423)

Same results. So let's avoid repeating it for ``50`` days.

Concluding
----------

Both the ``btrun`` from *Approach 1* and the small script from *Approach 2* use
exactly the same *analyzer* and therefore deliver the same results.

And *backtrader* has been able to withstand yet another small challenge

Two final notes:

  - Both approaches use the built-in *writer* functionality to deliver the
    output.

    - As parameter to ``btrun`` with ``--writer``

    - As parameter to ``cerebro.run`` with ``writer=True``

  - In both cases ``runonce`` has been deactivated. This is to make sure the
    online data keeps synchronized, because the results could have different
    lengths (one of the stocks could have traded less)

Script usage
------------
::

  $ ./st-screener.py --help
  usage: st-screener.py [-h] [--tickers TICKERS] [--period PERIOD]

  SMA Stock Screener

  optional arguments:
    -h, --help         show this help message and exit
    --tickers TICKERS  Yahoo Tickers to consider, COMMA separated (default:
                       YHOO,IBM,AAPL,TSLA,ORCL,NVDA)
    --period PERIOD    SMA period (default: 10)


The full script
---------------

.. literalinclude:: st-screener.py
   :language: python
