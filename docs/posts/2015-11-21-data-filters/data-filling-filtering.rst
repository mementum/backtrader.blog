
.. post:: Nov 21, 2015
   :author: mementum
   :image: 1

Data Filters
############

Some time ago `Ticket #23 <https://github.com/mementum/backtrader/issues/23>`_
got me thinking about a potential improvement for the discussion which was held
in the context of that ticket.

Within the ticket I added a ``DataFilter`` class, but this was overly
complicated. Actually reminiscent of the complexity which was built in
``DataResampler`` and ``DataReplayer``, the classes used to implement the
functionalities of the same names.

As such and since a couple of versions, ``backtrader`` supports adding a
``filter`` (call it ``processor`` if you wish) to data feeds. Resampling and
Replaying were internally reimplemented using the functionality and everything
seems less complicated (although it still is)

Filters at work
+++++++++++++++

Given an existing data feed/source you use the ``addfilter`` method of the data
feed::

  data = MyDataFeed(name=myname)

  data.addfilter(filter, *args, **kwargs)

Obviously the ``filter`` must conform to a given interface, being this:

  - A callable which accepts this signature::

      callable(data, *args, **kwargs)

  or

  - A class which can be instantiated and called

    - During instantiation the __init__ method must support the signature::

        def __init__(self, data, *args, **kwargs)

    - The __call__ and last methods this one::

        def __call__(self, data)

	def last(self, data)

The callable/instance will be called for each data the data source is producing.


A better solution for Ticket #23
++++++++++++++++++++++++++++++++

That ticket wanted:

  - A RelativeVolumeIndicator on an intraday basis

  - Intraday data may be missing

  - Pre/Post Session data could arrive

Implementing a couple of filters alleviates the situation for a backtesting
environment.

Filtering out Pre/Post Market Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following filter (already available in ``backtrader``) comes to the rescue::

  class SessionFilter(with_metaclass(metabase.MetaParams, object)):
      '''
      This class can be applied to a data source as a filter and will filter out
      intraday bars which fall outside of the regular session times (ie: pre/post
      market data)

      This is a "non-simple" filter and must manage the stack of the data (passed
      during init and __call__)

      It needs no "last" method because it has nothing to deliver
      '''
      def __init__(self, data):
          pass

      def __call__(self, data):
          '''
          Return Values:

            - False: data stream was not touched
            - True: data stream was manipulated (bar outside of session times and
            - removed)
          '''
          if data.sessionstart <= data.datetime.tm(0) <= data.sessionend:
              # Both ends of the comparison are in the session
              return False  # say the stream is untouched

          # bar outside of the regular session times
          data.backwards()  # remove bar from data stack
          return True  # signal the data was manipulated


The filter uses the in-the-data embedded session start/end times to filter
bars

  - If the datetime of the new data is within the session times ``False`` is
    returned to indicate the data is untouched

  - If the datatime falls outside of the range, the data source is sent
    ``backwards`` effectively erasing the last produced data. And ``True`` is
    returned to indicate the data stream was manipulated.

.. note:: Calling ``data.backwards()`` is possibly/probably low level and the
	  filters should have an API which deals with the internals of the data
	  stream


The sample code at the end of the script can be run with and without filter. The
first run is 100% unfiltered and without specifying session times::

  $ ./data-filler.py --writer --wrcsv

Looking at the start and end of the 1st day::

  ===============================================================================
  Id,2006-01-02-volume-min-001,len,datetime,open,high,low,close,volume,openinterest,Strategy,len
  1,2006-01-02-volume-min-001,1,2006-01-02 09:01:00,3602.0,3603.0,3597.0,3599.0,5699.0,0.0,Strategy,1
  2,2006-01-02-volume-min-001,2,2006-01-02 09:02:00,3600.0,3601.0,3598.0,3599.0,894.0,0.0,Strategy,2
  ...
  ...
  581,2006-01-02-volume-min-001,581,2006-01-02 19:59:00,3619.0,3619.0,3619.0,3619.0,1.0,0.0,Strategy,581
  582,2006-01-02-volume-min-001,582,2006-01-02 20:00:00,3618.0,3618.0,3617.0,3618.0,242.0,0.0,Strategy,582
  583,2006-01-02-volume-min-001,583,2006-01-02 20:01:00,3618.0,3618.0,3617.0,3617.0,15.0,0.0,Strategy,583
  584,2006-01-02-volume-min-001,584,2006-01-02 20:04:00,3617.0,3617.0,3617.0,3617.0,107.0,0.0,Strategy,584
  585,2006-01-02-volume-min-001,585,2006-01-03 09:01:00,3623.0,3625.0,3622.0,3624.0,4026.0,0.0,Strategy,585
  ...

The session run from 09:01:00 to 20:04:00 on the 2nd of January of 2006.

Now a run with a ``SessionFilter`` and telling the script to use 09:30 and 17:30
as the start/end times of the session::

  $ ./data-filler.py --writer --wrcsv --tstart 09:30 --tend 17:30 --filter

  ===============================================================================
  Id,2006-01-02-volume-min-001,len,datetime,open,high,low,close,volume,openinterest,Strategy,len
  1,2006-01-02-volume-min-001,1,2006-01-02 09:30:00,3604.0,3605.0,3603.0,3604.0,546.0,0.0,Strategy,1
  2,2006-01-02-volume-min-001,2,2006-01-02 09:31:00,3604.0,3606.0,3604.0,3606.0,438.0,0.0,Strategy,2
  ...
  ...
  445,2006-01-02-volume-min-001,445,2006-01-02 17:29:00,3621.0,3621.0,3620.0,3620.0,866.0,0.0,Strategy,445
  446,2006-01-02-volume-min-001,446,2006-01-02 17:30:00,3620.0,3621.0,3619.0,3621.0,1670.0,0.0,Strategy,446
  447,2006-01-02-volume-min-001,447,2006-01-03 09:30:00,3637.0,3638.0,3635.0,3636.0,1458.0,0.0,Strategy,447
  ...

The data output starts now at 09:30 and ends at 17:30. Pre/Post-Market Data has
been filtered out.

Filling in Missing Data
^^^^^^^^^^^^^^^^^^^^^^^

A deeper examination of the output shows the following::

  ...
  61,2006-01-02-volume-min-001,61,2006-01-02 10:30:00,3613.0,3614.0,3613.0,3614.0,112.0,0.0,Strategy,61
  62,2006-01-02-volume-min-001,62,2006-01-02 10:31:00,3614.0,3614.0,3614.0,3614.0,183.0,0.0,Strategy,62
  63,2006-01-02-volume-min-001,63,2006-01-02 10:34:00,3614.0,3614.0,3614.0,3614.0,841.0,0.0,Strategy,63
  64,2006-01-02-volume-min-001,64,2006-01-02 10:35:00,3614.0,3614.0,3614.0,3614.0,17.0,0.0,Strategy,64
  ...

Data for minutes 10:32 and 10:33 is missing. Being the 1st trading day of the
year there may have been no negotiation at all. Or the data feed may have failed
to capture that data.

For the purposes of Ticket #23 and to be able to compare the volume of a given
minute with the same minute of the previous day, we'll be filling in the missing
data.

Already in ``backtrader`` there is a ``SessionFiller`` which as expected fills
in missing data. The code is long and bears more complexities than that of a
filter (see at the end for the full implementation), but let's see the
class/params definition::

  class SessionFiller(with_metaclass(metabase.MetaParams, object)):
      '''
      Bar Filler for a Data Source inside the declared session start/end times.

      The fill bars are constructed using the declared Data Source ``timeframe``
      and ``compression`` (used to calculate the intervening missing times)

      Params:

        - fill_price (def: None):

          If None is passed, the closing price of the previous bar will be
          used. To end up with a bar which for example takes time but it is not
          displayed in a plot ... use float('Nan')

        - fill_vol (def: float('NaN')):

          Value to use to fill the missing volume

        - fill_oi (def: float('NaN')):

          Value to use to fill the missing Open Interest

        - skip_first_fill (def: True):

          Upon seeing the 1st valid bar do not fill from the sessionstart up to
          that bar
      '''
      params = (('fill_price', None),
                ('fill_vol', float('NaN')),
                ('fill_oi', float('NaN')),
                ('skip_first_fill', True))


The sample script can now filter and fill data::

  ./data-filler.py --writer --wrcsv --tstart 09:30 --tend 17:30 --filter --filler

  ...
  62,2006-01-02-volume-min-001,62,2006-01-02 10:31:00,3614.0,3614.0,3614.0,3614.0,183.0,0.0,Strategy,62
  63,2006-01-02-volume-min-001,63,2006-01-02 10:32:00,3614.0,3614.0,3614.0,3614.0,0.0,,Strategy,63
  64,2006-01-02-volume-min-001,64,2006-01-02 10:33:00,3614.0,3614.0,3614.0,3614.0,0.0,,Strategy,64
  65,2006-01-02-volume-min-001,65,2006-01-02 10:34:00,3614.0,3614.0,3614.0,3614.0,841.0,0.0,Strategy,65
  ...

Minutes 10:32 and 10:33 are there. The script uses the last known "close" price
to fill the price values and sets the volume and openinterest fields to 0. The
script accepts a ``--fvol`` argument to set the volume to anything (including
'NaN')

Completing Ticket #23
^^^^^^^^^^^^^^^^^^^^^

With the ``SessionFilter`` and ``SessionFiller`` the following has been
completed:

  - Pre/Post Market Data is not delivered

  - No Data (for the given timeframe) is missing

Now the "synchronization" discussed in Ticket 23 to implement a
``RelativeVolume`` indicator is no longer needed, because all days have exactly
the same number of bars (in the example all minutes from 09:30 to 17:30 both
included)

Remembering that the default is to set the missing volume to ``0`` an easy
``RelativeVolume`` indicator can be developed::

  class RelativeVolume(bt.Indicator):
      csv = True  # show up in csv output (default for indicators is False)

      lines = ('relvol',)
      params = (
          ('period', 20),
          ('volisnan', True),
      )

      def __init__(self):
          if self.p.volisnan:
              # if missing volume will be NaN, do a simple division
              # the end result for missing volumes will also be NaN
              relvol = self.data.volume(-self.p.period) / self.data.volume
          else:
              # Else do a controlled Div with a built-in function
              relvol = bt.DivByZero(
                  self.data.volume(-self.p.period),
                  self.data.volume,
                  zero=0.0)

          self.lines.relvol = relvol


Which is smart enough to avoid a division by zero by using a built-in aid in
``backtrader``.

Putting all pieces together in the next invocation of the script::

  ./data-filler.py --writer --wrcsv --tstart 09:30 --tend 17:30 --filter --filler --relvol

  ===============================================================================
  Id,2006-01-02-volume-min-001,len,datetime,open,high,low,close,volume,openinterest,Strategy,len,RelativeVolume,len,relvol
  1,2006-01-02-volume-min-001,1,2006-01-02 09:30:00,3604.0,3605.0,3603.0,3604.0,546.0,0.0,Strategy,1,RelativeVolume,1,
  2,2006-01-02-volume-min-001,2,2006-01-02 09:31:00,3604.0,3606.0,3604.0,3606.0,438.0,0.0,Strategy,2,RelativeVolume,2,
  ...

The ``RelativeVolume`` indicator produces no output, as expected, during the 1st
bars. The period is calculated in the script as: (17:30 - 09:30 * 60) + 1. Let's
directly look at how the relative volume looks for 10:32 and 10:33 in the second
day, given that the 1st day, the volume value was filled with ``0``::

  ...
  543,2006-01-02-volume-min-001,543,2006-01-03 10:31:00,3648.0,3648.0,3647.0,3648.0,56.0,0.0,Strategy,543,RelativeVolume,543,3.26785714286
  544,2006-01-02-volume-min-001,544,2006-01-03 10:32:00,3647.0,3648.0,3647.0,3647.0,313.0,0.0,Strategy,544,RelativeVolume,544,0.0
  545,2006-01-02-volume-min-001,545,2006-01-03 10:33:00,3647.0,3647.0,3647.0,3647.0,135.0,0.0,Strategy,545,RelativeVolume,545,0.0
  546,2006-01-02-volume-min-001,546,2006-01-03 10:34:00,3648.0,3648.0,3647.0,3648.0,171.0,0.0,Strategy,546,RelativeVolume,546,4.91812865497
  ...

It is set to ``0`` as expected for both.

Conclusion
^^^^^^^^^^

The ``filter`` mechanism in data sources opens the possibility to fully
manipulate the data stream. Use with caution.

Script Code and Usage
^^^^^^^^^^^^^^^^^^^^^

Available as sample in the sources of ``backtrader``::

  usage: data-filler.py [-h] [--data DATA] [--filter] [--filler] [--fvol FVOL]
                        [--tstart TSTART] [--tend TEND] [--relvol]
                        [--fromdate FROMDATE] [--todate TODATE] [--writer]
                        [--wrcsv] [--plot] [--numfigs NUMFIGS]

  DataFilter/DataFiller Sample

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA, -d DATA  data to add to the system
    --filter, -ft         Filter using session start/end times
    --filler, -fl         Fill missing bars inside start/end times
    --fvol FVOL           Use as fill volume for missing bar (def: 0.0)
    --tstart TSTART, -ts TSTART
                          Start time for the Session Filter (HH:MM)
    --tend TEND, -te TEND
                          End time for the Session Filter (HH:MM)
    --relvol, -rv         Add relative volume indicator
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format
    --todate TODATE, -t TODATE
                          Starting date in YYYY-MM-DD format
    --writer, -w          Add a writer to cerebro
    --wrcsv, -wc          Enable CSV Output in the writer
    --plot, -p            Plot the read data
    --numfigs NUMFIGS, -n NUMFIGS
                          Plot using numfigs figures

The code:

.. literalinclude:: ./data-filler.py
   :language: python
   :lines: 21-


SessionFiller
^^^^^^^^^^^^^

From the ``backtrader`` sources::

  class SessionFiller(with_metaclass(metabase.MetaParams, object)):
      '''
      Bar Filler for a Data Source inside the declared session start/end times.

      The fill bars are constructed using the declared Data Source ``timeframe``
      and ``compression`` (used to calculate the intervening missing times)

      Params:

        - fill_price (def: None):

          If None is passed, the closing price of the previous bar will be
          used. To end up with a bar which for example takes time but it is not
          displayed in a plot ... use float('Nan')

        - fill_vol (def: float('NaN')):

          Value to use to fill the missing volume

        - fill_oi (def: float('NaN')):

          Value to use to fill the missing Open Interest

        - skip_first_fill (def: True):

          Upon seeing the 1st valid bar do not fill from the sessionstart up to
          that bar
      '''
      params = (('fill_price', None),
                ('fill_vol', float('NaN')),
                ('fill_oi', float('NaN')),
                ('skip_first_fill', True))

      # Minimum delta unit in between bars
      _tdeltas = {
          TimeFrame.Minutes: datetime.timedelta(seconds=60),
          TimeFrame.Seconds: datetime.timedelta(seconds=1),
          TimeFrame.MicroSeconds: datetime.timedelta(microseconds=1),
      }

      def __init__(self, data):
          # Calculate and save timedelta for timeframe
          self._tdunit = self._tdeltas[data._timeframe] * data._compression

          self.seenbar = False  # control if at least one bar has been seen
          self.sessend = MAXDATE  # maxdate is the control for bar in session

      def __call__(self, data):
          '''
          Params:
            - data: the data source to filter/process

          Returns:
            - False (always) because this filter does not remove bars from the
          stream

          The logic (starting with a session end control flag of MAXDATE)

            - If new bar is over session end (never true for 1st bar)

              Fill up to session end. Reset sessionend to MAXDATE & fall through

            - If session end is flagged as MAXDATE

              Recalculate session limits and check whether the bar is within them

              if so, fill up and record the last seen tim

            - Else ... the incoming bar is in the session, fill up to it
          '''
          # Get time of current (from data source) bar
          dtime_cur = data.datetime.datetime()

          if dtime_cur > self.sessend:
              # bar over session end - fill up and invalidate
              self._fillbars(data, self.dtime_prev, self.sessend + self._tdunit)
              self.sessend = MAXDATE

          # Fall through from previous check ... the bar which is over the
          # session could already be in a new session and within the limits
          if self.sessend == MAXDATE:
              # No bar seen yet or one went over previous session limit
              sessstart = data.datetime.tm2datetime(data.sessionstart)
              self.sessend = sessend = data.datetime.tm2datetime(data.sessionend)

              if sessstart <= dtime_cur <= sessend:
                  # 1st bar from session in the session - fill from session start
                  if self.seenbar or not self.p.skip_first_fill:
                      self._fillbars(data, sessstart - self._tdunit, dtime_cur)

              self.seenbar = True
              self.dtime_prev = dtime_cur

          else:
              # Seen a previous bar and this is in the session - fill up to it
              self._fillbars(data, self.dtime_prev, dtime_cur)
              self.dtime_prev = dtime_cur

          return False

      def _fillbars(self, data, time_start, time_end, forcedirty=False):
          '''
          Fills one by one bars as needed from time_start to time_end

          Invalidates the control dtime_prev if requested
          '''
          # Control flag - bars added to the stack
          dirty = False

          time_start += self._tdunit
          while time_start < time_end:
              dirty = self._fillbar(data, time_start)
              time_start += self._tdunit

          if dirty or forcedirty:
              data._save2stack(erase=True)

      def _fillbar(self, data, dtime):
          # Prepare an array of the needed size
          bar = [float('Nan')] * data.size()

          # Fill datetime
          bar[data.DateTime] = date2num(dtime)

          # Fill the prices
          price = self.p.fill_price or data.close[-1]
          for pricetype in [data.Open, data.High, data.Low, data.Close]:
              bar[pricetype] = price

          # Fill volume and open interest
          bar[data.Volume] = self.p.fill_vol
          bar[data.OpenInterest] = self.p.fill_oi

          # Fill extra lines the data feed may have defined beyond DateTime
          for i in range(data.DateTime + 1, data.size()):
              bar[i] = data.lines[i][0]

          # Add tot he stack of bars to save
          data._add2stack(bar)

          return True
