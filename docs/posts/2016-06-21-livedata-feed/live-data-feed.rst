
.. post:: Jun 21, 2016
   :author: mementum
   :image: 1
   :excerpt: 3

Live Data/Live Trading
######################

Starting with release *1.5.0*, `backtrader` supports Live Data Feeds and Live
Trading. The first integrated entity is:

  - *Interactive Brokers*

This was long sought goal since the inception of the platform as a small
idea. The design ideas have proven to be flexible enough to accommodate the
needed changes. All whilst keeping the same interface which means: *backtest
once, trade many times*. The same code/api/primitives/notifications are meant
for *backtesting* and *live data feeding/trading*.

Naming the platform ``back`` + ``trader`` was intentional, although it could
have well been that it had remained as a pure backtester. But no longer.

What's new changed:

  - *Store* concept to have a integrated concept for entities like *Interactive
    Brokers* which provide *data* and *brokering* facilities in one go

  - New notifications to the *strategy* and/or *cerebro* from the *store*
    and/or *data feeds*

  - Time management support ... as one could be trading New York baed products
    from anywhere else and time has to be kept consistent

  - Work on Resampling/Replaying to deliver bars as soon as possible or not too
    late if the market is not trading (nobody wants a 5 second resampled bar
    received 30 seconds later, because there were no intervening ticks)

  - Of course many small internal changes

A great deal of testing has gone into the integration and a large sample called
``ibtest`` is integrated in the sources, but being this the 1st release there
could still be some edges. Should you decide to give this a try, execute 1st
against **Paper Trading** account provided by *Interactive Brokers* (usually
running at port ``7497`` rather than ``7496``)

.. note::
   Be sure to be comfortable with the inherent risks associated with data
   disconnection, bugs present in the software (*TWS* and *backtrader*), bugs
   in your own software and monitor your activities.

   ``backtrader`` cannot take any responsibility or be held responsible for any
   losses a trader may incur (it will also not take any of the winnings)

What's supported from *Interactive Brokers*:

  - Indices (obviously not for trading), Stocks, Futures, Options, Futures
    Options and Forex

  - Backfilling at the start of a connection and after a reconnection

  - Notifications on change from live to backfilling and viceversa

  - The order types already existing in *backtrader*: ``Market``, ``Limit``,
    ``StopLimit`` and ``Close`` (aka *Market on Close**)

It is not the intention of the platform to reinvent the wheel, so the following
is needed/optional to use the *Interactive Brokers* facilities:

  - Required: ``IbPy`` to interface with *Interative Brokers' TWS*

    The documentation for *IB* indicates how to install it if not already part
    of your arsenal

  - Optional: ``pytz`` to automatically set the timezone for the products.

    The end-user may provide other ``tzinfo`` -compatible  instances (from
    ``pytz`` or home-cooked) directly as a parameter to the data source rather
    than relying on automatic determination. See *Time Management* in the docs
    and the *IB* specific part of the documents.

  .. note::
     If no ``pytz`` is detected and no ``tzinfo`` compatible instance is
     supplied to the *data feed*, the time delivered by the platform will be
     ``UTC``

As much as possible has been documented and is available at the usual
documentation link:

  - `Read The Docs <http://backtrader.readthedocs.io/en/latest/>`_

A couple of runs from the sample ``ibtest`` against the *TWS Demo*

First: ``TWTR`` with resampling to 5 seconds::

  $ ./ibtest.py --port 7497 --data0 TWTR --resample --timeframe Seconds --compression 5

Output::

  Server Version: 76
  TWS Time at connection:20160620 22:37:37 CET
  --------------------------------------------------
  Strategy Created
  --------------------------------------------------
  Timezone from ContractDetails: EST5EDT
  Datetime, Open, High, Low, Close, Volume, OpenInterest, SMA
  ***** STORE NOTIF: <error id=-1, errorCode=2104, errorMsg=Market data farm connection is OK:ibdemo>
  ***** STORE NOTIF: <error id=-1, errorCode=2106, errorMsg=HMDS data farm connection is OK:demohmds>
  ***** DATA NOTIF: CONNECTED
  0001, 2016-06-20T14:37:35.000000, 15.96, 15.97, 15.96, 15.96, 0.0, 0, nan
  ***** DATA NOTIF: DELAYED
  0002, 2016-06-20T14:37:40.000000, 15.96, 15.97, 15.96, 15.96, 0.0, 0, nan
  0003, 2016-06-20T14:37:45.000000, 15.96, 15.97, 15.96, 15.97, 0.0, 0, nan
  0004, 2016-06-20T14:37:50.000000, 15.96, 15.98, 15.94, 15.94, 0.0, 0, nan
  0005, 2016-06-20T14:37:55.000000, 15.97, 15.97, 15.96, 15.97, 0.0, 0, 15.96
  ...
  1441, 2016-06-20T16:37:35.000000, 16.03, 16.03, 16.02, 16.03, 0.0, 0, 16.026
  1442, 2016-06-20T16:37:40.000000, 16.11, 16.11, 16.11, 16.11, 2.0, 0, 16.044
  ***** DATA NOTIF: LIVE
  1443, 2016-06-20T16:37:45.000000, 16.1, 16.11, 16.1, 16.11, 5.0, 0, 16.06
  1444, 2016-06-20T16:37:50.000000, 16.11, 16.11, 16.1, 16.1, 14.0, 0, 16.076
  ...

.. note:: The execution environment has ``pytz`` installed

The following can be observed:

  - The 1st lines (from ``IbPy`` itself) show the connection to the server has
    succeeded and the data feed has found out the operating timezone of the
    asset: ``EST5EDT`` (aka ``EST`` aka ``US/Eastern``)

    Notice how the local time (in timezone ``CET`` aka ``Europe/Berlin``) is
    reported by *TWS* at the beginning, but the asset is ``6`` hours behind.

    The asset is reported in the time of the trading venue. Check the docs if
    you thing you really want to change this and the reasoning for this behavior.

  - Some notifications from the *Store*, in this case *TWS* indicates that the
    connections to the different data farms is ok. This is being printed out by
    methods overriden in the *Strategy*

  - **DATA NOTIFICATIONS** like

      - ``CONNECTED``: to tell the strategy connection to *TWS* is available

      - ``DELAYED``: the data to be received is NOT live data. Backfilling
	(historical data) is taking place.

	Because the resampling parameters are *Seconds/5* the maximum number of
	5 seconds bar fitting in a single request is downloaded, roughly 1440.

      - ``LIVE``: as soon as the platform catches up with backfilling and the
	queue is reduced to live data, the notification tells the strategy
	about it.

	From bar 1443 onwards the data is real-time data.

	.. note:: because resampling is taking place this data is NOT tick-data
		  and is delivered at the end of the 5 second period. Please
		  check the docs for the ``qcheck`` parameter docs in
		  ``IBData`` to understand how quickly a resampled bar will be
		  delayed if no new ticks are being sent by the platform
		  (because with no new ticks, the platform cannot understand if
		  the currently resampled bar is yet over or not)

Let's do the same but forcing a disconnection (the network interface is
disabled 20 seconds)::

  $ ./ibtest.py --port 7497 --data0 TWTR --resample --timeframe Seconds --compression 5

Output (skipping the initial known part)::

  ...
  1440, 2016-06-20T18:16:20.000000, 16.05, 16.05, 16.04, 16.04, 0.0, 0, 16.048
  1441, 2016-06-20T18:16:25.000000, 16.05, 16.05, 16.05, 16.05, 0.0, 0, 16.05
  ***** DATA NOTIF: LIVE
  1442, 2016-06-20T18:16:30.000000, 15.9, 15.9, 15.89, 15.9, 11.0, 0, 16.02
  ***** STORE NOTIF: <error id=-1, errorCode=1100, errorMsg=Connectivity between IB and TWS has been lost.>
  ***** STORE NOTIF: <error id=-1, errorCode=2105, errorMsg=HMDS data farm connection is broken:demohmds>
  ***** STORE NOTIF: <error id=-1, errorCode=2103, errorMsg=Market data farm connection is broken:ibdemo>
  1443, 2016-06-20T18:16:35.000000, 15.9, 15.9, 15.89, 15.9, 28.0, 0, 15.988
  ***** STORE NOTIF: <error id=-1, errorCode=1102, errorMsg=Connectivity between IB and TWS has been restored - data maintained.>
  ***** STORE NOTIF: <error id=-1, errorCode=2106, errorMsg=HMDS data farm connection is OK:demohmds>
  ***** STORE NOTIF: <error id=-1, errorCode=2104, errorMsg=Market data farm connection is OK:ibdemo>
  ***** DATA NOTIF: DELAYED
  1444, 2016-06-20T18:16:40.000000, 16.04, 16.04, 16.03, 16.04, 0.0, 0, 15.986
  1445, 2016-06-20T18:16:45.000000, 16.03, 16.04, 16.03, 16.04, 0.0, 0, 15.986
  1446, 2016-06-20T18:16:50.000000, 16.04, 16.04, 16.03, 16.03, 0.0, 0, 15.982
  1447, 2016-06-20T18:16:55.000000, 16.04, 16.04, 16.03, 16.04, 0.0, 0, 16.01
  1448, 2016-06-20T18:17:00.000000, 16.03, 16.04, 16.03, 16.04, 0.0, 0, 16.038
  1449, 2016-06-20T18:17:05.000000, 16.03, 16.04, 16.02, 16.03, 0.0, 0, 16.036
  1450, 2016-06-20T18:17:10.000000, 15.9, 15.91, 15.9, 15.91, 3.0, 0, 16.01
  ***** DATA NOTIF: LIVE
  1451, 2016-06-20T18:17:15.000000, 15.92, 15.92, 15.9, 15.92, 9.0, 0, 15.988
  1452, 2016-06-20T18:17:20.000000, 15.91, 15.91, 15.89, 15.89, 18.0, 0, 15.958
  1453, 2016-06-20T18:17:25.000000, 15.89, 15.92, 15.89, 15.89, 24.0, 0, 15.928
  ...

The narrative:

  - After bar 1442, the WLAN interface has been disabled
  - TWS notifications arrive indicating the situation
  - Bar 1443 is delivered from the resampler, because the platform had some
    ticks in between ``18:16:30.000000`` and ``18:16:35.000000``

  - Connectivity is restored at around ``18:17:15``, but this data is not
    delivered at once

  - The situation is identified and *backfilling* is attempted between
    ``18:16:35`` and ``18:17:15``.

    This can be seen with the notification ``DELAYED``. The data is no longer ``LIVE``

  - Bars 1444 to 1450 (both incl.) deliver the missing time

  - The notification ``LIVE`` is received and bar 1451 contains a real-time
    packet

.. note::
   There are some situations which ``backtrader`` cannot overcome, because
   **TWS** does not oblige. If TCP/IP packets are somehow lost and the *IB*
   Server is slow to react, it will take *TWS* a long time to react and notify
   the loss of connectivity.

   *TWS* will even deliver packets clearly received late from the server with
   current timestamps (identified through a sudden burst of packets)

And finally some trading, buying *20K* shares of ``TWTR`` with a single
``Market`` order and selling them in 2 orders of *10K* each.

Execution::

  ./ibtest.py --port 7497 --data0 TWTR --resample --timeframe Seconds --compression 5 --broker --trade --stake 20000

The output is rather verbose, showing all parts of the order
exeuction. Summarising a bit::

  ...
  ***** DATA NOTIF: LIVE
  1442, 2016-06-20T18:28:05.000000, 15.92, 15.93, 15.92, 15.93, 1748.0, 0, 16.03
  -------------------------------------------------- ORDER BEGIN 2016-06-20 23:28:11.343000
  Ref: 1
  OrdType: 0
  OrdType: Buy
  Status: 1
  Status: Submitted
  Size: 20000
  Price: 14.34
  Price Limit: None
  ExecType: 0
  ExecType: Market
  CommInfo: <backtrader.brokers.ibbroker.IBCommInfo object at 0x00000000040B9278>
  End of Session: 736136.166655
  Info: AutoOrderedDict()
  Broker: <backtrader.brokers.ibbroker.IBBroker object at 0x0000000003E23470>
  Alive: True
  Ref: 1
  orderId: 1
  Action: BUY
  Size (ib): 20000
  Lmt Price: 0.0
  Aux Price: 0.0
  OrderType: MKT
  Tif (Time in Force): GTC
  GoodTillDate:
  -------------------------------------------------- ORDER END
  ...
  1443, 2016-06-20T18:28:10.000000, 15.93, 15.93, 15.92, 15.92, 10.0, 0, 16.004
  -------------------------------------------------- ORDER BEGIN 2016-06-20 23:28:15.924000
  Ref: 1
  OrdType: 0
  OrdType: Buy
  Status: 3
  Status: Partial
  Size: 20000
  Price: 14.34
  Price Limit: None
  ExecType: 0
  ExecType: Market
  CommInfo: <backtrader.brokers.ibbroker.IBCommInfo object at 0x00000000040B9278>
  End of Session: 736136.166655
  Info: AutoOrderedDict()
  Broker: <backtrader.brokers.ibbroker.IBBroker object at 0x0000000003E23470>
  Alive: True
  Ref: 1
  orderId: 1
  Action: BUY
  Size (ib): 20000
  Lmt Price: 0.0
  Aux Price: 0.0
  OrderType: MKT
  Tif (Time in Force): GTC
  GoodTillDate:
  -------------------------------------------------- ORDER END
  ...
  -------------------------------------------------- ORDER BEGIN 2016-06-20 23:28:20.972000
  Ref: 1
  OrdType: 0
  OrdType: Buy
  Status: 4
  Status: Completed
  Size: 20000
  Price: 14.34
  Price Limit: None
  ExecType: 0
  ExecType: Market
  CommInfo: <backtrader.brokers.ibbroker.IBCommInfo object at 0x00000000040B9278>
  End of Session: 736136.166655
  Info: AutoOrderedDict()
  Broker: <backtrader.brokers.ibbroker.IBBroker object at 0x0000000003E23470>
  Alive: False
  Ref: 1
  orderId: 1
  Action: BUY
  Size (ib): 20000
  Lmt Price: 0.0
  Aux Price: 0.0
  OrderType: MKT
  Tif (Time in Force): GTC
  GoodTillDate:
  -------------------------------------------------- ORDER END
  1445, 2016-06-20T18:28:20.000000, 15.92, 15.93, 15.92, 15.93, 21.0, 0, 15.954
  ...

The following happens:

  - Data is received as normal
  - A ``BUY`` for ``20K`` with execution type ``Market`` is issued

    - ``Submitted`` and ``Accepted`` notifications are received (only
      ``Submitted`` is shown above)

    - A streak of ``Partial`` executions (only 1 shown) until ``Completed`` is
      received.

      The actual execution is not shown, but is available in the ``order``
      instance received under ``order.executed``

  - Although not shown, 2 x ``Market`` ``SELL`` orders are issued to undo the
    operation

    The screenshot shows the logs in *TWS* after two different runs across an
    evening

.. thumbnail:: ibtest-twtr-execution.png


The sample can do much more and is intended as a thorough test of the
facilities and if possible to uncover any rough edges.

The usage::

  $ ./ibtest.py --help
  usage: ibtest.py [-h] [--exactbars EXACTBARS] [--plot] [--stopafter STOPAFTER]
                   [--usestore] [--notifyall] [--debug] [--host HOST]
                   [--qcheck QCHECK] [--port PORT] [--clientId CLIENTID]
                   [--no-timeoffset] [--reconnect RECONNECT] [--timeout TIMEOUT]
                   --data0 DATA0 [--data1 DATA1] [--timezone TIMEZONE]
                   [--what WHAT] [--no-backfill_start] [--latethrough]
                   [--no-backfill] [--rtbar] [--historical]
                   [--fromdate FROMDATE] [--smaperiod SMAPERIOD]
                   [--replay | --resample]
                   [--timeframe {Ticks,MicroSeconds,Seconds,Minutes,Days,Weeks,Months,Years}]
                   [--compression COMPRESSION] [--no-takelate] [--no-bar2edge]
                   [--no-adjbartime] [--no-rightedge] [--broker] [--trade]
                   [--donotsell]
                   [--exectype {Market,Close,Limit,Stop,StopLimit}]
                   [--stake STAKE] [--valid VALID] [--cancel CANCEL]

  Test Interactive Brokers integration

  optional arguments:
    -h, --help            show this help message and exit
    --exactbars EXACTBARS
                          exactbars level, use 0/-1/-2 to enable plotting
                          (default: 1)
    --plot                Plot if possible (default: False)
    --stopafter STOPAFTER
                          Stop after x lines of LIVE data (default: 0)
    --usestore            Use the store pattern (default: False)
    --notifyall           Notify all messages to strategy as store notifs
                          (default: False)
    --debug               Display all info received form IB (default: False)
    --host HOST           Host for the Interactive Brokers TWS Connection
                          (default: 127.0.0.1)
    --qcheck QCHECK       Timeout for periodic notification/resampling/replaying
                          check (default: 0.5)
    --port PORT           Port for the Interactive Brokers TWS Connection
                          (default: 7496)
    --clientId CLIENTID   Client Id to connect to TWS (default: random)
                          (default: None)
    --no-timeoffset       Do not Use TWS/System time offset for non timestamped
                          prices and to align resampling (default: False)
    --reconnect RECONNECT
                          Number of recconnection attempts to TWS (default: 3)
    --timeout TIMEOUT     Timeout between reconnection attempts to TWS (default:
                          3.0)
    --data0 DATA0         data 0 into the system (default: None)
    --data1 DATA1         data 1 into the system (default: None)
    --timezone TIMEZONE   timezone to get time output into (pytz names)
                          (default: None)
    --what WHAT           specific price type for historical requests (default:
                          None)
    --no-backfill_start   Disable backfilling at the start (default: False)
    --latethrough         if resampling replaying, adjusting time and disabling
                          time offset, let late samples through (default: False)
    --no-backfill         Disable backfilling after a disconnection (default:
                          False)
    --rtbar               Use 5 seconds real time bar updates if possible
                          (default: False)
    --historical          do only historical download (default: False)
    --fromdate FROMDATE   Starting date for historical download with format:
                          YYYY-MM-DD[THH:MM:SS] (default: None)
    --smaperiod SMAPERIOD
                          Period to apply to the Simple Moving Average (default:
                          5)
    --replay              replay to chosen timeframe (default: False)
    --resample            resample to chosen timeframe (default: False)
    --timeframe {Ticks,MicroSeconds,Seconds,Minutes,Days,Weeks,Months,Years}
                          TimeFrame for Resample/Replay (default: Ticks)
    --compression COMPRESSION
                          Compression for Resample/Replay (default: 1)
    --no-takelate         resample/replay, do not accept late samples in new bar
                          if the data source let them through (latethrough)
                          (default: False)
    --no-bar2edge         no bar2edge for resample/replay (default: False)
    --no-adjbartime       no adjbartime for resample/replay (default: False)
    --no-rightedge        no rightedge for resample/replay (default: False)
    --broker              Use IB as broker (default: False)
    --trade               Do Sample Buy/Sell operations (default: False)
    --donotsell           Do not sell after a buy (default: False)
    --exectype {Market,Close,Limit,Stop,StopLimit}
                          Execution to Use when opening position (default:
                          Market)
    --stake STAKE         Stake to use in buy operations (default: 10)
    --valid VALID         Seconds to keep the order alive (0 means DAY)
                          (default: None)
    --cancel CANCEL       Cancel a buy order after n bars in operation, to be
                          combined with orders like Limit (default: 0)

The code:

.. literalinclude:: ./ibtest.py
   :language: python
   :lines: 21-
