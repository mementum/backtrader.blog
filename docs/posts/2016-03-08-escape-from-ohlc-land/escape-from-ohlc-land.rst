
.. post:: Mar 8, 2016
   :author: mementum
   :image: 1

Escape from OHLC Land
#####################

One of the key concepts applied during the conception and development of
`backtrader` was **flexibility**. The *metaprogramming* and *introspection*
capabilities of Python were (and still are) the basis to keep many things
flexible whilst still being able to deliver.

An old post shows the extension concept.

  - `Extending a datafeed
    <http://blog.backtrader.com/posts/2015-08-07/extending-a-datafeed/>`_

The basics::

    from backtrader.feeds import GenericCSVData

    class GenericCSV_PE(GenericCSVData):
        lines = ('pe',)  # Add 'pe' to already defined lines

Done. ``backtrader`` defines in the background the most usual lines: OHLC.

If we digged into the final aspect of ``GenericCSV_PE``, the sum of inherited
plus newly defined lines would yield the following lines::

    ('close', 'open', 'high', 'low', 'volume', 'openinterest', 'datetime', 'pe',)

This can be check at any time with the method ``getlinealiases`` (applicable to
*DataFeeds*, *Indicators*, *Strategies* and *Observers*)

The mechanism is flexible and by poking a bit into the internals you could
actually get anything, but it has been proven not to be enough.

`Ticket #60 <https://github.com/mementum/backtrader/issues/60>`_ asks about
supporting *High Frequency Data*, ie: Bid/Ask data. Which implies that the
predefined *lines* hierarchy in the form of *OHLC* is not enough. The *Bid* and
*Ask* prices, volumes and number of trades can be made to fit into the existing
*OHLC* fields, but it wouldn't feel natural. And if one is only concerned with
the *Bid* and *Ask* prices, there would be too many fields left untouched.

This called for a solution which has been implemented with `Release 1.2.1.88
<http://blog.backtrader.com/posts/2016-03-07-release-1.2.1.88/release-1.2.1.88/>`_. The
idea can be summarized as:

  - Now it's not only possible to *extend* the existing hierarchy, but also to
    *replace* the hierarchy with a new one

Only one constraint in place:

  - There must be a ``datetime`` field present (which will hopefully contain
    meaningful ``datetime`` information)

    This is so because ``backtrader`` needs something for synchronization
    (multiple datas, multiple timeframes, resampling, replaying) just like
    Archimedes needed a lever.

Here it is how it works::

    from backtrader.feeds import GenericCSVData

    class GenericCSV_BidAsk(GenericCSVData):
        linesoverride = True
        lines = ('bid', 'ask', 'datetime')  # Replace hierarchy with this one

Done.

Ok, not fully. But only because we are looking at loading the lines from a
*csv* source. The hierarchy has actually already been **replaced** with the
*bid, ask datetime* definition thanks to the ``linesoverride=True`` setting.

The original ``GenericCSVData`` class parses a *csv* file
and needs a hint as to where the *fields* corresponding to the *lines* are
located. The original definition is::

    class GenericCSVData(feed.CSVDataBase):
        params = (
            ('nullvalue', float('NaN')),
            ('dtformat', '%Y-%m-%d %H:%M:%S'),
            ('tmformat', '%H:%M:%S'),

            ('datetime', 0),
            ('time', -1),  # -1 means not present
            ('open', 1),
            ('high', 2),
            ('low', 3),
            ('close', 4),
            ('volume', 5),
            ('openinterest', 6),
        )

The new *hierarchy-redefining-class* can be completed with a light touch::

    from backtrader.feeds import GenericCSVData

    class GenericCSV_BidAsk(GenericCSVData):
        linesoverride = True
        lines = ('bid', 'ask', 'datetime')  # Replace hierarchy with this one

        params = (('bid', 1), ('ask', 2))

Indicating that *Bid* prices are field #1 in the csv stream and *Ask* prices
are field #2. We have left the *datetime* #0 definition untouched from the base
class.

Crafting a small data file for the occasion helps:

.. literalinclude:: ./bidask.csv

Add a small test script to the equation (with some more content for those who
just go directly to the samples in the sources) (see full code at the end)::

    $ ./bidask.py

And the output speaks up for itself::

     1: 2010-02-03T16:53:50 - Bid 0.5346 - 0.5347 Ask
     2: 2010-02-03T16:53:51 - Bid 0.5343 - 0.5347 Ask
     3: 2010-02-03T16:53:52 - Bid 0.5543 - 0.5545 Ask
     4: 2010-02-03T16:53:53 - Bid 0.5342 - 0.5344 Ask
     5: 2010-02-03T16:53:54 - Bid 0.5245 - 0.5464 Ask
     6: 2010-02-03T16:53:54 - Bid 0.5460 - 0.5470 Ask
     7: 2010-02-03T16:53:56 - Bid 0.5824 - 0.5826 Ask
     8: 2010-02-03T16:53:57 - Bid 0.5371 - 0.5374 Ask
     9: 2010-02-03T16:53:58 - Bid 0.5793 - 0.5794 Ask
    10: 2010-02-03T16:53:59 - Bid 0.5684 - 0.5688 Ask

Et voilá! The *Bid*/*Ask* prices have been properly read, parsed and
interpreted and the strategy has been able to access the *.bid* and *.ask*
lines in the data feed through *self.data*.

Redefining the *lines* hierarchy opens a broad question though and that is the
usage of the already predefined *Indicators*.

  - Example: the *Stochastic* is an indicator which relies on *close*, *high*
    and *low* prices to calculate its output

    Even if we though about *Bid* as the *close* (because is the first) there
    is only one other *price* element (*Ask*) and not two more. And
    conceptually *Ask* has nothing to do with *high* and *low*

    It is probable that someone working with these fields and operating (or
    researching) in the *High Frequency Trading* domain is not concerned with
    *Stochastic* as an indicator of choice

  - Other indicators like *moving average* are perfectly fine. They assume
    nothing about what the fields mean or imply and will happily take
    anything. As such one can do::

        mysma = backtrader.indicators.SMA(self.data.bid, period=5)

    And an moving average of the last 5 *bid* prices will be delivered

The test script already supports adding a *SMA*. Let's execute::

    $ ./bidask.py --sma --period=3

The output::

     3: 2010-02-03T16:53:52 - Bid 0.5543 - 0.5545 Ask - SMA: 0.5411
     4: 2010-02-03T16:53:53 - Bid 0.5342 - 0.5344 Ask - SMA: 0.5409
     5: 2010-02-03T16:53:54 - Bid 0.5245 - 0.5464 Ask - SMA: 0.5377
     6: 2010-02-03T16:53:54 - Bid 0.5460 - 0.5470 Ask - SMA: 0.5349
     7: 2010-02-03T16:53:56 - Bid 0.5824 - 0.5826 Ask - SMA: 0.5510
     8: 2010-02-03T16:53:57 - Bid 0.5371 - 0.5374 Ask - SMA: 0.5552
     9: 2010-02-03T16:53:58 - Bid 0.5793 - 0.5794 Ask - SMA: 0.5663
    10: 2010-02-03T16:53:59 - Bid 0.5684 - 0.5688 Ask - SMA: 0.5616

.. note::

   Plotting still relies on ``open``, ``high``, ``low``, ``close`` and
   ``volume`` being present in the *data* feed.

   Some cases can be directly covered by simply plotting with a *Line on Close*
   and taking just the 1st defined line in the object. But a sound model has to
   be developed. For an upcoming version of ``backtrader``

The test script usage::

    $ ./bidask.py --help
    usage: bidask.py [-h] [--data DATA] [--dtformat DTFORMAT] [--sma]
                     [--period PERIOD]

    Bid/Ask Line Hierarchy

    optional arguments:
      -h, --help            show this help message and exit
      --data DATA, -d DATA  data to add to the system (default:
                            ../../datas/bidask.csv)
      --dtformat DTFORMAT, -dt DTFORMAT
                            Format of datetime in input (default: %m/%d/%Y
                            %H:%M:%S)
      --sma, -s             Add an SMA to the mix (default: False)
      --period PERIOD, -p PERIOD
                            Period for the sma (default: 5)

And the test script itself (included in the ``backtrader`` sources)

.. literalinclude:: ./bidask.py
   :language: python
   :lines: 21-
