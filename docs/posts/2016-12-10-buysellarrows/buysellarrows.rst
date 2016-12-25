
.. post:: Dec 10, 2016
   :author: mementum
   :image: 1
   :excerpt: 2

Arrows for the BuySell Observer
###############################

*backtrader* was conceived to try to deliver ease of use. Creation of
*indicators* and other usual suspects should be easy.

And of course, customizing existing items should also be part of the deal.

A topic in the community, `BuySell Arrows
<https://community.backtrader.com/topic/8/change-buysell-to-trade-arrows-in-charts-213>`_,
which originates from the migration from issues is a good example.

The current behavior can be seen by running the sample::

  ./buysellarrows.py --plot style="'ohlc'"

With following output

.. thumbnail:: buysell-triangles.png

The sample when using does the following:

  - Define a subclass of the ``BuySell`` observer
  - Override the ``plotlines`` definition and simply change the markers which
    indicate the buy and sell operations
  - Monkey patches the existing observer with the custom one

In code terms.

.. literalinclude:: buysellarrows.py
   :language: python
   :lines: 30-34

and:

.. literalinclude:: buysellarrows.py
   :language: python
   :lines: 82-85

.. note::

   Monkey patching is not strictly necesary. One can also go the standard way::

     cerebro = bt.Cerebro(stdstats=False)  # remove the standard observers

     ...
     cerebro.addobserver(MyObserver, barplot=True)

     ...

   And the custom observer would also be used, but the other regularly
   instantiated observers would be missing. Hence the monkey patching in the
   sample to simply modify the observer and keep the look.

Running it again with the reight parameter::

  $ ./buysellarrows.py --plot style="'ohlc'" --myobserver

Which then outputs.

.. thumbnail:: buysell-arrows.png

Because ``matplotlib`` allows the use of *Unicode* characters, the default look
of the observer can be changed to anything and nos just arrows. Be my
guest. For example from *Wikipedia*:

  - `Arrows (Unicode block)
    <https://en.wikipedia.org/wiki/Arrows_%28Unicode_block%29>`_

Sample Usage
************
::

  $ ./buysellarrows.py --help
  usage: buysellarrows.py [-h] [--data DATA | --yahoo TICKER]
                          [--fromdate FROMDATE] [--todate TODATE]
                          [--cerebro kwargs] [--broker kwargs] [--sizer kwargs]
                          [--strat kwargs] [--plot [kwargs]] [--myobserver]

  buysell arrows ...

  optional arguments:
    -h, --help           show this help message and exit
    --data DATA          Data to read in (default:
                         ../../datas/2005-2006-day-001.txt)
    --yahoo TICKER       Yahoo ticker to download (default: )
    --fromdate FROMDATE  Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
    --todate TODATE      Date[time] in YYYY-MM-DD[THH:MM:SS] format (default: )
    --cerebro kwargs     kwargs in key=value format (default: )
    --broker kwargs      kwargs in key=value format (default: )
    --sizer kwargs       kwargs in key=value format (default: )
    --strat kwargs       kwargs in key=value format (default: )
    --plot [kwargs]      kwargs in key=value format (default: )
    --myobserver         Patch in Custom BuySell observer (default: False)

Sample Code
***********

.. literalinclude:: buysellarrows.py
   :language: python
   :lines: 21-
