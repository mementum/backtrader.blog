
.. post:: Sep 17, 2016
   :author: mementum
   :image: 1
   :excerpt: 2


Data Synchronization Rework
###########################

In the latest release the *minor* number has been moved from `8` to `9` to
indicate a change which may have some behavioral impact, regardless, even if
compatibility has been taken into account.

With release `1.9.0.99` the entire mechanism to synchronize multiple datas
using *datetime* has been reworked (for both *next* and *once* modes).

.. note:: All standard test cases get a nice OK from ``nosetests``, but complex
	  uses cases might uncover corner cases not covered.

The previous behavior was discussed in tickets
`#39 <https://github.com/mementum/backtrader/issues/39>`_,
`#76 <https://github.com/mementum/backtrader/issues/76>`_,
`#115 <https://github.com/mementum/backtrader/issues/115>`_ and
`#129 <https://github.com/mementum/backtrader/issues/129>`_ and this has been
the basis to deprecate the old behavior.

Now, the *datetime* timestamp of the incoming prices is checked to align datas
and deliver what's new (older bars first). Benefits:

  - Non time aligned data can now be used.

  - In live feeds the behavior improves because the re-synchronizes
    automatically

Let's recall that the old behavior used the 1st data introduced in the system
as a master for time synchronization and no other data could be faster. The
order of introduction of datas in the system plays no role now.

Part of the rework has addressed plotting which naively assumed all datas ended
up having the same length, being this a consequence of having a time
master. The new plotting code allows datas of different length.

.. note::

   The old behavior is still available by using::

     cerebro = bt.Cerebro(oldsync=True)

   or::

     cerebro.rund(oldsync=True)


Seeing it with a sample
***********************

The ``multidata-strategy`` sample has been used as the basis for the
``multidata-strategy-unaligned`` sample (in the same folder). Two data samples
have been manually altered to remove some bars. Both had ``756`` bars and have
been capped down to ``753`` at two different points in time

  - End of 2004, beginning of 2005 for ``YHOO``
  - End of 2005 for ``ORCL``

As always, a execution is worth a thousand words.

First the old behavior
======================

The execution::

  $ ./multidata-strategy-unaligned.py --oldsync --plot

From the output, the important part is right at the end::

  ...
  Self  len: 753
  Data0 len: 753
  Data1 len: 750
  Data0 len == Data1 len: False
  Data0 dt: 2005-12-27 23:59:59
  Data1 dt: 2005-12-27 23:59:59
  ...

To notice:

  - The *strategy* has a length of ``753``

  - The 1st data (time master) also has ``753``

  - The 2nd data (time slave) has ``750``

It's not obvious from the output but the ``YHOO`` file contains data up to
``2005-12-30``, which is not being processed by the system.


The visual chart

.. thumbnail:: multidata-oldsync.png

The new behavior
================

The execution::

  $ ./multidata-strategy-unaligned.py --plot

From the output, the important part is right at the end::

  ...
  Self  len: 756
  Data0 len: 753
  Data1 len: 753
  Data0 len == Data1 len: True
  Data0 dt: 2005-12-27 23:59:59
  Data1 dt: 2005-12-30 23:59:59
  ...

The behavior has obvioulsy improved:

  - The *strategy* goes to a length of ``756`` and each of the datas to the
    full ``753`` data points.

  - Because the removed data points don't overlap the strategy ends up being
    ``3`` units longer than the datas.

  - ``2005-12-30`` has been reached with ``data1`` (it's one of the data points
    removed for ``data0``), so all datas have been processed to the very end

The visual chart

.. thumbnail:: multidata-newsync.png

Although the charts do not exhibit major differences, they are actually
different behind the scenes.

Another check
*************

For the interested user, the ``data-multitimeframe`` sample has been updated to
also support a ``--oldsync`` parameter. Because now different length datas are
being plotted, the visual aspect of the larger time frame is better.

Execution with new synchronization model
========================================

.. thumbnail:: data-multitimeframe-newsync.png

Execution with old synchronization model
========================================

.. thumbnail:: data-multitimeframe-oldsync.png


Sample Usage
************
::

  $ ./multidata-strategy-unaligned.py --help
  usage: multidata-strategy-unaligned.py [-h] [--data0 DATA0] [--data1 DATA1]
                                         [--fromdate FROMDATE] [--todate TODATE]
                                         [--period PERIOD] [--cash CASH]
                                         [--runnext] [--nopreload] [--oldsync]
                                         [--commperc COMMPERC] [--stake STAKE]
                                         [--plot] [--numfigs NUMFIGS]

  MultiData Strategy

  optional arguments:
    -h, --help            show this help message and exit
    --data0 DATA0, -d0 DATA0
                          1st data into the system
    --data1 DATA1, -d1 DATA1
                          2nd data into the system
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format
    --todate TODATE, -t TODATE
                          Starting date in YYYY-MM-DD format
    --period PERIOD       Period to apply to the Simple Moving Average
    --cash CASH           Starting Cash
    --runnext             Use next by next instead of runonce
    --nopreload           Do not preload the data
    --oldsync             Use old data synchronization method
    --commperc COMMPERC   Percentage commission (0.005 is 0.5%
    --stake STAKE         Stake to apply in each operation
    --plot, -p            Plot the read data
    --numfigs NUMFIGS, -n NUMFIGS
                          Plot using numfigs figures


Sample Code
***********

.. literalinclude:: multidata-strategy-unaligned.py
   :language: python
   :lines: 21-
