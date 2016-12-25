
.. post:: Oct 4, 2015
   :author: mementum
   :image: 1

Bar Synchronization
###################

The lack of a standard formula in the literature and/or industry is not the
problem, because the problem can actually be summarized as:

  - Bar Synchronization

`Ticket #23 <https://github.com/mementum/backtrader/issues/23>`_ raises some
questions as to whether ``backtrader`` can look into calculating
a **RelativeVolume** indicator.

The requester needs to compare the volume of a given moment in time against the
same moment in time on the previous trading day. Including:

  - Some pre-market data of unknown length

Having such a requirement invalidates the basic principle on which most
indicators are built:

  - Having a fixed period which is used to look backwards

Furthermore and given the comparison is done intraday, something else has to be
taken into account:

  - Some of the "intraday" instants may be missing (be it minutes or seconds)

    It is unlikely a data source will be missing a daily bar, but missing a
    minute or second bar is not that uncommon.

    The main reason being that there may have not been any negotiation at
    all. Or they might have been a problem at the negotiation exchange which
    actually prevented the bar from being recorded at all.

Taking into account all the aforementioned points some conclusions for the
development of the indicator:

  - The **period** is not a period in this case but a buffer to make sure enough
    bars will be there to have the indicator kick in as soon as possible

  - Some bars may be missing

  - The main issue is synchronization

Luckily there is a key which comes to the rescue to aid with the
synchronization:

  - Compared bars are "intraday" and hence counting the already seen days and
    the number of seen "bars" for a given moment of time enables synchronization

The previous day values are kept in a dictionary, because the "lookback" period
as explained before is unknown.

Some other early ideas can be discarded, like for example implementing a
``DataFilter`` data source because this would actually bring the data source out
of sync with other parts of the systme by removing the pre-market data. And the
synchronization problem would also be there.

An idea to be explored would be creating a ``DataFiller`` which would fill in
the missing minutes/seconds by using the last closing price and setting the
volume to 0.

Getting hands on has also proven good to identify some extra needs in
``backtrader`` like a **time2num** function (an addition to the date2num and
num2date family) and what will become extra methods for the **lines**:

  - Extracting the "day" and "fraction" (time) of day parts from the floating
    point representation of the day

    To be called "dt" and "tm"

In the meantime the code of the ``RelativeVolumeByBar`` indicator is presented
below. Having the"period"/"buffer" calculation inside the indicator is not the
preferred pattern, but it serves the purpose in this case.

.. literalinclude:: ./relvolbybar.py
   :language: python
   :lines: 21-

Invoked through an script, which can be used as follows::

  $ ./relative-volume.py --help
  usage: relative-volume.py [-h] [--data DATA] [--prestart PRESTART]
                            [--start START] [--end END] [--fromdate FROMDATE]
                            [--todate TODATE] [--writer] [--wrcsv] [--plot]
                            [--numfigs NUMFIGS]

  MultiData Strategy

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA, -d DATA  data to add to the system
    --prestart PRESTART   Start time for the Session Filter
    --start START         Start time for the Session Filter
    --end END, -te END    End time for the Session Filter
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format
    --todate TODATE, -t TODATE
                          Starting date in YYYY-MM-DD format
    --writer, -w          Add a writer to cerebro
    --wrcsv, -wc          Enable CSV Output in the writer
    --plot, -p            Plot the read data
    --numfigs NUMFIGS, -n NUMFIGS
                          Plot using numfigs figures

A test invocation::

  $ ./relative-volume.py --plot

Generates this chart:

.. thumbnail:: ./bar-synchronization.png

The code for the script.

.. literalinclude:: ./relative-volume.py
   :language: python
   :lines: 21-
