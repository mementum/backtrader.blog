
.. post:: Nov 20, 2016
   :author: mementum
   :image: 1


Hidden Powers of Python (1)
###########################

It's only when meeting real users of *backtrader* when one can realize if the
abstractions and Python powers used in the platform make sense.

Without leaving the *pythonic* motto aside, *backtrader* tries to give the users
as much control as possible, whilst at the same time simplifying the usage by
putting into action the *hidden* powers that Python offers.

The first example in this the first post of a series.

Is it an array or what is it?
*****************************

A very quick example::

  import backtrader as bt

  class MyStrategy(bt.Strategy):

      def __init__(self):

          self.hi_lo_avg = (self.data.high + self.data.low) / 2.0

      def next(self):
          if self.hi_lo_avg[0] > another_value:
              print('we have a winner!')

  ...
  ...
  cerebro.addstrategy(MyStrategy)
  cerebro.run()


One of the questions that very quickly pops up is:

  - Couldn't one also use the ``[]`` during ``__init__``?.

The question being asked because the user has already tried and Python has
stopped running with an exception.

The answer:

  - No. Using ``[]`` is not meant during initialization.

With the next question being then:

  - So what's actually stored in ``self.hi_lo_avg`` during ``__init__`` if it's
    not an array?

And the answer is not puzzling for programmers but it may be for algo traders
who went for Python

  - It's a lazily evaluated object, which will calculate and deliver the values
    via the ``[]`` operator during the ``cerebro.run`` phase, i.e.: in the
    ``next`` method of the strategy.

Bottomline: in the ``next`` method the array indexing operator ``[]`` will give
you access to the calculated values for past and current time moments.

The secret is in the sauce
**************************

And *operator overriding* is the real sauce. Let's break down the calculation
of the *high-low-average*::

  self.hi_lo_avg = (self.data.high + self.data.low) / 2.0

The components:

  - ``self.data.high`` and ``self.data.low`` are themselves *objects* (*lines*
    in the *backtrader* naming scheme)

They are in many cases mistakenly taken for pure *arrays* but they are not. The
reasons for them being objects:

  - Implementation of the ``0`` and ``-1`` indexing scheme in place in
    *backtrader*
  - Control of the buffer sizing and linking to other objects

And the most important aspect in this case:

  - Overriding operators to return *objects*

And that why the operation below returns a *lines* object. Let's start::

  temp = self.data.high - self.data.low

The temporary object is then divided by ``2.0`` and assigned to the member
variable::

  self.hi_lo_avg = temp / 2.0

This agains returns another *lines* object. Because operator overriding
does not only apply to operations executed directly amongst *lines* objects,
but also to, for example, arithmetic operations like this division.

Which means that ``self.hi_lo_avg`` has a reference to a *lines* object. This
object is useful in the ``next`` method of the strategy or as input to
*indicators* or other calculations.

A *logic operator* example
**************************

The example above used an arithmetic operator during ``__init__`` and later the
combination of ``[0]`` and a logic opertor, ``>`` in ``next``.

Because operator overriding is not limited to *arithmetic*, let's put another
example in place, adding an indicator to the mix. A first attempt would be::

  import backtrader as bt

  class MyStrategy(bt.Strategy):

      def __init__(self):
          self.hi_lo_avg = (self.data.high + self.data.low) / 2.0
	  self.sma = bt.indicators.SMA(period=30)

      def next(self):
          if self.hi_lo_avg[0] > self.sma[0]:
              print('we have a winner!')

  ...
  ...
  cerebro.addstrategy(MyStrategy)
  cerebro.run()

But in this case there is simply change from ``another_value`` to
``self.sma[0]``. Let's improve it::

  import backtrader as bt

  class MyStrategy(bt.Strategy):

      def __init__(self):
          self.hi_lo_avg = (self.data.high + self.data.low) / 2.0
	  self.sma = bt.indicators.SMA(period=30)

      def next(self):
          if self.hi_lo_avg > self.sma:
              print('we have a winner!')

  ...
  ...
  cerebro.addstrategy(MyStrategy)
  cerebro.run()

One for the good guys. Operator overriding does also work in ``next`` and the
users can actually drop the ``[0]`` and directly compare the objects.

If all that were what's actually possible it would actually seem an
overkill. But the good thing is that there is more. See this example::

  import backtrader as bt

  class MyStrategy(bt.Strategy):

      def __init__(self):
          hi_lo_avg = (self.data.high + self.data.low) / 2.0
	  sma = bt.indicators.SMA(period=30)
	  self.signal = hi_lo_avg > sma

      def next(self):
          if self.signal:
              print('we have a winner!')

  ...
  ...
  cerebro.addstrategy(MyStrategy)
  cerebro.run()


We have done 2 things:

  1. Create a *lines* object named ``self.signal`` which compares the
     *high-low-average* against the value of a *Simple Moving Average*

     As explained above this object is useful in ``next``, when it has been
     calculated

  2. Remove the usage of ``[0]`` in ``next`` when checking if ``signal`` is
     ``True``. This is possible because operators have also been overriden for
     boolean operations

Conclusion
**********

Hopefully this adds some light to what actually happens when operations are
executed in ``__init__`` and how operator overriding actually happens.
