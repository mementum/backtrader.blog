
.. post:: Dec 13, 2016
   :author: mementum
   :image: 1

Gold vs SP500
#############

Sometimes getting hints about where *backtrader* is in use helps understanding
what people may be looking for and using the platform for.

The reference:

  - https://estrategiastrading.com/oro-bolsa-estadistica-con-python/

It is a post (Spanish) analyzing two ETFs: ``GLD`` vs ``SPY`` (effectively
*Gold* vs *S&P500*)

Without going into the translation, let's concentrate on the important points
for *backtrader*:

  - Adding a *Correlation* indicator. For the sake of it ``PearsonR`` was
    chosen.

    And for the feat of creating it and instead of coding it from scratch, a
    sample of how to do it from a ``scipy`` function is done. The code

    .. literalinclude:: gold-vs-sp500.py
			:language: python
			:lines: 35-45

  - Adding rolling logarithmic returns

    The platform already had an analyzer with logarithmic returns, but not
    *rolling*.

    The analyzer ``LogReturnsRolling`` has been added, which takes a
    ``timeframe`` parameter (and ``compression``) to use a different timeframe
    than that of the data (if needed be)

    And together with it and for visualization (using the *analyzer*
    internally) a ``LogReturns`` observer

  - Allowing data on data plotting (easily). Just like this

    .. literalinclude:: gold-vs-sp500.py
			:language: python
			:lines: 81-89

    Just using ``plotmaster=data0`` will plot ``data1`` on ``data0``

Plotting the moving averages on its own axis and on each other was supported
from the very start of the platform.

The *analyzer* and *observer* have also been added to the platform, together
with a sample with the same defaults as those from the blog post.

Running the sample::

  $ ./gold-vs-sp500.py --cerebro stdstats=False --plot volume=False

.. note::

   ``stdstats=False`` and ``volume=False`` are there to reduce clutter in the
   chart by removing some of the usual things like ``CashValue`` observer and
   the *volume* subplots.

Produces a chart which mimics most of the output from the article.

.. thumbnail:: gold-vs-sp500.png

Not included:

  - The charts creating distributions of returns.

    They wouldn't fit in the chart which has a *datetime* based x axis.

But having those distributions may come.

Sample Usage
************
::

  $ ./gold-vs-sp500.py --help
  usage: gold-vs-sp500.py [-h] [--data0 TICKER] [--data1 TICKER] [--offline]
                          [--fromdate FROMDATE] [--todate TODATE]
                          [--cerebro kwargs] [--broker kwargs] [--sizer kwargs]
                          [--strat kwargs] [--plot [kwargs]] [--myobserver]

  Gold vs SP500 from https://estrategiastrading.com/oro-bolsa-estadistica-con-
  python/

  optional arguments:
    -h, --help           show this help message and exit
    --data0 TICKER       Yahoo ticker to download (default: SPY)
    --data1 TICKER       Yahoo ticker to download (default: GLD)
    --offline            Use the offline files (default: False)
    --fromdate FROMDATE  Date[time] in YYYY-MM-DD[THH:MM:SS] format (default:
                         2005-01-01)
    --todate TODATE      Date[time] in YYYY-MM-DD[THH:MM:SS] format (default:
                         2016-01-01)
    --cerebro kwargs     kwargs in key=value format (default: )
    --broker kwargs      kwargs in key=value format (default: )
    --sizer kwargs       kwargs in key=value format (default: )
    --strat kwargs       kwargs in key=value format (default: )
    --plot [kwargs]      kwargs in key=value format (default: )

Sample Code
***********

.. literalinclude:: gold-vs-sp500.py
   :language: python
   :lines: 21-
