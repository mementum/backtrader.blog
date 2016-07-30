
.. post:: Jul 30, 2016
   :author: mementum
   :image: 1

MACD Settings
#############

In the *Algotrading* site of *Reddit* I found the following thread:

  - `How to determine best MACD settings?
    <https://www.reddit.com/r/algotrading/comments/4s832w/how_to_determine_best_macd_settings/>`_

Having started the *backtrader* quest because of `Trading Your Way To Financial
Freedom - Amazon Link
<https://www.amazon.com/Trade-Your-Way-Financial-Freedom/dp/007147871X>`_ I had
no other choice but to post an answer and craft a sample.

The strategy approach is loosely based on some of the ideas presented in the
book. Nothing new under the sun. And the parameters have been quickly set. No
overfitting, no optimization, no nothing. Roughly:

  - Enter if the ``macd`` line crosses the ``signal`` line to the upside and a
    control ``Simple Moving Average`` has had a net negative direction in the
    last x periods (current *SMA* value below the value *x* periods ago)

  - Set a ``stop`` price ``N x ATR`` times away from the ``close`` price

  - Exit the market if the ``close`` price goes below the ``stop`` price

  - If still in the market, update the ``stop`` price only if it's greater than
    the actual one

The staking is done by:

  - Having a ``Sizer`` allocate a *percentage* of the available cash to the
    operation. The more the strategy wins, the more it stakes ... and the more
    it loses the less it stakes.

There is a *commision* included. Because the tests will be done with *stocks* a
percentage commission has been chosen with a value ``0.0033`` (aka ``0.33%``
per round trip.

To put this into play, there will be 3 runs with 3 datas (for a total of 9
runs)

  #. The standard parameters which have been chosen manually

  #. Increase cash allocation perentage from ``0.20`` to ``0.50``

  #. Increase ATR distance for the stop from ``3.0`` to ``4.0`` to try to avoid
     being whipped

The manually chosen parameters for the strategy::

    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )


And system wide::

    parser.add_argument('--cash', required=False, action='store',
                        type=float, default=50000,
                        help=('Cash to start with'))

    parser.add_argument('--cashalloc', required=False, action='store',
                        type=float, default=0.20,
                        help=('Perc (abs) of cash to allocate for ops'))

    parser.add_argument('--commperc', required=False, action='store',
                        type=float, default=0.0033,
                        help=('Perc (abs) commision in each operation. '
                              '0.001 -> 0.1%%, 0.01 -> 1%%'))


The date range will be from ``2005-01-01`` to ``2014-12-31`` for a total of 10
years.


Analyzers
*********

To get some *objective* data 3 analyzers will be added to the system:

  - Two ``TimeReturn`` for the entire period

    1. For the strategy itself
    2. For the data being operated upon as benchmark

    Effectively benchmarking the strategy against the asset

  - A ``TimeReturn`` to measure *annual returns*

  - A ``SharpeRatio`` to see how the strategy performs against a risk-free
    asset

    The value is set at ``1%``, can be changed with the sample options

  - A ``SQN`` (*System Quality Number*) to analyze the quality of the trades
    using this performance indicator defined by Van K. Tharp

Additonally a ``DrawDown`` observer will be added to the mix.


Run 1: Standard Parameters
**************************

YHOO
====
::

  $ ./macdsystem.py --plot --dataset yhoo
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: -0.07118518868
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 0.316736183525
  ===============================================================================
  TimeReturn:
    - 2005-12-31: 0.02323119024
    - 2006-12-31: -0.0813678018166
    - 2007-12-31: -0.0144802141955
    - 2008-12-31: -0.142301023804
    - 2009-12-31: 0.0612152927491
    - 2010-12-31: 0.00898269987778
    - 2011-12-31: -0.00845048588578
    - 2012-12-31: 0.0541362123146
    - 2013-12-31: 0.0158705967774
    - 2014-12-31: 0.0281978956007
  ===============================================================================
  SharpeRatio:
    - sharperatio: -0.261214264357
  ===============================================================================
  SQN:
    - sqn: -0.784558216044
    - trades: 45

.. thumbnail:: yhoo-run01.png

ORCL
====
::

  $ ./macdsystem.py --plot --dataset orcl
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 0.24890384718
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 2.23991354467
  ===============================================================================
  TimeReturn:
    - 2005-12-31: -0.02372911952
    - 2006-12-31: 0.0692563226579
    - 2007-12-31: 0.0551086853554
    - 2008-12-31: -0.026707886256
    - 2009-12-31: 0.0786118091383
    - 2010-12-31: 0.037571919146
    - 2011-12-31: 0.00846519206845
    - 2012-12-31: 0.0402937469005
    - 2013-12-31: -0.0147124502187
    - 2014-12-31: 0.00710131291379
  ===============================================================================
  SharpeRatio:
    - sharperatio: 0.359712552054
  ===============================================================================
  SQN:
    - sqn: 1.76240859868
    - trades: 37

.. thumbnail:: orcl-run01.png

NVDA
====
::

  $ ./macdsystem.py --plot --dataset nvda
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: -0.0178507058999
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: -0.177604931253
  ===============================================================================
  TimeReturn:
    - 2005-12-31: 0.0773031957141
    - 2006-12-31: 0.105007457325
    - 2007-12-31: 0.015286423657
    - 2008-12-31: -0.109130552525
    - 2009-12-31: 0.14716076542
    - 2010-12-31: -0.0891638005423
    - 2011-12-31: -0.0788216550171
    - 2012-12-31: -0.0498231953066
    - 2013-12-31: -0.0119166712361
    - 2014-12-31: 0.00940493597076
  ===============================================================================
  SharpeRatio:
    - sharperatio: -0.102967601564
  ===============================================================================
  SQN:
    - sqn: -0.0700412395071
    - trades: 38

.. thumbnail:: nvda-run01.png

Analysis of Run 1
=================

 - *YHOO*

   The 1st and 2nd ``TimeReturn`` analyzers (the strategy and the asset itself)
   show that The strategy has lost ``7.11%`` whilst the asset in question has
   appreciated ``31.67%``.

   Not even worth having a look at the other analyzers

 - *ORCL*

   A ``24.89%`` for the strategy, but paled by the ``223.99%`` return of the
   asset itself.

   The *SharpeRatio* at ``0.35`` is still away from the usual minimum target of
   ``1``.

   The *SQN* returns a ``1.76`` which at least gets a grading in the
   *Van K. Tharp* scale: ``1.6 - 1.9 Below Average``.

 - *NVDA*

   In this case a ``-1.78%`` for the strategy and a ``-17.76%`` for the
   asset. The SharpeRatio, with ``-0.10`` shows that even if the strategy has
   outperformed the asset, it would have been better to go with a ``1%`` bank
   account.

   The *SQN* is obviously not even at the bottom of the scale.


Conclusions of Run 1
====================

  - *1 great loss, a tie and a win which underperforms the asset*. Not that successful.

Run 2: CashAlloc to 0.50
************************

YHOO
====
::

  $ ./macdsystem.py --plot --dataset yhoo --cashalloc 0.50
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: -0.20560369198
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 0.316736183525
  ===============================================================================
  TimeReturn:
    - 2005-12-31: 0.05517338686
    - 2006-12-31: -0.195123836162
    - 2007-12-31: -0.0441556438731
    - 2008-12-31: -0.32426212721
    - 2009-12-31: 0.153876836394
    - 2010-12-31: 0.0167157437151
    - 2011-12-31: -0.0202891373759
    - 2012-12-31: 0.13289763017
    - 2013-12-31: 0.0408192946307
    - 2014-12-31: 0.0685527133815
  ===============================================================================
  SharpeRatio:
    - sharperatio: -0.154427699146
  ===============================================================================
  SQN:
    - sqn: -0.97846453428
    - trades: 45

.. thumbnail:: yhoo-run02.png

ORCL
====
::

  $ ./macdsystem.py --plot --dataset orcl --cashalloc 0.50
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 0.69016747856
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 2.23991354467
  ===============================================================================
  TimeReturn:
    - 2005-12-31: -0.0597533502
    - 2006-12-31: 0.176988400688
    - 2007-12-31: 0.140268851352
    - 2008-12-31: -0.0685193675128
    - 2009-12-31: 0.195760054561
    - 2010-12-31: 0.0956386594392
    - 2011-12-31: 0.018709882089
    - 2012-12-31: 0.100122407053
    - 2013-12-31: -0.0375741196261
    - 2014-12-31: 0.017570390931
  ===============================================================================
  SharpeRatio:
    - sharperatio: 0.518921692742
  ===============================================================================
  SQN:
    - sqn: 1.68844251174
    - trades: 37

.. thumbnail:: orcl-run02.png

NVDA
====
::

  $ ./macdsystem.py --plot --dataset nvda --cashalloc 0.50
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: -0.128845648113
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: -0.177604931253
  ===============================================================================
  TimeReturn:
    - 2005-12-31: 0.200593209479
    - 2006-12-31: 0.219254906522
    - 2007-12-31: 0.0407793562989
    - 2008-12-31: -0.259567975403
    - 2009-12-31: 0.380971100974
    - 2010-12-31: -0.208860409742
    - 2011-12-31: -0.189068154062
    - 2012-12-31: -0.122095056225
    - 2013-12-31: -0.0296495770432
    - 2014-12-31: 0.0232050942344
  ===============================================================================
  SharpeRatio:
    - sharperatio: -0.0222780544339
  ===============================================================================
  SQN:
    - sqn: -0.190661428812
    - trades: 38

.. thumbnail:: nvda-run02.png


Conclusions of Run 2
====================

 - Increasing the percentage cash allocation in each operation from ``20%`` to
   ``50%`` has increased the effect of the previous results

   - The strategy on *YHOO* and *NVDA* has lost more than before

   - And the strategy on *ORCL* has won more than before, still not close to
     the over *220%* of the asset.

Run 3: ATR Distance to 4.0
**************************

Still keeping the previous increase in cash allocation to ``50%``. The idea is
to avoid getting too early out of the market.

YHOO
====
::

  $ ./macdsystem.py --plot --dataset yhoo --cashalloc 0.50 --atrdist 4.0
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 0.01196310622
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 0.316736183525
  ===============================================================================
  TimeReturn:
    - 2005-12-31: 0.06476232676
    - 2006-12-31: -0.220219327475
    - 2007-12-31: -0.0525484648039
    - 2008-12-31: -0.314772526784
    - 2009-12-31: 0.179631995594
    - 2010-12-31: 0.0579495723922
    - 2011-12-31: -0.0248948026947
    - 2012-12-31: 0.10922621981
    - 2013-12-31: 0.406711050602
    - 2014-12-31: -0.0113108751022
  ===============================================================================
  SharpeRatio:
    - sharperatio: 0.0495181271704
  ===============================================================================
  SQN:
    - sqn: -0.211652416441
    - trades: 33

.. thumbnail:: yhoo-run03.png

ORCL
====
::

  $ ./macdsystem.py --plot --dataset orcl --cashalloc 0.50 --atrdist 4.0
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 0.21907748452
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 2.23991354467
  ===============================================================================
  TimeReturn:
    - 2005-12-31: -0.06660102614
    - 2006-12-31: 0.169334910265
    - 2007-12-31: 0.10620478758
    - 2008-12-31: -0.167615289704
    - 2009-12-31: 0.17616784045
    - 2010-12-31: 0.0591200431984
    - 2011-12-31: -0.100238247103
    - 2012-12-31: 0.135096589522
    - 2013-12-31: -0.0630483842399
    - 2014-12-31: 0.0175914485158
  ===============================================================================
  SharpeRatio:
    - sharperatio: 0.144210776122
  ===============================================================================
  SQN:
    - sqn: 0.646519270815
    - trades: 30

.. thumbnail:: orcl-run03.png

NVDA
====
::

  $ ./macdsystem.py --plot --dataset nvda --cashalloc 0.50 --atrdist 4.0
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: 0.48840287049
  ===============================================================================
  TimeReturn:
    - 9999-12-31 23:59:59.999999: -0.177604931253
  ===============================================================================
  TimeReturn:
    - 2005-12-31: 0.246510998277
    - 2006-12-31: 0.194958106054
    - 2007-12-31: -0.123140650516
    - 2008-12-31: -0.246174938322
    - 2009-12-31: 0.33121185861
    - 2010-12-31: -0.0442212647256
    - 2011-12-31: 0.0368388717861
    - 2012-12-31: -0.048473112136
    - 2013-12-31: 0.10657587649
    - 2014-12-31: 0.0883112536534
  ===============================================================================
  SharpeRatio:
    - sharperatio: 0.264551262551
  ===============================================================================
  SQN:
    - sqn: 0.564151633588
    - trades: 29

.. thumbnail:: nvda-run03.png


Conclusions of Run 3
====================

 - **Chicken, Chicken, Winner Dinner!!**

   The strategy makes money on the 3 assets

   - *YHOO*: ``1.19%`` vs the ``31.67%`` return of the asset itself

   - *ORCL*: ``21.90%`` vs the ``223.99%`` of the asset

     In this case increasing the ``ATRDist`` parameter has decreased the
     previous returns of *Run 2* which were at ``69.01%``

   - *NVDA*: ``48.84%`` vs ``-17.76%`` of the asset.

     The surprising thing here is that the *SharpRatio* and *SQN* are telling
     that

Usage of the sample
*******************
::

  $ ./macdsystem.py --help
  usage: macdsystem.py [-h] (--data DATA | --dataset {yhoo,orcl,nvda})
                       [--fromdate FROMDATE] [--todate TODATE] [--cash CASH]
                       [--cashalloc CASHALLOC] [--commperc COMMPERC]
                       [--macd1 MACD1] [--macd2 MACD2] [--macdsig MACDSIG]
                       [--atrperiod ATRPERIOD] [--atrdist ATRDIST]
                       [--smaperiod SMAPERIOD] [--dirperiod DIRPERIOD]
                       [--riskfreerate RISKFREERATE] [--plot [kwargs]]

  Sample for Tharp example with MACD

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA           Specific data to be read in (default: None)
    --dataset {yhoo,orcl,nvda}
                          Choose one of the predefined data sets (default: None)
    --fromdate FROMDATE   Starting date in YYYY-MM-DD format (default:
                          2005-01-01)
    --todate TODATE       Ending date in YYYY-MM-DD format (default: None)
    --cash CASH           Cash to start with (default: 50000)
    --cashalloc CASHALLOC
                          Perc (abs) of cash to allocate for ops (default: 0.2)
    --commperc COMMPERC   Perc (abs) commision in each operation. 0.001 -> 0.1%,
                          0.01 -> 1% (default: 0.0033)
    --macd1 MACD1         MACD Period 1 value (default: 12)
    --macd2 MACD2         MACD Period 2 value (default: 26)
    --macdsig MACDSIG     MACD Signal Period value (default: 9)
    --atrperiod ATRPERIOD
                          ATR Period To Consider (default: 14)
    --atrdist ATRDIST     ATR Factor for stop price calculation (default: 3.0)
    --smaperiod SMAPERIOD
                          Period for the moving average (default: 30)
    --dirperiod DIRPERIOD
                          Period for SMA direction calculation (default: 10)
    --riskfreerate RISKFREERATE
                          Risk free rate in Perc (abs) of the asset for the
                          Sharpe Ratio (default: 0.01)
    --plot [kwargs], -p [kwargs]
                          Plot the read data applying any kwargs passed For
                          example: --plot style="candle" (to plot candles)
                          (default: None)


And the code itself
*******************

.. literalinclude:: ./macd-settings.py
   :language: python
   :lines: 21-
