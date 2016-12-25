
.. post:: Apr 19, 2016
   :author: mementum
   :image: 1

Synchronizing different markets
###############################

The more the usage the more the mix of ideas and unexpected scenarios that
`backtrader` has to face. And with each new one, a challenge to see if the
platform can live up to the expectations set forth when development started,
flexibility and ease of use were the targets and *Python* was chosen as the
cornerstone.

`Ticket #76 <https://github.com/mementum/backtrader/issues/76>`_ raises the
question as to whether synchronizing markets with different trading calendars can
be done. Direct attempts to do so fail and the issue creator wonders why
``backtrader`` is not looking at the date.

Before any answer is delivered some thought has to be put into:

  - Behavior of indicators for the days which do not align

The answer to the latter is:

  - The platform is as much as possible ``date`` and ``time`` agnostic and will
    not look at the contents of the fields to evaluate those concepts

Taken into account the fact that stock market prices are ``datetime`` series
the above can hold up true up to certain limits. In the case of multiple datas
the following design considerations apply:

  - The 1st data added to ``cerebro`` is the ``datamaster``
  - All other datas have to be time aligned/synchronized with it never being
    able to overtake (in ``datetime`` terms) the ``datamaster``

Putting together the 3 bullet points from above delivers the mix experienced by
the issue creator. The scenario:

  - Calendar Year: ``2012``
  - Data 0: ``^GSPC`` (or S&P 500 for friends)
  - Data 1: ``^GDAXI`` (or Dax Index for friends)

Running a custom script to see how the data is synchronized by ``backtrader``::

  $ ./weekdaysaligner.py --online --data1 '^GSPC' --data0 '^GDAXI'

And the output::

  0001,  True, data0, 2012-01-03T23:59:59, 2012-01-03T23:59:59, data1
  0002,  True, data0, 2012-01-04T23:59:59, 2012-01-04T23:59:59, data1
  0003,  True, data0, 2012-01-05T23:59:59, 2012-01-05T23:59:59, data1
  0004,  True, data0, 2012-01-06T23:59:59, 2012-01-06T23:59:59, data1
  0005,  True, data0, 2012-01-09T23:59:59, 2012-01-09T23:59:59, data1
  0006,  True, data0, 2012-01-10T23:59:59, 2012-01-10T23:59:59, data1
  0007,  True, data0, 2012-01-11T23:59:59, 2012-01-11T23:59:59, data1
  0008,  True, data0, 2012-01-12T23:59:59, 2012-01-12T23:59:59, data1
  0009,  True, data0, 2012-01-13T23:59:59, 2012-01-13T23:59:59, data1
  0010, False, data0, 2012-01-17T23:59:59, 2012-01-16T23:59:59, data1
  0011, False, data0, 2012-01-18T23:59:59, 2012-01-17T23:59:59, data1
  ...

As soon as ``2012-01-16`` the trading calendars diverge. The ``data0`` is the
``datamaster`` (``^GSPC``) and even if ``data1`` (``^GDAXI``) would have a bar
to deliver on ``2012-01-16``, **this wasn't a trading day** for the *S&P 500*.

The best that ``backtrader`` can do with the aforementioned design restrictions
when the next trading day for the ``^GSPC`` comes in, the ``2012-01-17`` is
deliver the next not yet processed date for ``^GDAXI`` which is the
``2012-01-16``.

And the synchronization problem accumulates with each diverging day. At the end
of ``2012`` it looks like follows::

  ...
  0249, False, data0, 2012-12-28T23:59:59, 2012-12-19T23:59:59, data1
  0250, False, data0, 2012-12-31T23:59:59, 2012-12-20T23:59:59, data1

The reason should be obvious: *the Europeans trade more days than the
Americans*.

In the `Ticket #76 <https://github.com/mementum/backtrader/issues/76>` the
poster shows what ``zipline`` does. Let's look at the ``2012-01-13`` -
``2012-01-17`` conundrum::

  0009 : True : 2012-01-13 : close 1289.09 - 2012-01-13 :  close 6143.08
  0010 : False : 2012-01-13 : close 1289.09 - 2012-01-16 :  close 6220.01
  0011 : True : 2012-01-17 : close 1293.67 - 2012-01-17 :  close 6332.93

Blistering barnacles! The data for ``2012-01-13`` has been simply
**duplicated** without apparently asking the user for permission. Imho, this
shouldn't be because the end user of the platform cannot undo this spontaneous
addition.

.. note:: Except for a brief look at ``zipline``, the author doesn't know if
	  this is the standard behavior, configured by the script developer and
	  if it can be undone

Once we have seen that the *others* let's try again with ``backtrader`` using
the accumulated wisdom: *the Europeans trade more often than the
Americans*. Let's reverse the roles of ``^GSPC`` and ``^GDAXI`` and see the
outcome::

  $ ./weekdaysaligner.py --online --data1 '^GSPC' --data0 '^GDAXI'

The output (skipping to ``2012-01-13`` directly)::

  ...
  0009,  True, data0, 2012-01-13T23:59:59, 2012-01-13T23:59:59, data1
  0010, False, data0, 2012-01-16T23:59:59, 2012-01-13T23:59:59, data1
  0011,  True, data0, 2012-01-17T23:59:59, 2012-01-17T23:59:59, data1
  ...

Blistering barnacles again! ``backtrader`` has also *duplicated* the
``2012-01-13`` value for ``data1`` (in this case ``^GSPC``) as a match for
``data0`` (now ``^GDAXI``) delivery of ``2012-01-16``.

And even better:

  - Synchronization is reachieved with the next date: ``2012-01-17``

The same re-synchronization is seen again soon::

  ...
  0034,  True, data0, 2012-02-17T23:59:59, 2012-02-17T23:59:59, data1
  0035, False, data0, 2012-02-20T23:59:59, 2012-02-17T23:59:59, data1
  0036,  True, data0, 2012-02-21T23:59:59, 2012-02-21T23:59:59, data1
  ...

Followed by not such an easy re-sync::

  ...
  0068,  True, data0, 2012-04-05T23:59:59, 2012-04-05T23:59:59, data1
  0069, False, data0, 2012-04-10T23:59:59, 2012-04-09T23:59:59, data1
  ...
  0129, False, data0, 2012-07-04T23:59:59, 2012-07-03T23:59:59, data1
  0130,  True, data0, 2012-07-05T23:59:59, 2012-07-05T23:59:59, data1
  ...

Such episodes keep repeating until the last bar for ``^GDAXI`` is delivered::

  ...
  0256,  True, data0, 2012-12-31T23:59:59, 2012-12-31T23:59:59, data1
  ...

The reason for this *synchronization* issues is that ``backtrader`` does NOT
duplicate the data.

  - Once the ``datamaster`` has delivered a new bar the other ``datas`` are
    asked to deliver

  - If no bar can be delivered for the current ``datetime`` of the
    ``datamaster`` (because it, for example, would be overtaken) the next best
    data is, so to say, *re-delivered*

    And this is a bar with an already seen ``date``

Proper Synchronization
^^^^^^^^^^^^^^^^^^^^^^

But not all hope is lost. ``backtrader`` can deliver. Let's use
**filters**. This piece of technology in ``backtrader`` allows manipulating the
data before it hits the deepest parts of the platform and for example
*indicators* are calculated.

.. note:: ``delivering`` is a perception matter and therefore what
	  ``backtrader`` delivers may not be what the recipient is expecting as
	  the ``delivery``

The actual code

.. literalinclude:: ./weekdaysfiller.py
   :language: python
   :lines: 21-

The test script is already fitted with the capability to use it::

  $ ./weekdaysaligner.py --online --data0 '^GSPC' --data1 '^GDAXI' --filler

With ``--filler`` the ``WeekDaysFiller`` is added to both ``data0`` and
``data1``. And the output::

  0001,  True, data0, 2012-01-03T23:59:59, 2012-01-03T23:59:59, data1
  ...
  0009,  True, data0, 2012-01-13T23:59:59, 2012-01-13T23:59:59, data1
  0010,  True, data0, 2012-01-16T23:59:59, 2012-01-16T23:59:59, data1
  0011,  True, data0, 2012-01-17T23:59:59, 2012-01-17T23:59:59, data1
  ...

The 1st *conundrum* at ``2012-01-13`` - ``2012-01-17`` is gone. And the entire
set is *synchronized*::

  ...
  0256,  True, data0, 2012-12-25T23:59:59, 2012-12-25T23:59:59, data1
  0257,  True, data0, 2012-12-26T23:59:59, 2012-12-26T23:59:59, data1
  0258,  True, data0, 2012-12-27T23:59:59, 2012-12-27T23:59:59, data1
  0259,  True, data0, 2012-12-28T23:59:59, 2012-12-28T23:59:59, data1
  0260,  True, data0, 2012-12-31T23:59:59, 2012-12-31T23:59:59, data1

Something worth noticing:

  - With ``^GSPC`` as ``data0`` we had ``250`` lines (the index traded ``250`` days in
    ``2012``)

  - With ``^GDAXI`` we ``data0`` had ``256`` lines (the index traded ``256`` days in
    ``2012``)

  - And with the ``WeekDaysFiller`` in place the length of both *datas* has
    been extended to ``260``

    Adding ``52`` * ``2`` (weekends and days in a weekend), we would end up
    with ``364``. The remaining day until the regular ``365`` days in a year
    was for sure a *Saturday* or a *Sunday*.

The *filter* is *filling* with ``NaN`` values for the days in which no trading
took place for the given data. Let's plot it::

  $ ./weekdaysaligner.py --online --data0 '^GSPC' --data1 '^GDAXI' --filler --plot

.. thumbnail:: gspc-gdaxi-synced.png

Filled days are quite obvious:

  - The gap in between bars is there
  - The gap is even more obvious for the *volume* plot

A 2nd plot will try to answer the question at the top: *what happens with
indicators?*. Remember that the new bars have been given a value of ``NaN``
(that's why they are not displayed)::

  $ ./weekdaysaligner.py --online --data0 '^GSPC' --data1 '^GDAXI' --filler --plot --sma 10

.. thumbnail:: gspc-gdaxi-synced-broken-sma.png

Re-blistering barnacles! The *Simple Moving Average* has broken the space time
continuum and jumps some bars with no solution of continuity. This is of course
the effect of filling up with *Not a Number* aka ``NaN``: *mathematic
operations no longer make sense*.

If instead of ``NaN`` the last seen closing price is used::

  $ ./weekdaysaligner.py --online --data0 '^GSPC' --data1 '^GDAXI' --filler --plot --sma 10 --fillclose

The plot looks a lot nicer with a regular *SMA* for the entire 260 days

.. thumbnail:: gspc-gdaxi-synced-good-sma.png


Conclusion
^^^^^^^^^^

Synchronizing two instruments with different trading calendars is a matter of
making decisions and compromises. ``backtrader`` needs time aligned data to
work with multiple datas and different trading calendars don't help.

The use of the ``WeekDaysFiller`` described here can alleviate the situation
but it is by no means a universal panacea, because with which values to fill is
a matter of long and prolonged consideration.

Script Code and Usage
^^^^^^^^^^^^^^^^^^^^^

Available as sample in the sources of ``backtrader``::

  $ ./weekdaysaligner.py --help
  usage: weekdaysaligner.py [-h] [--online] --data0 DATA0 [--data1 DATA1]
                            [--sma SMA] [--fillclose] [--filler] [--filler0]
                            [--filler1] [--fromdate FROMDATE] [--todate TODATE]
                            [--plot]

  Sample for aligning with trade

  optional arguments:
    -h, --help            show this help message and exit
    --online              Fetch data online from Yahoo (default: False)
    --data0 DATA0         Data 0 to be read in (default: None)
    --data1 DATA1         Data 1 to be read in (default: None)
    --sma SMA             Add a sma to the datas (default: 0)
    --fillclose           Fill with Close price instead of NaN (default: False)
    --filler              Add Filler to Datas 0 and 1 (default: False)
    --filler0             Add Filler to Data 0 (default: False)
    --filler1             Add Filler to Data 1 (default: False)
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format (default:
                          2012-01-01)
    --todate TODATE, -t TODATE
                          Ending date in YYYY-MM-DD format (default: 2012-12-31)
    --plot                Do plot (default: False)


The code:

.. literalinclude:: ./weekdaysaligner.py
   :language: python
   :lines: 21-
