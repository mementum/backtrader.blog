
.. post:: Aug 27, 2015
   :author: mementum
   :image: 1
   :redirect: posts/2015-08-27
   :excerpt: 3

Real World Usage
################

Finally it seems it pays having gotten down to developing `backtrader`.

Following what seemed like the end of the world when looking at the European
markets in the last weeks, a friend asked if I could have a look at the data in
our charting package to see how the falling range compared against previous
similar occurrences.

Of course I could, but I said I could do more than looking into the charts,
because I could quickly:

  - Create a quick ``LegDown`` indicator to measure the range of the fall. It
    could also have gotten the name of ``HighLowRange`` or
    ``HiLoRange``. Luckily and in case this would be deemed needed, it can be
    solved via ``alias``

  - Create a ``LegDownAnalyzer`` that would gather the results and sort them

This led to an addtional request:

  - Recovery after the falls in the next 5, 10, 15, 20 days (trading ...)

    Solved with a ``LegUp`` indicator which writes the values back for alignment
    with the corresponding``LegDown``

The work was quickly done (within the allowance of my free time) and results
shared with the requester. But ... being the only problem tha I saw potential
for:

  - Improvements in the automation ``bt-run.py``

    - Multiple strategies/observers/analyzers with separated kwargs

    - Injection of indicators directly into Strategies with kwargs for each
      indicator

    - single plot argument accepting also kwargs

  - Improvements in in the ``Analyzer`` API to have automated **printing**
    capabilities for the results (which are returned as a ``dict`` -like
    instance) and have direct ``data`` access aliases

Notwithstanding that:

  - An obscure bug showed up due to the implementation combination I wrote to
    align the ``LegDown`` and ``LegUp`` values by mixing declaration of
    and the additional use of ``next``

    The bug had been introduced to simplify the passing of a single data with
    multiple ``Lines``, so that ``Indicators`` can operate on each of the lines
    as individual datas

The latter pushing me into:

  - Adding a background object opposite to ``LineDelay`` to "look" into the
    "future"

    That actually means that actual values are written into past array positions

Once all of the above were in place, it was time to retest how nicely the
(small?) challenges posed by the above request could be solved more easily and
faster (in implementation time).

Finally the execution and outcomes for the Eurostoxx 50 Future from 1998 up
until today::

  bt-run.py \
      --csvformat vchartcsv \
      --data ../datas/sample/1998-2015-estx50-vchart.txt \
      --analyzer legdownup \
      --pranalyzer \
      --nostdstats \
      --plot

  ====================
  == Analyzers
  ====================
  ##########
  legdownupanalyzer
  ##########
  Date,LegDown,LegUp_5,LegUp_10,LegUp_15,LegUp_20
  2008-10-10,901.0,331.0,69.0,336.0,335.0
  2001-09-11,889.0,145.0,111.0,239.0,376.0
  2008-01-22,844.0,328.0,360.0,302.0,344.0
  2001-09-21,813.0,572.0,696.0,816.0,731.0
  2002-07-24,799.0,515.0,384.0,373.0,572.0
  2008-01-23,789.0,345.0,256.0,319.0,290.0
  2001-09-17,769.0,116.0,339.0,405.0,522.0
  2008-10-09,768.0,102.0,0.0,120.0,208.0
  2001-09-12,764.0,137.0,126.0,169.0,400.0
  2002-07-23,759.0,331.0,183.0,285.0,421.0
  2008-10-16,758.0,102.0,222.0,310.0,201.0
  2008-10-17,740.0,-48.0,219.0,218.0,116.0
  2015-08-24,731.0,nan,nan,nan,nan
  2002-07-22,729.0,292.0,62.0,262.0,368.0
  ...
  ...
  ...
  2001-10-05,-364.0,228.0,143.0,286.0,230.0
  1999-01-04,-370.0,219.0,99.0,-7.0,191.0
  2000-03-06,-382.0,-60.0,-127.0,-39.0,-161.0
  2000-02-14,-393.0,-92.0,90.0,340.0,230.0
  2000-02-09,-400.0,-22.0,-46.0,96.0,270.0
  1999-01-05,-438.0,3.0,5.0,-107.0,5.0
  1999-01-07,-446.0,-196.0,-6.0,-82.0,-50.0
  1999-01-06,-536.0,-231.0,-42.0,-174.0,-129.0

The August 2015 leg down shows up at place 13th. Obviously a non-common
ocurrence although greater have happened.

What to do out of the follow up legs that point upwards is a lot more for
staticians and bright math minds than for me.

Details about the implementation (see the entire module code at the end) of the
``LegUpDownAnalyzer``:

  - It creates indicators in ``__init__`` just as other objects do:
    ``Strategies``, ``Indicators`` being usually the usual suspects

    These indicators get automatically registered to the strategy to which the
    analyzer is attached

  - Just like strategies the ``Analyzer`` has ``self.datas`` (an array of
    datas) and aliases to it: ``self.data``, ``self.data0``, ``self.data1`` ...

  - Again like strategies: ``nexstart`` and ``stop`` hooks (those are not present
    in indicators)

    In this case used to:

      - ``nextstart``: record the initial starting point of the strategy

      - ``stop``: making the final calculations because things are done

  - Note: other methods like ``start``, ``prenext`` and ``next`` are not needed
    in this case

  - The ``LegDownUpAnalyzer`` method ``print`` has been overriden to no longer
    call the ``pprint`` method but to create a CSV printout of the calculations

After much talk and since we added ``--plot`` to the mix ... the chart.

.. thumbnail:: real-wold-legupdown.png

Finally the ``legupdown`` module which is being loaded by ``bt-run``.

.. literalinclude:: ./legdownup.py
   :language: python
   :lines: 21-
