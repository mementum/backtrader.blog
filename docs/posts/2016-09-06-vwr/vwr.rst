
.. post:: Sep 6, 2016
   :author: mementum
   :image: 1
   :excerpt: 3


Variability Weighted Return (or VWR)
####################################

Following some hints about an *improved* `SharpeRatio`, *backtrader* has
added this *analyzer* to its arsenal.

The literature is at:

  - https://www.crystalbull.com/sharpe-ratio-better-with-log-returns/

Starting with the benefits of logarithmic returns and following on the side
effects of having the *standard deviation* in the denominator of the
`SharpeRatio` equation, the document develops the formula and expectations of
this *analyzer*.

One of the most important properties may be:

  - *A consistent value across timeframes*

The ``SharpeRatio`` uses the arithmetic mean of excess returns versus a risk
free rate/asset divided by the *standard deviation* of the excess returns
versus the risk free rate/asset. This makes the final value dependent on the
number of samples and the standard deviation which could even be ``0``. In this
case the ``SharpeRatio`` would be infinite.

*backtrader* includes a sample for testing the ``SharpeRatio`` using the sample
data which includes prices for ``2005`` and ``2006``. The returned values for
different *timeframes*:

  - ``TimeFrame.Years``: ``11.6473``
  - ``TimeFrame.Months``: ``0.5425``
  - ``TimeFrame.Weeks``: ``0.457``
  - ``TimeFrame.Days``: ``0.4274``

.. note::

   For consistency the ratio is annualized. The ``sharpe-timereturn`` sample
   and is executed with::

     --annualize --timeframe xxx

   Where ``xxx`` stands for ``days``, ``weeks``, ``months`` or ``years``
   (default)

In this sample there is something clear:

  - The smaller the *timeframe*, the smaller the value of the ``SharpeRatio``

Which is caused by the number of samples which is larger for the smaller
*timeframes* and adds *variability* and hence increases the *standard
deviation*, which is the denominator in the ``SharpeRatio`` equation.

There is a *large sensibility* to changes in the *standard deviation*

It is exactly this what the ``VWR`` tries to solved by offering a consistent
value across *timeframes*. The same strategy offers the following values:

  - ``TimeFrame.Years``: ``1.5368``
  - ``TimeFrame.Months``: ``1.5163``
  - ``TimeFrame.Weeks``: ``1.5383``
  - ``TimeFrame.Days``: ``1.5221``

.. note::

   The ``VWR`` is returned (following the literature) always in annualized
   form. The sample is executed with::

     --timeframe xxx

   Where ``xxx`` stands for ``days``, ``weeks``, ``months`` or ``years``

   The default is ``None`` which uses the underlying *timeframe* of the data
   which is ``days``

Consistent values which show that the performance of the strategy when it comes
to offering consistent returns can be evaluated on any timeframe.

.. note::

   Theoretically the values should be the same, but this would require fine
   tuning the ``tann`` parameters (number of periods for annualization) to the
   exact trading periods. This is not done here, because the purpose is just
   looking at consistency.


Conclusion
**********

A new tool which offers a timeframe independent approach to strategy evaluation
is available for the users


Sample Usage
************
::

  $ ./vwr.py --help
  usage: vwr.py [-h] [--data DATA] [--cash CASH] [--fromdate FROMDATE]
                [--todate TODATE] [--writercsv]
                [--tframe {weeks,months,days,years}] [--sigma-max SIGMA_MAX]
                [--tau TAU] [--tann TANN] [--stddev-sample] [--plot [kwargs]]

  TimeReturns and VWR

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA, -d DATA  data to add to the system (default:
                          ../../datas/2005-2006-day-001.txt)
    --cash CASH           Starting Cash (default: None)
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format (default: None)
    --todate TODATE, -t TODATE
                          Starting date in YYYY-MM-DD format (default: None)
    --writercsv, -wcsv    Tell the writer to produce a csv stream (default:
                          False)
    --tframe {weeks,months,days,years}, --timeframe {weeks,months,days,years}
                          TimeFrame for the Returns/Sharpe calculations
                          (default: None)
    --sigma-max SIGMA_MAX
                          VWR Sigma Max (default: None)
    --tau TAU             VWR tau factor (default: None)
    --tann TANN           Annualization factor (default: None)
    --stddev-sample       Consider Bessels correction for stddeviation (default:
                          False)
    --plot [kwargs], -p [kwargs]
                          Plot the read data applying any kwargs passed For
                          example: --plot style="candle" (to plot candles)
                          (default: None)


Sample Code
***********

.. literalinclude:: vwr.py
   :language: python
   :lines: 21-
