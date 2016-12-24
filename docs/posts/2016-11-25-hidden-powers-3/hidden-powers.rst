
.. post:: Nov 25, 2016
   :author: mementum
   :image: 1


Hidden Powers of Python (3)
###########################

Last, but not least, in this series about how the hidden powers of Python are used in
*backtrader* is how some of the magic variables show up.

Where do ``self.datas`` and others come from?
*********************************************

The usual suspect classes (or subclasses thereof) ``Strategy``, ``Indicator``,
``Analyzer``, ``Observer`` have auto-magically defined attributes, like for
example the array which contains the *data feeds*.

Data Feeds are added to a ``cerebro`` instance like this::

  from datetime import datetime
  import backtrader as bt

  cerebro = bt.Cerebro()
  data = bt.YahooFinanceData(dataname=my_ticker, fromdate=datetime(2016, 1, 1))
  cerebro.adddata(data)

  ...

Our winning strategy for the example will go long when the ``close`` goes above
a *Simple Moving Average*. We'll use *Signals* to make the example shorter::

  class MyStrategy(bt.SignalStrategy):
      params = (('period', 30),)

      def __init__(self):
          mysig = self.data.close > bt.indicators.SMA(period=self.p.period)
	  self.signal_add(bt.signal.SIGNAL_LONG, mysig)

Which gets added to the mix as::

  cerebro.addstrategy(MyStrategy)

Any reader will notice that:

  - ``__init__`` takes no parameters, named or not

  - There is no ``super`` call so the base class is not being directly asked to
    do its init

  - The definition of ``mysig`` references ``self.data`` which probably has to
    do with the ``YahooFinanceData`` instance which is added to ``cerebro``

    **Indeed it does!**

There actually other attributes which are there and not seen in the
example. For example:

  - ``self.datas``: an array containing all *data feeds* which are added to
    ``cerebro``

  - ``self.dataX``: where ``X`` is a number which reflects the order in which
    the data was added to cerebro (``data0`` would be the data added above)

  - ``self.data``: which points to ``self.data0``. Just a ahortcut for
    convenience since most examples and strategies only target a single data

More can be found in the docs:

  - https://www.backtrader.com/docu/concepts.html
  - https://www.backtrader.com/docu/datafeed.html


How are those attributes created?
*********************************

In the 2nd article in this series it was seen that the class creation
mechanims and instance creation mechanism were intercepted. The latter is used
to do that.

  - ``cerebro`` receives the *class* via ``adstrategy``

  - It will instantiate it when needed and add itself as an attribute

  - The ``new`` classmethod of the strategy is intercepted during the creation
    of the ``Strategy`` instance and examines which *data feeds* are available
    in ``cerebro``

    And it does creates the *array* and *aliases* mentioned above

This mechanism is applied to many other objects in the *backtrader* ecosystem,
in order to simplifly what the end users have to do. As such:

  - There is for example no need to constantly create function prototypes which
    contain an argument named ``datas`` and no need to assign it to
    ``self.datas``

    Because it is done auto-magically in the background

Another example of this interception
************************************

Let's define a winning indicator and add it to a winning strategy. We'll repack
the *close over SMA* idea::

  class MyIndicator(bt.Indicator):
      params = (('period', 30),)
      lines = ('signal',)

      def __init__(self):
          self.lines.signal = self.data - bt.indicators.SMA

And now add it to a regular strategy::

  class MyStrategy(bt.Strategy):
      params = (('period', 30),)

      def __init__(self):
          self.mysig = MyIndicator(period=self.p.period)

      def next(self):
          if self.mysig:
	      pass  # do something like buy ...


From the code above there is obviously a calculation taking place in
``MyIndicator``::

  self.lines.signal = self.data - bt.indicators.SMA

But it seems to be done nowhere. As seen in the 1st article in this series, the
operation generates an *object*, which is assigned to ``self.lines.signal`` and
the following happens:

  - This object intercepts also its creation process

  - It scans the *stack* to understand the context in which is being created,
    in this case inside an instance of ``MyIndicators``

  - And after its *initialization* is completed, it adds itself to the internal
    structures of ``MyIndicator``

  - Later when ``MyIndicator`` is calculated, it will in turn calculate the
    operation which is inside the object referenced by ``self.lines.signal``

Good, but who calculates ``MyIndicator``
****************************************

Exactly the same process is followed:

  - ``MyIndicator`` scans the stack during creation and finds the
    ``MyStrategy``

  - And adds itself to the structures of ``MyStrategy``

  - Right before ``next`` is called, ``MyIndicator`` is asked to recalculate
    itself, which in turns tells ``self.lines.signal`` to recalculate itself

The process can have multiple layers of indirection.

And the best things for the user:

  - No need to add calls like ``register_operation`` when something is created

  - No need to manually trigger calculations


Concluding
**********

The last article in the series shows another example of how class/instance
creation interception is used to make the life of the end user easier by:

  - Adding objects from the ecosystem there where they are needed and creating
    aliases

  - Auto-registering classes and triggering calculations
