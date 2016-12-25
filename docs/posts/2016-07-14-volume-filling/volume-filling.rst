
.. post:: Jul 14, 2016
   :author: mementum
   :image: 1
   :excerpt: 2

Volume Filling
##############

Up until now the default volume filling strategy in *backtrader* has been
rather simple and straightforward:

  - Ignore volume

.. note::

    Jul 15, 2016

    Corrected a bug in the implementation and updated the sample to
    ``close`` the position and repeat after a break.

    The last test run below (and the corresponding chart) are from the
    update sample

This is based on 2 premises:

  - Trade in markets liquid enough to fully absorb *buy/sell* orders in one go
  - Real volume matching requires a real wolrd

    A quick example is a ``Fill or Kill`` order. Even down to the *tick*
    resolution and with enough volume for a *fill*, the *backtrader* broker
    cannot know how many extra actors happen to be in the market to
    discriminate if such an order would be or would not be matched to stick to
    the ``Fill`` part or if the order should be ``Kill``


But with release ``1.5.2.93`` it is possible to specify a ``filler`` for the
*broker* to take *Volume* into account when executing an order. Additionally 3
initial fillers have made it into the release:

  - ``FixedSize``: uses a fixed matching size (for example: 1000 units) each
    day, provided the current bar has at least 1000 units

  - ``FixedBarPerc``: uses a percentage of the total bar volume to try to match
    the order

  - ``BarPointPerc``: does a uniform distribution of the bar volume across the
    price range high-low and uses a percentage of the volume that would
    correspond to a single price point

Creating a filler
=================

A *filler* in the *backtrader* ecosystem can be any *callable* which matches
the following signature::

  callable(order, price, ago)

Where:

  - ``order`` is the order which is going to be executed

    This object gives access to the ``data`` object which is the target of the
    operation, creation sizes/prices, execution prices/sizes/remaining sizes
    and other details

  - ``price`` at which the order is going to be executed

  - ``ago`` is the index to the ``data`` in the *order* in which to look for
    the volume and price elements

    In almost all cases this will be ``0`` (current point in time) but in a
    corner case to cover ``Close`` orders this may be ``-1``

    To for example access the bar volume do::

      barvolume = order.data.volume[ago]

The callable can be a function or for example an instance of a class
supporting the ``__call__`` method, like in::

  class MyFiller(object):
      def __call__(self, order, price, ago):
          pass

Adding a Filler to the broker
=============================

The most straightforward method is to use the ``set_filler``::

  import backtrader as bt

  cerebro = Cerebro()
  cerebro.broker.set_filler(bt.broker.filler.FixedSize())

The second choice is to completely replace the ``broker``, although this is
probably only meant for subclasses of ``BrokerBack`` which have rewritten
portions of the functionality::

  import backtrader as bt

  cerebro = Cerebro()
  filler = bt.broker.filler.FixedSize()
  newbroker = bt.broker.BrokerBack(filler=filler)
  cerebro.broker = newbroker

The sample
==========

The *backtrader* sources contain a sample named ``volumefilling`` which allows
to test some of the integrated ``fillers`` (initially all)

The sample uses a default data sample in the sources named:
``datas/2006-volume-day-001.txt``.

For example a run with no filler::

  $ ./volumefilling.py --stakeperc 20.0

Output::

  Len,Datetime,Open,High,Low,Close,Volume,OpenInterest
  0001,2006-01-02,3602.00,3624.00,3596.00,3617.00,164794.00,1511674.00
  ++ STAKE VOLUME: 32958.0
  -- NOTIFY ORDER BEGIN
  Ref: 1
  ...
  Alive: False
  -- NOTIFY ORDER END
  -- ORDER REMSIZE: 0.0
  ++ ORDER COMPLETED at data.len: 2
  0002,2006-01-03,3623.00,3665.00,3614.00,3665.00,554426.00,1501792.00
  ...

Much of the input has been skipped because it is rather verbose, but the
summary is:

  - Upon seeing the 1st bar ``20%`` (*--stakeperc 20.0*) will be used to issue
    a *buy* order

  - As seen in the output and with the default behaviour of *backtrader* the
    order has been completely matched in a single shot. No look at the volume
    has been performed

.. note:: The broker has an insane amount of cash allocated in the sample to
	  make sure it can withstand many test situations

Another run with the ``FixedSize`` volume filler and a maximum of ``1000``
units per bar::

  $ ./volumefilling.py --stakeperc 20.0 --filler FixedSize --filler-args size=1000

Ouutput::

  Len,Datetime,Open,High,Low,Close,Volume,OpenInterest
  0001,2006-01-02,3602.00,3624.00,3596.00,3617.00,164794.00,1511674.00
  ++ STAKE VOLUME: 32958.0
  -- NOTIFY ORDER BEGIN
  ...
  -- NOTIFY ORDER END
  -- ORDER REMSIZE: 0.0
  ++ ORDER COMPLETED at data.len: 34
  0034,2006-02-16,3755.00,3774.00,3738.00,3773.00,502043.00,1662302.00
  ...

Now:

  - The chosen volume remains the same at ``32958``

  - Execution is completed at bar ``34`` which seems reasonable because from
    bar 2 to 34 ... 33 bars have been seen. With ```1000`` units matched per
    bar 33 bars are obviously needed to complete the execution

This is not a great achievement, so let's go for ``FixedBarPerc``::

  $ ./volumefilling.py --stakeperc 20.0 --filler FixedBarPerc --filler-args perc=0.75

Output::

  ...
  -- NOTIFY ORDER END
  -- ORDER REMSIZE: 0.0
  ++ ORDER COMPLETED at data.len: 11
  0011,2006-01-16,3635.00,3664.00,3632.00,3660.00,273296.00,1592611.00
  ...

This time:

  - Skipping the start, still ``32958`` units for the order

  - The execution uses 0.75% of the bar volume to match the request.

  - It takes from bar 2 to 11 (10 bars) to complete.

This is more interesting, but let's see what happens now with a more dynamic
volume allocation with ``BarPointPerc``::

  $ ./volumefilling.py --stakeperc 20.0 --filler BarPointPerc --filler-args minmov=1.0,perc=10.0

Output::

  ...
  -- NOTIFY ORDER END
  -- ORDER REMSIZE: 0.0
  ++ ORDER COMPLETED at data.len: 22
  0022,2006-01-31,3697.00,3718.00,3681.00,3704.00,749740.00,1642003.00
  ...

What happens is:

  - Same initial allocation (skipped) to the order of ``32958`` as size

  - It takes from 2 to 22 to fully execute (21 bars)

  - The *filler* has used a ``minmov`` of ``1.0`` (*minimum price movement of
    the asset*) to uniformly distribute the volume amongst the high-low range

  - A ``10%`` of the volumed assigned to a given price point is used for order
    matching


For anyone interested in how the order is being matched partially at each bar,
examining the full output of a run may be worth the time.

.. update:: Jul 15, 2016

	    Run with corrected bug in 1.5.3.93 and updated sample to ``close``
	    the operation after a break

The cash is increased to an even insaner amount to avoid margin calls and
plotting is enabled::

  $ ./volumefilling.py --filler FixedSize --filler-args size=10000 --stakeperc 10.0 --plot --cash 500e9

Rather than looking at the output which is extremely verbose, let's look at the
chart which already tells the story.

.. thumbnail:: volumefilling.png


Usage of the sample::

  usage: volumefilling.py [-h] [--data DATA] [--cash CASH]
                          [--filler {FixedSize,FixedBarPerc,BarPointPerc}]
                          [--filler-args FILLER_ARGS] [--stakeperc STAKEPERC]
                          [--opbreak OPBREAK] [--fromdate FROMDATE]
                          [--todate TODATE] [--plot]

  Volume Filling Sample

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA           Data to be read in (default: ../../datas/2006-volume-
                          day-001.txt)
    --cash CASH           Starting cash (default: 500000000.0)
    --filler {FixedSize,FixedBarPerc,BarPointPerc}
                          Apply a volume filler for the execution (default:
                          None)
    --filler-args FILLER_ARGS
                          kwargs for the filler with format:
                          arg1=val1,arg2=val2... (default: None)
    --stakeperc STAKEPERC
                          Percentage of 1st bar to use for stake (default: 10.0)
    --opbreak OPBREAK     Bars to wait for new op after completing another
                          (default: 10)
    --fromdate FROMDATE, -f FROMDATE
                          Starting date in YYYY-MM-DD format (default: None)
    --todate TODATE, -t TODATE
                          Ending date in YYYY-MM-DD format (default: None)
    --plot                Plot the result (default: False)


The code
--------

.. literalinclude:: ./volumefilling.py
   :language: python
   :lines: 21-
