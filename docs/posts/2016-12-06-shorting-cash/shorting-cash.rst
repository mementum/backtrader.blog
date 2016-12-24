
.. post:: Dec 6, 2016
   :author: mementum
   :image: 1


Shorting the cash
#################

From the very first moment *backtrader* was enabled for shorting anything,
including *stock-like* and *future-like* instruments.  When a short was done,
the cash was decreased and the value of the shorted asset used for the total
net liquidation value.

Removing from one side and adding to the other keeps things in balance.

It seems that people prefer to have *cash* increased, which probably lends to
more spending.

With release ``1.9.7.105``, the broker has changed the default behavior to
adding cash and removing value. This can be controlled with the parameter
``shortcash`` which defaults to ``True``. Changing it would be done like this::

  cerebro.broker.set_shortcash(False)

or::

  cerebro.broker = bt.brokers.BackBroker(shortcash=False, **other_kwargs)

In action
*********

The sample below uses a standard moving average crossover and can be used to
see the differences. Running it without arguments and the new behavior::

  $ ./shortcash.py --plot

.. thumbnail:: shortcash-on.png

It can be compared with the behavior disabled with::

  $ ./shortcash.py --plot --broker shortcash=False

.. thumbnail:: shortcash-off.png

Things that remain the same:

  - Final result
  - Trades
  - Net Liquidation Value evolution

    To see this an extra *Observer* is added to make sure the scaling allows
    seeing the evolution in detail

What changes:

  - When ``shortcash`` is set to ``False`` cash never goes above the initial
    level, because an operation alwasy costs money

    But with the new default behavior we can already see that the 1st short
    operation (which happens to be the 1st) adds cash to the system and then
    how the *longs* deduct cash from the system (the short is 1st closed, obviously)

Sample Usage
************
::

  $ ./shortcash.py --help
  usage: shortcash.py [-h] [--data DATA] [--cerebro CEREBRO] [--broker BROKER]
                      [--sizer SIZER] [--strat STRAT] [--plot [kwargs]]

  shortcash testing ...

  optional arguments:
    -h, --help            show this help message and exit
    --data DATA           Data to read in (default:
                          ../../datas/2005-2006-day-001.txt)
    --cerebro CEREBRO     kwargs in key=value format (default: )
    --broker BROKER       kwargs in key=value format (default: )
    --sizer SIZER         kwargs in key=value format (default: )
    --strat STRAT         kwargs in key=value format (default: )
    --plot [kwargs], -p [kwargs]
                          Plot the read data applying any kwargs passed For
                          example: --plot style="candle" (to plot candles)
                          (default: None)


Sample Code
***********

.. literalinclude:: shortcash.py
   :language: python
   :lines: 21-
