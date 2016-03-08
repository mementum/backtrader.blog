
.. post:: Mar 7, 2016
   :author: mementum
   :image: 1

Release 1.2.1.88
################

Changing the ``minor`` version number from ``1`` to ``2`` has taken sometime,
but the deprecation of the old ``DataResampler`` and ``DataReplayer`` have led
to it.

The documentation at **readthedocs** has


The `Documentation <http://backtrader.readthedocs.org/en/latest/>`_ has been
updated to only reference the modern way to do ``resampling`` and
``replaying``. It is as easy as:
::

    ...
    data = backtrader.feeds.BacktraderCSVData(dataname='mydata.csv')  # daily bars
    cerebro.resampledata(data, timeframe=backtrader.TimeFrame.Weeks) # to weeks
    ...

For *replaying* just change ``resampledata`` to ``replaydata``. There are
additional ways to do it, but this is the most straightforward interface and
probably the only one that will ever get used by anyone.


Following `Ticket #60 <https://github.com/mementum/backtrader/issues/60>`_ it
was clear that the extension mechanism which allows adding additional lines to
data feeds (actually to any *lines* based object) was not enough to support
what was suggested in the ticket.

Hence the implementation of an additional *parameter* to *lines* object which
allows the complete redefinition of the lines hierarchy (**Escape from OHLC
Land** would be an appropriate film title)

A sample named *data-bid-ask* has been added to the sources. From the sample:
::

    class BidAskCSV(btfeeds.GenericCSVData):
        linesoverride = True  # discard usual OHLC structure
        # datetime must be present and last
        lines = ('bid', 'ask', 'datetime')
        # datetime (always 1st) and then the desired order for
        params = (
            ('dtformat', '%m/%d/%Y %H:%M:%S'),

            ('datetime', 0),  # field pos 0
            ('bid', 1),  # default field pos 1
            ('ask', 2),  # defult field pos 2
        )

By specifying ``linesoverride`` the regular *lines* inheritance mechanisme is
bypassed and the defined lines in the object supersede any previous lines.

The release is available from *pypi* and can be installed with usual:
::

     pip install backtrader

Or if updating:
::

     pip install backtrader --upgrade
