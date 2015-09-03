
.. post:: Sep 3, 2015
   :author: mementum
   :image: 1

MultiData Strategy
##################

Because nothing in the world lives in isolation it can well be that the trigger
to buy an asset is actually another asset.

Using different analysis techniques a correlation may have been found between
two different datas.

``backtrader`` supports using different data sources simultaneously so it can
possibly be used for the purpose in most cases.

Let's assume that a correlation has been found between the following companies:

  - ``Oracle``
  - ``Yahoo``

One could imagine that when things go well for Yahoo, the company buys more
servers, more databases and more professional services from Oracle, which in
turn pushes the stock prices up.

As such and having run a profound analysis a strategy is devised:

  - If the close price of ``Yahoo`` goes over the Simple Moving Average (period 15)

  - Buy ``Oracle``

To exit the position:

  - Use the crossing downwards of the close price

Order Execution Type:

  - Market

In summary what's needed to set this up with ``backtrader``:

  - Create a ``cerebro``
  - Load the Data Source 1 (Oracle) and add it to cerebro
  - Load the Data Source 2 (Yahoo) and add it to cerebro
  - Load the Strategy we have devised

The details of the strategy:

  - Create a Simple Moving Average on Data Source 2 (Yahoo)
  - Create a CrossOver indicator using Yahoo's close price and the Moving
    Average

And then execute the buy/sell orders on Data Source 1 (Oracle) as described
above.

The script below uses the following defaults:

  - Oracle (Data Source 1)
  - Yahoo (Data Source 2)
  - Cash: 10000 (system default)
  - Stake: 10 shares
  - Commission: 0.5% for each round (expressed as 0.005)
  - Period: 15 trading days
  - Period: 2003, 2004 and 2005

The script can take arguments to modify the above settings as seen in the help
text::

  $ ./multidata-strategy.py --help
  usage: multidata-strategy.py [-h] [--data0 DATA0] [--data1 DATA1]
                               [--fromdate FROMDATE] [--todate TODATE]
                               [--period PERIOD] [--cash CASH]
                               [--commperc COMMPERC] [--stake STAKE] [--plot]
                               [--numfigs NUMFIGS]

  MultiData Strategy

  optional arguments:
    -h, --help            show this help message and exit
    --data0 DATA0, -d0 DATA0
                          1st data into the system
    --data1 DATA1, -d1 DATA1
                          2nd data into the system
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format
    --todate TODATE, -t TODATE
                          Starting date in YYYY-MM-DD format
    --period PERIOD       Period to apply to the Simple Moving Average
    --cash CASH           Starting Cash
    --commperc COMMPERC   Percentage commission for operation (0.005 is 0.5%
    --stake STAKE         Stake to apply in each operation
    --plot, -p            Plot the read data
    --numfigs NUMFIGS, -n NUMFIGS
                          Plot using numfigs figures


The result of a standard execution::

  $ ./multidata-strategy.py
  2003-02-11T23:59:59+00:00, BUY CREATE , 9.14
  2003-02-12T23:59:59+00:00, BUY COMPLETE, 11.14
  2003-02-12T23:59:59+00:00, SELL CREATE , 9.09
  2003-02-13T23:59:59+00:00, SELL COMPLETE, 10.90
  2003-02-14T23:59:59+00:00, BUY CREATE , 9.45
  2003-02-18T23:59:59+00:00, BUY COMPLETE, 11.22
  2003-03-06T23:59:59+00:00, SELL CREATE , 9.72
  2003-03-07T23:59:59+00:00, SELL COMPLETE, 10.32
  ...
  ...
  2005-12-22T23:59:59+00:00, BUY CREATE , 40.83
  2005-12-23T23:59:59+00:00, BUY COMPLETE, 11.68
  2005-12-23T23:59:59+00:00, SELL CREATE , 40.63
  2005-12-27T23:59:59+00:00, SELL COMPLETE, 11.63
  ==================================================
  Starting Value - 100000.00
  Ending   Value - 99959.26
  ==================================================

After two complete years of execution the Strategy:

  - Has lost 40.74 monetary units

**So much for the correlation between Yahoo and Oracle**

The Visual Ouput (add ``--plot`` to produce a chart)

.. thumbnail:: ./multidata-strategy-defaults.png

And the script (which has been added to the source distribution of
``backtrader`` under the ``samples/multidata-strategy`` directory.

.. literalinclude:: ./multidata-strategy.py
   :language: python
   :lines: 21-
