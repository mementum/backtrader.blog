
.. post:: Sep 21, 2015
   :author: mementum
   :image: 1

Plotting on the same axis
#########################

Following a comment on the blog a slight addition (luckily just a few lines of
code) has been made to plotting.

  - The abilitiy to plot any indicator on any other indicator

A potential use case:

  - Saving precious screen real estate by plotting some indicators together and
    having more room to appreciate the OHLC bars

    Example: join Stochastic and RSI plots

Of course something has to be taken into account:

  - If the scaling of the indicators is too different, some of the indicators
    would not be visible.

    Example: a MACD oscillating around 0.0 plus/minus 0.5 plotted over a
    Stochastic which moves across the 0-100 range.

The first implementation is in the development branch on commit `...14252c6
<https://github.com/mementum/backtrader/commit/6991c0995ddc5097ccd14bffef91d5c8114252c6>`_

A sample script (see below for the full code) let us see the effects

.. note:: Because the sample strategy does nothing, the standards observers are
	  removed unless activated via a command line switch.

First the script run with no switches.

  - A Simple Moving Average is plotted over the data
  - A MACD, Stochastic and RSI are plotted on own axis/subplots

Execution::

  $ ./plot-same-axis.py

And the chart.

.. thumbnail:: ./plotting-same-axis-standard.png

The second execution changes the panorama:

  - The Simple Moving Average is moved to a subplot
  - The MACD is hidden
  - The RSI is plotted over the Stochastic (the y-axis range is compatible:
    0-100)

    This is achieved by setting the ``plotinfo.plotmaster`` value of the
    indicator to the other indicator to be plotted onto.

    In this case and because the local variables in ``__init__`` are named
    ``stoc`` for Stochastic and ``rsi`` for RSI, it looks like::

      rsi.plotinfo.plotmaster = stoc

Execution::

  $ ./plot-same-axis.py --smasubplot --nomacdplot --rsioverstoc

The chart.

.. thumbnail:: ./plotting-same-axis-new-panorama.png

And to check the incompatibility of scales, let's try plotting the rsi over the SMA::

  $ ./plot-same-axis.py --rsiovermacd

The chart.

.. thumbnail:: ./plotting-same-axis-rsi-over-sma.png

The RSI label shows up with the data and the SMA, but the scale is in the
3400-4200 range and hence ... no traces of the RSI.

A further futile attempt is to place the SMA on a subplot and again plot the RSI
on the SMA

  $ ./plot-same-axis.py --rsiovermacd --smasubplot

The chart.

.. thumbnail:: ./plotting-same-axis-rsi-over-sma-subplot.png

The label is clear but all that remains from the RSI is a faint blue line at the
bottom of the SMA plot.

.. update:: Sep 22, 2015

   Added multi-line indicator plotted over another indicator

Going in the other direction, let's plot a multi-line indicator on another
indicator. Let's plot the Stochastic on the RSI::

  $ ./plot-same-axis.py --stocrsi

.. thumbnail:: ./plotting-same-axis-stoc-over-rsi.png

It works. The ``Stochastic`` label shows up and the 2 lines ``K%`` and ``D%``
too. But the lines are not "named" because we have got the name of the
indicator.

In the code, the current setting would be::

  stoc.plotinfo.plotmaster = rsi

To have the names of the Stochastic lines displayed instead of the name, we
would additionally need::

  stoc.plotinfo.plotlinelabels = True

This has been parametrized and a new execution shows it::

  $ ./plot-same-axis.py --stocrsi --stocrsilabels

With the chart now showing the name of the Stochasti lines below the name of the
RSI line.

.. thumbnail:: ./plotting-same-axis-stoc-over-rsi-lines.png

The script usage::

  $ ./plot-same-axis.py --help
  usage: plot-same-axis.py [-h] [--data DATA] [--fromdate FROMDATE]
                           [--todate TODATE] [--stdstats] [--smasubplot]
                           [--nomacdplot]
                           [--rsioverstoc | --rsioversma | --stocrsi]
                           [--stocrsilabels] [--numfigs NUMFIGS]

  Plotting Example

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA, -d DATA  data to add to the system
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format
    --todate TODATE, -t TODATE
                          Starting date in YYYY-MM-DD format
    --stdstats, -st       Show standard observers
    --smasubplot, -ss     Put SMA on own subplot/axis
    --nomacdplot, -nm     Hide the indicator from the plot
    --rsioverstoc, -ros   Plot the RSI indicator on the Stochastic axis
    --rsioversma, -rom    Plot the RSI indicator on the SMA axis
    --stocrsi, -strsi     Plot the Stochastic indicator on the RSI axis
    --stocrsilabels       Plot line names instead of indicator name
    --numfigs NUMFIGS, -n NUMFIGS
                          Plot using numfigs figures

And the code.

.. literalinclude:: ./plot-same-axis.py
   :language: python
   :lines: 21-
