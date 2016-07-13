
.. post:: Jul 13, 2016
   :author: mementum
   :image: 1

Trading a Day in Steps
######################

It seems that somewhere in the world there is an interest that can be
summarized as follows:

  - *Introduce an order using daily bars but using the opening price*

This comes from the conversations in tickets `#105 Order execution logic with
current day data <https://github.com/mementum/backtrader/issues/105>`_ and
`#101 Dynamic stake calculation
<https://github.com/mementum/backtrader/issues/101>`_

*backtrader* tries to remain as realistic as possible and the following premise
applies when working with *daily bars*:

  - When a daily bar is being evaluated, the bar is already over

It makes sense because all price (*open/high/low/close*) components are
known. It would actually seem illogical to allow an action on the ``open``
price when the ``close`` price is already known.

The obvious approach to this is to use *intraday* data and enter when the
opening prices is known. But it seems *intraday* data is not so widespread.

This is where adding a *filter* to a data feed can help. A filter that:

  - *Converts daily data into intraday-like data*

Blistering barnacles!!! The curious reader will immediately point out that
*upsampling* for example ``Minutes`` to ``Days`` is logical and works, but that
*downsampling* ``Days`` to ``Minutes`` cannot be done.

And it is 100% right. The filter presented below will not try that, but a much
humble and simpler goal:

  - Break a daily bar in 2 parts

    1. A bar with only the opening price and no volume
    2. A 2nd bar which is a copy of the regular daily bar

This can still be held as a logical approach:

  - Upon seeing the *opening* price, the trader can act
  - The order is matched during the rest of the day (actually may or may not be
    matched depending on execution type and price constraints)

The full code is presented below. Let's see a sample run with a well known data
of ``255`` *daily* bars::

  $ ./daysteps.py --data ../../datas/2006-day-001.txt

Output::

  Calls,Len Strat,Len Data,Datetime,Open,High,Low,Close,Volume,OpenInterest
  0001,0001,0001,2006-01-02T23:59:59,3578.73,3578.73,3578.73,3578.73,0.00,0.00
  - I could issue a buy order during the Opening
  0002,0001,0001,2006-01-02T23:59:59,3578.73,3605.95,3578.73,3604.33,0.00,0.00
  0003,0002,0002,2006-01-03T23:59:59,3604.08,3604.08,3604.08,3604.08,0.00,0.00
  - I could issue a buy order during the Opening
  0004,0002,0002,2006-01-03T23:59:59,3604.08,3638.42,3601.84,3614.34,0.00,0.00
  0005,0003,0003,2006-01-04T23:59:59,3615.23,3615.23,3615.23,3615.23,0.00,0.00
  - I could issue a buy order during the Opening
  0006,0003,0003,2006-01-04T23:59:59,3615.23,3652.46,3615.23,3652.46,0.00,0.00
  ...
  ...
  0505,0253,0253,2006-12-27T23:59:59,4079.70,4079.70,4079.70,4079.70,0.00,0.00
  - I could issue a buy order during the Opening
  0506,0253,0253,2006-12-27T23:59:59,4079.70,4134.86,4079.70,4134.86,0.00,0.00
  0507,0254,0254,2006-12-28T23:59:59,4137.44,4137.44,4137.44,4137.44,0.00,0.00
  - I could issue a buy order during the Opening
  0508,0254,0254,2006-12-28T23:59:59,4137.44,4142.06,4125.14,4130.66,0.00,0.00
  0509,0255,0255,2006-12-29T23:59:59,4130.12,4130.12,4130.12,4130.12,0.00,0.00
  - I could issue a buy order during the Opening
  0510,0255,0255,2006-12-29T23:59:59,4130.12,4142.01,4119.94,4119.94,0.00,0.00

The following happens:

  - ``next`` is called: ``510 times`` which is ``255 x 2``

  - The ``len`` of the *Strategy* and that of the *data* reaches a total of
    ``255``, which is the expected: **the data has only those many bars**

  - Every time the ``len`` of the *data* increases, the 4 price components have
    the same value, namely the ``open`` price

    Here a remark is printed out to indicate that during this *opening* phase
    action could be taken, like for example buying.

Effectively:

  - The daily data feed is being *replayed* with 2 steps for each day, giving
    the option to act in between ``open`` and the rest of the price components

The filter will be added to the default distribution of *backtrader* in the
next release.

The sample code including the filter.

.. literalinclude:: ./daysteps.py
   :language: python
   :lines: 21-
