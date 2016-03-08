
.. post:: Sep 14, 2015
   :author: mementum
   :image: 1

Writers - Write it down
#######################

With the 1.1.7.88 release ``backtrader`` gets a new addition: ``writers``

This is probably long due and should have been there and the discussion in
`Issue #14 <https://github.com/mementum/backtrader/issues/14>`_ should also have
kicked started the development.

But better late than never.

The ``Writer`` implementation tries to remain in line with the other objects in
the ``backtrader`` environment

  - Get added over Cerebro
  - Provide the most resonable defaults
  - Don't force the user to do much

Of course and of much more importance is to understand what the writer actually
writes. And that is:

  - A CSV output of
      - ``datas`` added to the system (can be switched off)
      - ``strategies`` (a Strategy can have named lines)
      - ``indicators`` inside the strategies (only 1st level)
      - ``observers`` inside the strategies (only 1st level)

      Which ``indicators`` and ``observers`` output data to the CSV stream is
      controlled by the attribute:

        ``csv`` in each instance

      The defaults are:

        - Observers have ``csv = True``
        - Indicators have ``csv = False``

      The value can be overriden for any instance created inside a strategy

Once the backtesting phase is over, ``Writers`` add a new section for the
``Cerebro`` instance and the following subsections are added:

  - Properties of ``datas`` in the system (name, compression, timeframe)
  - Properties of ``strategies`` in the system (lines, params)

    - Properties of ``indicators`` in the strategies (lines, params)

    - Properties of ``observers`` in the strategies (lines, params)

    - Analyzers with the following properties

      - Params
      - Analysis

With all that in mind, an example may be the easiest way to show the power (or
weakness) or the ``writers``.

But before how to add them to cerebro.

  1. Using the ``writer`` param to ``cerebro``::

       cerebro = bt.Cerebro(writer=True)

     This creates a default instance.

  2. Specific addition::

       cerebro = bt.Cerebro()

       cerebro.addwriter(bt.WriterFile, csv=False)

     Adds (right now the only writer) a ``WriterFile`` class to the writer list
     to be later instantiated with ``csv=False`` (no csv stream will be
     generated in the output.

The long due example with a **long-short** strategy (see below for the full
code) using a Close-SMA crossover as the signal by executing::

  $ ./writer-test.py

The chart:

.. thumbnail:: ./writer-test.png

With the following output::

  ===============================================================================
  Cerebro:
    -----------------------------------------------------------------------------
    - Datas:
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data0:
        - Name: 2006-day-001
        - Timeframe: Days
        - Compression: 1
    -----------------------------------------------------------------------------
    - Strategies:
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - LongShortStrategy:
        *************************************************************************
        - Params:
          - csvcross: False
          - printout: False
          - onlylong: False
          - stake: 1
          - period: 15
        *************************************************************************
        - Indicators:
          .......................................................................
          - SMA:
            - Lines: sma
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Params:
              - period: 15
          .......................................................................
          - CrossOver:
            - Lines: crossover
            - Params: None
        *************************************************************************
        - Observers:
          .......................................................................
          - Broker:
            - Lines: cash, value
            - Params: None
          .......................................................................
          - BuySell:
            - Lines: buy, sell
            - Params: None
          .......................................................................
          - Trades:
            - Lines: pnlplus, pnlminus
            - Params: None
        *************************************************************************
        - Analyzers:
          .......................................................................
          - Value:
            - Begin: 100000
            - End: 100826.1
          .......................................................................
          - SQN:
            - Params: None
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Analysis:
              - sqn: 0.05
              - trades: 22

After the run we have a complete summary of how the system is setup and at the
end what the analzyers say. In this case the analyzers are

  - ``Value`` which is a fake analyzer inside the strategy which collects the
    starting and ending values of the portfolio

  - ``SQN`` (or SystemQualityNumber) defined by Van K. Tharp (addition to
    ``backtrader`` 1.1.7.88 which is telling us that it has seen 22 trades and
    has calculated a ``sqn`` of 0.05.

    This is actually pretty low. We could have figured it out by looking at the
    small profit after a full year (luckily the system loses no money)

The test script allows us to tune the strategy to become **long-only**::

  $ ./writer-test.py --onlylong --plot

The chart:

.. thumbnail:: ./writer-test-onlylong.png

The output being now::

  ===============================================================================
  Cerebro:
    -----------------------------------------------------------------------------
    - Datas:
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - Data0:
        - Name: 2006-day-001
        - Timeframe: Days
        - Compression: 1
    -----------------------------------------------------------------------------
    - Strategies:
      +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      - LongShortStrategy:
        *************************************************************************
        - Params:
          - csvcross: False
          - printout: False
          - onlylong: True
          - stake: 1
          - period: 15
        *************************************************************************
        - Indicators:
          .......................................................................
          - SMA:
            - Lines: sma
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Params:
              - period: 15
          .......................................................................
          - CrossOver:
            - Lines: crossover
            - Params: None
        *************************************************************************
        - Observers:
          .......................................................................
          - Broker:
            - Lines: cash, value
            - Params: None
          .......................................................................
          - BuySell:
            - Lines: buy, sell
            - Params: None
          .......................................................................
          - Trades:
            - Lines: pnlplus, pnlminus
            - Params: None
        *************************************************************************
        - Analyzers:
          .......................................................................
          - Value:
            - Begin: 100000
            - End: 102795.0
          .......................................................................
          - SQN:
            - Params: None
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            - Analysis:
              - sqn: 0.91
              - trades: 11

The changes in the "params" to the strategy can be seen (onlylong has turned to
True) and the Analyzers tell a different story:

  - Ending value improved from 100826.1 to 102795.0

  - Trades seen by SQN down to 11 from 22

  - The SQN score grows from 0.05 to 0.91 which is much much better

But still there is no CSV output to be seen. Let's run the script to turn it
on::

  $ ./writer-test.py --onlylong --writercsv

With renewed output::

  ===============================================================================
  Id,2006-day-001,len,datetime,open,high,low,close,volume,openinterest,LongShortStrategy,len,Broker,len,cash,value,Buy
  Sell,len,buy,sell,Trades,len,pnlplus,pnlminus
  1,2006-day-001,1,2006-01-02 23:59:59+00:00,3578.73,3605.95,3578.73,3604.33,0.0,0.0,LongShortStrategy,1,Broker,1,1000
  00.0,100000.0,BuySell,1,,,Trades,1,,
  2,2006-day-001,2,2006-01-03 23:59:59+00:00,3604.08,3638.42,3601.84,3614.34,0.0,0.0,LongShortStrategy,2,Broker,2,1000
  00.0,100000.0,BuySell,2,,,Trades,2,,
  ...
  ...
  ...
  255,2006-day-001,255,2006-12-29 23:59:59+00:00,4130.12,4142.01,4119.94,4119.94,0.0,0.0,LongShortStrategy,255,Broker,255,100795.0,102795.0,BuySell,255,,,Trades,255,,
  ===============================================================================
  Cerebro:
    -----------------------------------------------------------------------------
  ...
  ...

We can skip most of the csv stream and the already seen summaries. The CSV
stream has printe out the following

  - A section line separator at the beginning
  - A header row
  - The corresponding data

Note how each object gets its "length" printed. Although in this case it doesn't
offer much information, it will if multi-timeframe datas are used or data is
replayed.

The ``writer`` defaults do the following:

  - No indicators are printed (neither the Simple Moving Average nor the
    CrossOver)
  - The obsevers are printed

Let's run the script with an additional parameter to have the CrossOver
indicator added to the CSV stream::

  $ ./writer-test.py --onlylong --writercsv --csvcross

The output::

  ===============================================================================
  Id,2006-day-001,len,datetime,open,high,low,close,volume,openinterest,LongShortStrategy,len,CrossOver,len,crossover,B
  roker,len,cash,value,BuySell,len,buy,sell,Trades,len,pnlplus,pnlminus
  1,2006-day-001,1,2006-01-02 23:59:59+00:00,3578.73,3605.95,3578.73,3604.33,0.0,0.0,LongShortStrategy,1,CrossOver,1,,
  Broker,1,100000.0,100000.0,BuySell,1,,,Trades,1,,
  ...
  ...

This has shown some of the powers of the writers. Further documentation of the
class is still a to-do.

Meanwhile the execution possibilities and code used for the example.

Usage::

  $ ./writer-test.py --help
  usage: writer-test.py [-h] [--data DATA] [--fromdate FROMDATE]
                        [--todate TODATE] [--period PERIOD] [--onlylong]
                        [--writercsv] [--csvcross] [--cash CASH] [--comm COMM]
                        [--mult MULT] [--margin MARGIN] [--stake STAKE] [--plot]
                        [--numfigs NUMFIGS]

  MultiData Strategy

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA, -d DATA  data to add to the system
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format
    --todate TODATE, -t TODATE
                          Starting date in YYYY-MM-DD format
    --period PERIOD       Period to apply to the Simple Moving Average
    --onlylong, -ol       Do only long operations
    --writercsv, -wcsv    Tell the writer to produce a csv stream
    --csvcross            Output the CrossOver signals to CSV
    --cash CASH           Starting Cash
    --comm COMM           Commission for operation
    --mult MULT           Multiplier for futures
    --margin MARGIN       Margin for each future
    --stake STAKE         Stake to apply in each operation
    --plot, -p            Plot the read data
    --numfigs NUMFIGS, -n NUMFIGS
                          Plot using numfigs figures


And the test script.

.. literalinclude:: ./writer-test.py
   :language: python
   :lines: 21-
