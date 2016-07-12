
.. post:: Jul 12, 2016
   :author: mementum
   :image: 1

Visual Chart Live Data/Trading
##############################

Starting with release *1.5.1.93*, ``backtrader`` supports Visual Chart Live
Feeds and Live Trading.

Needed things:

  - *Visual Chart 6* (this one runs on Windows)

  - ``comtypes``, specifically this fork: https://github.com/mementum/comtypes

    Install it with: ``pip install
    https://github.com/mementum/comtypes/archive/master.zip``

    The *Visual Chart* API is based on *COM* and the current ``comtypes`` main
    branch doesn't support unpacking of ``VT_ARRAYS`` of ``VT_RECORD``. And
    this is used by *Visual Chart*

    `Pull Request #104 <https://github.com/enthought/comtypes/pull/104>`_ has
    been submitted but not yet integrated. As soon as it is integrated, the
    main branch can be used.

  - ``pytz`` (optional but strongly recommended)

    In many cases the internal ``SymbolInfo.TimeOffset`` provided by the data
    feeds suffices to return data feeds in market time (even if the default
    configuration is ``LocalTime`` in *Visual Chart*)

If you don't know what's *Visual Chart* and/or its currently associated
broker *Esfera Capital*, then visit the following sites:

  - `Visual Chart <www.visualchart.com>`_
  - `Esfera Capital <www.esferacapital.es>`_

Initial statement:

  - As always and before risking your money, **TEST**, **TEST**, **TEST** and
    **RE-TEST** a thousand times.

    From *bugs* in this software, to bugs in your own software and the
    management of unexpected situations: **Anything can go wrong**

Some notes about this:

  - The data feed is rather good and supports built-in resampling. Good,
    because there is no need to do resampling.

  - The data feed doesn't support *Seconds* resolution. Not good but solvable
    by the built-in resampling of *backtrader*

  - Backfilling is built-in

  - Some on the markets in ``International Indices`` (in exchange ``096``) have
    odd timezones and market offsets.

    Some work has gone into this to for example deliver ``096.DJI`` in the
    expected ``US/Eastern`` timezone

  - The data feed offers *continuous futures* which is very handy to have a
    large history.

    As such a second parameter can be passed to a data to indicate which is the
    actual trading asset.

  - DateTime for a *Good Til Date* order can only be specified as a *date*. The
    *time* component is ignored.

  - There is no direct way to find the offset from the local equipment to the
    data server and a heuristic is needed to find this out from *RealTime
    Ticks* at the start of a session.

  - Passing a *datetime* with a *time* component (rather than the default
    *00:00:00*) seems to create a *time filter* in the *COM* API. For example
    if you say you want the *Minute* data, starting 3 days ago at *14:30*, you
    could do::

      dt = datetime.now() - timedelta(days=3)
      dt.replace(hour=14, minute=30)

      vcstore.getdata(dataname='001ES', fromdate=dt)

    Data is then skipped until *14:30* not only 3 days ago, *BUT EVERY OF THE
    DAYS AFTERWARDS*

    As such, please pass only *full dates* in the sense that the default *time*
    component is untouched.

  - The *broker* supports the notion of *Positions* but only when they are
    *open*. The last event with regards to a *Position* (which is **size is
    0**) is not sent.

    As such, *Position* accounting is done entirely by *backtrader*

  - The *broker* doesn't report commissions.

    The workaround is to supply your own ``CommissionInfo`` derived class when
    instantiating the broker. See the *backtader* docs for creating your own
    class. It is rather easy.

  - ``Cancelled`` vs ``Expired`` orders. This distinction doesn't exist and an
    heuristic would be needed to try to clear the distinction out.

    As such only ``Cancelled`` will be reported

Some additional notes:

  - *RealTime* ticks are mostly not used. They produce large amounts of
    unneeded information for *backtrader* purposes. They have 2 main purposes
    before being completely disconnected by *backtrader*

    1. Finding out if a Symbol exists.

    2. Calculating the offset to the data server

    Of course the information is gathered in realtime for prices but from
    *DataSource* objects, which provide the historical data at the same time.

As much as possible has been documented and is available at the usual
documentation link:

  - `Read The Docs <http://backtrader.readthedocs.io/en/latest/>`_

A couple of runs from the sample ``vctest.pye`` against the *Visual Chart* and
the *Demo Broker*

First: ``015ES`` (*EuroStoxx50* continuous) with resampling to 1 minute and
featuring a disconnection and reconnection::

  $ ./vctest.py --data0 015ES --timeframe Minutes --compression 1 --fromdate 2016-07-12

Output::

  --------------------------------------------------
  Strategy Created
  --------------------------------------------------
  Datetime, Open, High, Low, Close, Volume, OpenInterest, SMA
  ***** DATA NOTIF: CONNECTED
  ***** DATA NOTIF: DELAYED
  0001, 2016-07-12T08:01:00.000000, 2871.0, 2872.0, 2869.0, 2872.0, 1915.0, 0.0, nan
  0002, 2016-07-12T08:02:00.000000, 2872.0, 2872.0, 2870.0, 2871.0, 479.0, 0.0, nan
  0003, 2016-07-12T08:03:00.000000, 2871.0, 2871.0, 2869.0, 2870.0, 518.0, 0.0, nan
  0004, 2016-07-12T08:04:00.000000, 2870.0, 2871.0, 2870.0, 2871.0, 248.0, 0.0, nan
  0005, 2016-07-12T08:05:00.000000, 2870.0, 2871.0, 2870.0, 2871.0, 234.0, 0.0, 2871.0
  ...
  ...
  0639, 2016-07-12T18:39:00.000000, 2932.0, 2933.0, 2932.0, 2932.0, 1108.0, 0.0, 2932.8
  0640, 2016-07-12T18:40:00.000000, 2931.0, 2932.0, 2931.0, 2931.0, 65.0, 0.0, 2932.6
  ***** DATA NOTIF: LIVE
  0641, 2016-07-12T18:41:00.000000, 2932.0, 2932.0, 2930.0, 2930.0, 2093.0, 0.0, 2931.8
  ***** STORE NOTIF: (u'VisualChart is Disconnected', -65520)
  ***** DATA NOTIF: CONNBROKEN
  ***** STORE NOTIF: (u'VisualChart is Connected', -65521)
  ***** DATA NOTIF: CONNECTED
  ***** DATA NOTIF: DELAYED
  0642, 2016-07-12T18:42:00.000000, 2931.0, 2931.0, 2931.0, 2931.0, 137.0, 0.0, 2931.2
  0643, 2016-07-12T18:43:00.000000, 2931.0, 2931.0, 2931.0, 2931.0, 432.0, 0.0, 2931.0
  ...
  0658, 2016-07-12T18:58:00.000000, 2929.0, 2929.0, 2929.0, 2929.0, 4.0, 0.0, 2930.0
  0659, 2016-07-12T18:59:00.000000, 2929.0, 2930.0, 2929.0, 2930.0, 353.0, 0.0, 2930.0
  ***** DATA NOTIF: LIVE
  0660, 2016-07-12T19:00:00.000000, 2930.0, 2930.0, 2930.0, 2930.0, 376.0, 0.0, 2930.0
  0661, 2016-07-12T19:01:00.000000, 2929.0, 2930.0, 2929.0, 2930.0, 35.0, 0.0, 2929.8

.. note:: The execution environment has ``pytz`` installed

.. note:: Notice the absence of ``--resample``: for ``Minutes`` the resampling
	  is built-in *Visual Chart*

And finally some trading, buying *2* contract of ``015ES`` with a single
``Market`` order and selling them in 2 orders of *1* contract each.

Execution::

  $ ./vctest.py --data0 015ES --timeframe Minutes --compression 1 --fromdate 2016-07-12 2>&1 --broker --account accname --trade --stake 2

The output is rather verbose, showing all parts of the order
exeuction. Summarising a bit::

  --------------------------------------------------
  Strategy Created
  --------------------------------------------------
  Datetime, Open, High, Low, Close, Volume, OpenInterest, SMA
  ***** DATA NOTIF: CONNECTED
  ***** DATA NOTIF: DELAYED
  0001, 2016-07-12T08:01:00.000000, 2871.0, 2872.0, 2869.0, 2872.0, 1915.0, 0.0, nan
  ...
  0709, 2016-07-12T19:50:00.000000, 2929.0, 2930.0, 2929.0, 2930.0, 11.0, 0.0, 2930.4
  ***** DATA NOTIF: LIVE
  0710, 2016-07-12T19:51:00.000000, 2930.0, 2930.0, 2929.0, 2929.0, 134.0, 0.0, 2930.0
  -------------------------------------------------- ORDER BEGIN 2016-07-12 19:52:01.629000
  Ref: 1
  OrdType: 0
  OrdType: Buy
  Status: 1
  Status: Submitted
  Size: 2
  Price: None
  Price Limit: None
  ExecType: 0
  ExecType: Market
  CommInfo: <backtrader.brokers.vcbroker.VCCommInfo object at 0x000000001100CE10>
  End of Session: 736157.916655
  Info: AutoOrderedDict()
  Broker: <backtrader.brokers.vcbroker.VCBroker object at 0x000000000475D400>
  Alive: True
  -------------------------------------------------- ORDER END
  -------------------------------------------------- ORDER BEGIN 2016-07-12 19:52:01.629000
  Ref: 1
  OrdType: 0
  OrdType: Buy
  Status: 2
  Status: Accepted
  Size: 2
  Price: None
  Price Limit: None
  ExecType: 0
  ExecType: Market
  CommInfo: <backtrader.brokers.vcbroker.VCCommInfo object at 0x000000001100CE10>
  End of Session: 736157.916655
  Info: AutoOrderedDict()
  Broker: None
  Alive: True
  -------------------------------------------------- ORDER END
  -------------------------------------------------- ORDER BEGIN 2016-07-12 19:52:01.629000
  Ref: 1
  OrdType: 0
  OrdType: Buy
  Status: 4
  Status: Completed
  Size: 2
  Price: None
  Price Limit: None
  ExecType: 0
  ExecType: Market
  CommInfo: <backtrader.brokers.vcbroker.VCCommInfo object at 0x000000001100CE10>
  End of Session: 736157.916655
  Info: AutoOrderedDict()
  Broker: None
  Alive: False
  -------------------------------------------------- ORDER END
  -------------------------------------------------- TRADE BEGIN 2016-07-12 19:52:01.629000
  ref:1
  data:<backtrader.feeds.vcdata.VCData object at 0x000000000475D9E8>
  tradeid:0
  size:2.0
  price:2930.0
  value:5860.0
  commission:0.0
  pnl:0.0
  pnlcomm:0.0
  justopened:True
  isopen:True
  isclosed:0
  baropen:710
  dtopen:736157.74375
  barclose:0
  dtclose:0.0
  barlen:0
  historyon:False
  history:[]
  status:1
  -------------------------------------------------- TRADE END
  ...

The following happens:

  - Data is received as normal
  - A ``BUY`` for ``2`` with execution type ``Market`` is issued

    - ``Submitted`` and ``Accepted`` notifications are received (only
      ``Submitted`` is shown above)

    - A streak of ``Partial`` executions (only 1 shown) until ``Completed`` is
      received.

      The actual execution is not shown, but is available in the ``order``
      instance received under ``order.executed``

  - Although not shown, 2 x ``Market`` ``SELL`` orders are issued to undo the
    operation

    The screenshot shows the logs in *Visual Chart* after two different runs across an
    evening with ``015ES`` (*EuroStoxx 50*) and ``034EURUS`` (*EUR.USD Forex Pair*)

.. thumbnail:: visualchart-filled-orders.png


The sample can do much more and is intended as a thorough test of the
facilities and if possible to uncover any rough edges.

The usage::

  $ ./vctest.py --help
  usage: vctest.py [-h] [--exactbars EXACTBARS] [--plot] [--stopafter STOPAFTER]
                   [--nostore] [--qcheck QCHECK] [--no-timeoffset] --data0 DATA0
                   [--tradename TRADENAME] [--data1 DATA1] [--timezone TIMEZONE]
                   [--no-backfill_start] [--latethrough] [--historical]
                   [--fromdate FROMDATE] [--todate TODATE]
                   [--smaperiod SMAPERIOD] [--replay | --resample]
                   [--timeframe {Ticks,MicroSeconds,Seconds,Minutes,Days,Weeks,Months,Years}]
                   [--compression COMPRESSION] [--no-bar2edge] [--no-adjbartime]
                   [--no-rightedge] [--broker] [--account ACCOUNT] [--trade]
                   [--donotsell]
                   [--exectype {Market,Close,Limit,Stop,StopLimit}]
                   [--price PRICE] [--pstoplimit PSTOPLIMIT] [--stake STAKE]
                   [--valid VALID] [--cancel CANCEL]

  Test Visual Chart 6 integration

  optional arguments:
    -h, --help            show this help message and exit
    --exactbars EXACTBARS
                          exactbars level, use 0/-1/-2 to enable plotting
                          (default: 1)
    --plot                Plot if possible (default: False)
    --stopafter STOPAFTER
                          Stop after x lines of LIVE data (default: 0)
    --nostore             Do not Use the store pattern (default: False)
    --qcheck QCHECK       Timeout for periodic notification/resampling/replaying
                          check (default: 0.5)
    --no-timeoffset       Do not Use TWS/System time offset for non timestamped
                          prices and to align resampling (default: False)
    --data0 DATA0         data 0 into the system (default: None)
    --tradename TRADENAME
                          Actual Trading Name of the asset (default: None)
    --data1 DATA1         data 1 into the system (default: None)
    --timezone TIMEZONE   timezone to get time output into (pytz names)
                          (default: None)
    --historical          do only historical download (default: False)
    --fromdate FROMDATE   Starting date for historical download with format:
                          YYYY-MM-DD[THH:MM:SS] (default: None)
    --todate TODATE       End date for historical download with format: YYYY-MM-
                          DD[THH:MM:SS] (default: None)
    --smaperiod SMAPERIOD
                          Period to apply to the Simple Moving Average (default:
                          5)
    --replay              replay to chosen timeframe (default: False)
    --resample            resample to chosen timeframe (default: False)
    --timeframe {Ticks,MicroSeconds,Seconds,Minutes,Days,Weeks,Months,Years}
                          TimeFrame for Resample/Replay (default: Ticks)
    --compression COMPRESSION
                          Compression for Resample/Replay (default: 1)
    --no-bar2edge         no bar2edge for resample/replay (default: False)
    --no-adjbartime       no adjbartime for resample/replay (default: False)
    --no-rightedge        no rightedge for resample/replay (default: False)
    --broker              Use VisualChart as broker (default: False)
    --account ACCOUNT     Choose broker account (else first) (default: None)
    --trade               Do Sample Buy/Sell operations (default: False)
    --donotsell           Do not sell after a buy (default: False)
    --exectype {Market,Close,Limit,Stop,StopLimit}
                          Execution to Use when opening position (default:
                          Market)
    --price PRICE         Price in Limit orders or Stop Trigger Price (default:
                          None)
    --pstoplimit PSTOPLIMIT
                          Price for the limit in StopLimit (default: None)
    --stake STAKE         Stake to use in buy operations (default: 10)
    --valid VALID         Seconds or YYYY-MM-DD (default: None)
    --cancel CANCEL       Cancel a buy order after n bars in operation, to be
                          combined with orders like Limit (default: 0)

The code:

.. literalinclude:: ./vctest.py
   :language: python
   :lines: 21-
