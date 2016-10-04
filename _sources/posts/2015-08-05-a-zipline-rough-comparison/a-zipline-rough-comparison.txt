
A rough Zipline comparison
--------------------------

.. post:: Aug 5, 2015
   :author: mementum
   :image: 1
   :redirect: posts/2015-08-05

This "rough" and "quick" comparison hast its origin in an issue opened in
GitHub, `Issue #7 <https://github.com/mementum/backtrader/issues/7>`_ asks about
the differences with Quantopian's `Zipline
<https://github.com/quantopian/zipline>`_.

The ``Zipline`` platform is listed in the ``backtrader`` `README.rst
<https://github.com/mementum/backtrader>`_ as an open source alternative to
``backtrader``

Open Source is not a war (at least for me) and if anyone finds the API, ways of
doing things, naming conventions or others better in ``Zipline``, I will not
preach to move him/her away from that platform or any other.

And additionally ... if time and effort have been long invested in another
platform, no matter which advantages may ``backtrader`` have, moving to it may
not be worth the efffort.

As I have never ever used ``Zipline`` before and becauseI know ``backtrader``
from the inside out it would be unfair to compare in terms of this is better and
this is not.

Given there is a **Getting Started** guide for ``Zipline`` available at `Zipline
beginner tutorial <http://www.zipline.io/tutorial/>`_, I can comment as what
difference I perceive when I look at this tutorial.

Approach
========
  - ``Zipline`` seems to be module and function based. An algorithm must define
    ``initialize`` and ``handle_data`` in a module and will get a ``context``
    variable.

    In the good old times of C programming this was called Poor Man Object
    Orientend Programming. Not "poor" by any means. It was a good way to use the
    OOP advantages in a language/environment which didn't provide the means

  - ``backtrader`` has in contrast an OOP approach. The **algorithm** (strategy)
    is an object which is self-contained

    A subclass of ``backtrader.Strategy`` is needed. A single module can contain
    a collection of such classes.

    The final operative details are ver similar:

      - Declare indicators and others in ``__init__``
      - Evaluate the logic in ``next`` for each incoming data

It's possibly a matter of taste whether to go for a full OOP approach or stick
to functions.

Plotting
========

Not knowing if ``Zipline`` offers a simplified interface to ``matplotlib``, but
the tutorial shows a very manual approach to plotting.

``backtrader`` has plotting automated, fully integrated and features a simple
control interface for what's get plotted and what not (giving the user full
control)

Plotting is not the ultimate goal of a backtesting platform but it can aid when
it comes down to identifying traits to try to improve an algorithm.

For examples of plotting in ``backtrader`` see:

  - `Visual Inspection: Plotting
    <http://backtrader.readthedocs.org/quickstart.html#visual-inspection-plotting>`_

  - `Extending an Indicator
    <http://blog.backtrader.com/posts/2015-07-20/extending-an-indicator/>`_


  - `Improving Commissions: Stocks vs Futures
    <http://blog.backtrader.com/posts/2015-07-31/commission-schemes-updated/>`_

And for reference on how to apply that to the ``Indicators``:

  - `Indicator plotting
    <http://backtrader.readthedocs.org/induse.html#indicator-plotting>`_

Data Flow
=========

One of the things I tried to achieve with ``backtrader`` was full freedom for
the end user in terms of ease of use.

From the ``Zipline`` tutorial::

  def initialize(context):
      # Register 2 histories that track daily prices,
      # one with a 100 window and one with a 300 day window
      add_history(100, '1d', 'price')
      add_history(300, '1d', 'price')

      context.i = 0

  def handle_data(context, data):
      # Skip first 300 days to get full windows
      context.i += 1
      if context.i < 300:
          return

The user is forced to:

  - Initialize a counter in the context
  - Inform the system to keep a **history** of bars
  - Implement a logic to skip a certain number of bars

Here ``backtrader`` tries to help in that those 3 actions are not user
implemented.

  - If an indicator like a *Simple Moving Average* of period 300 is declared,
    the system will not call the ``next`` method of a strategy until 300 bars
    are available and the *Simple Moving Average* has been able to produce the
    1st value

  - If several indicators are declared, the largest of the periods will
    determine when the ``next`` method gets first called

Of course a user (for whatever reason) wants to override this, there are two
ways to get early access to the bars (even without the indicators having
produced a single output value)

  - Declare a ``prenext`` method which will be called until ``next`` is called

or

  - use the method ``setminperiod`` to set the number of bars to skip

The automatic behavior is of course fully recommended.

.. note::
   ``backtrader`` supports mixing different timeframes datas in a single
   run. Larger timeframe datas will of course push the first invocation of
   ``next`` further into the future according to the declared indicators

Example for ``backtrader``::

  import backtrader as bt
  import backtrader.indicators as btind

  class SMACrossOver(bt.Strategy):
      params = (('period1', 100), ('period2', 300))

      def __init__(self):

          self.sma1 = btind.SMA(period=self.params.period1)
          self.sma2 = btind.SMA(period=self.params.period2)

      def next(self):
          # not called until enough bars have elapsed.
          # with the default parameters from above: 300 bars

          # implement your logic here
          pass

Indicator declaration and Logic implementation
==============================================

From the zipline tutorial::

    def initialize(context):
        # Register 2 histories that track daily prices,
        # one with a 100 window and one with a 300 day window
        add_history(100, '1d', 'price')
        add_history(300, '1d', 'price')

        ...

    def handle_data(context, data):
        ...

        # Compute averages
        # history() has to be called with the same params
        # from above and returns a pandas dataframe.
        short_mavg = history(100, '1d', 'price').mean()
        long_mavg = history(300, '1d', 'price').mean()

The averages are being "calculated"/"declared"/"call it x" during the
``handle_data`` phase, which should only care about logic issues. This also
decouples the ``add_history`` from the ``history``

Obviously (without having looked into the details), ``history`` returns and
object which provides functions like ``mean``.

The declaration in ``backtrader`` (repeating from above just the ``__init__``
part) is a single one::

  class SMACrossOver(bt.Strategy):
      params = (('period1', 100), ('period2', 300))

      def __init__(self):

          self.sma1 = btind.SMA(period=self.params.period1)
          self.sma2 = btind.SMA(period=self.params.period2)

The actual logic implementation is similar, but ``backtrader`` can offer some
advantages when compared with the tutorial (again ... ``Zipline`` may offer
alternative methods similar to the ones shown below)

From the tutorial::

    def handle_data(context, data):
        ...

        # Trading logic
        if short_mavg[0] > long_mavg[0]:
            # order_target orders as many shares as needed to
            # achieve the desired number of shares.
            order_target(symbol('AAPL'), 100)
        elif short_mavg[0] < long_mavg[0]:
            order_target(symbol('AAPL'), 0)

``backtrader`` offers also the **[0]** notation to access the value. Sample next
implementation::

   def next(self):
       if self.sma1[0] > self.sma2[0]:
           self.buy()  # buys the main data feed passed to the system

       elif self.sma1[0] < self.sma2[0]:
           self.sell()  # sells the main data feed passed to the system

.. note::
   ``Zipline`` issues orders by fetching a ``symbol`` which looking at the
   tutorial means the end user can be analyzing NVDA and operating on AAPL
   (which is legit ... whether it makes sense or not ... there may be a
   correlation)

   ``backtrader`` operates on one of the data feeds which are present in the
   system (having been passed to a ``Cerebro`` instance). The default when
   nothing is indicated is to operate on the main ``data``, which is what common
   sense dictates makes more sense.

An even better approach in ``backtrader``::

   def next(self):
       if self.sma1 > self.sma2:
           self.buy()  # buys the main data feed passed to the system

       elif self.sma1 < self.sma2:
           self.sell()  # sells the main data feed passed to the system

The objects (indicators) can be compared directly, because operator overloading
has been implemented.

An even better alternative approach (in the author's modest opinion) is to
define the comparison logic during the ``__init__`` phase. Approach 1::

  class SMACrossOver(bt.Strategy):
      params = (('period1', 100), ('period2', 300))

      def __init__(self):

          sma1 = btind.SMA(period=self.params.period1)
          sma2 = btind.SMA(period=self.params.period2)

	  self.buysell = btind.Cmp(sma1, sma2)

   def next(self):
       if self.buysell > 0:
           self.buy()  # buys the main data feed passed to the system

       elif self.buysell < 0:
           self.sell()  # sells the main data feed passed to the system

And yet another possibility further using the already built-in operator
overloading::

  class SMACrossOver(bt.Strategy):
      params = (('period1', 100), ('period2', 300))

      def __init__(self):

          sma1 = btind.SMA(period=self.params.period1)
          sma2 = btind.SMA(period=self.params.period2)

	  self.buysig = sma1 > sma2
	  self.sellsig = sma1 < sma2

   def next(self):
       if self.buysig > 0:
           self.buy()  # buys the main data feed passed to the system

       elif self.sellsig < 0:
           self.sell()  # sells the main data feed passed to the system

There are other options like using the built-in ``CrossOver`` / ``CrossUp`` /
``CrossDown`` indicator family.

Data Recording
==============

This part of the ``Zipline`` tutorial has got me really puzzled::

    def handle_data(context, data):
        ...
        ...

        # Save values for later inspection
        record(AAPL=data[symbol('AAPL')].price,
               short_mavg=short_mavg[0],
               long_mavg=long_mavg[0])


``backtrader`` keeps the values of all datas, indicators, orders, trades and
statistics (growing area at the time of writing) always there for current or
later inspection.

Other things (not seen in the tutorial)
=======================================

I have to assume this are available in ``Zipline`` but not shown in the
tutorial:

  - Order notification (one thing is creating an order, but getting it accepted,
    executed and getting the execution price are different ones)

  - Trade notification (buy opens a trade, sell can or cannot close it ...)

  - Optimization using different parameters

  - Data Resampling

  - Data Replaying
