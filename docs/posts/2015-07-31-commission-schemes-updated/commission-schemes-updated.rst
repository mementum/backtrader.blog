
Improving Commissions: Stocks vs Futures
----------------------------------------

.. post:: Jul 31, 2015
   :author: mementum
   :image: 1
   :redirect: posts/2015-07-31

Posting ``backtrader`` usage examples has given me an insight into things that
were missing. For starters:

  - :ref:`multicore-optimization`

  - :ref:`commission-schemes`

The latter showed me:

  - The broker was doing the right things with regards to the calculation of
    profit and loss and providing the right order notifications to the calling
    strategy

  - The strategy had no access to ``operations`` (aka ``trades``) which is the
    result of an order having opened and closed a position (with the latter
    showing a P&L figure)

  - The plotted ``Operation`` P&L figures were gathered by an ``Observer`` and
    had no access to the actual ``commission scheme``, hence rendering the same
    P&L for a ``futures-like`` operation and for a ``stocks-like`` one

Clearly a small internal rework was needed to achieve:

  - ``Operation`` notification to the strategy

  - ``Operations`` displaying the right P&L figures

The ``broker`` already had all of the needed information and already stuffing
most of it into the ``order`` which was being notified to the ``strategy`` which
had create it. The only decision to make was whether the ``broker`` would fit an
extra information bit into the order or it could calculate the ``operations``
itself.

Since the strategy already gets the ``orders`` and keeping the ``operations`` in
a list seems natural, the ``broker`` just adds the actual P&L when an order has
closed partially/totally a position, leaving the responsibility of the
calculation to the ``strategy``.

In turn this simplifies the actual role of the ``Operations Observer`` to that
of observing newly closed ``Operation`` and recording it. The role it should
always have had.


The code below has been reworked to no longer calculate the P&L figures, but to
just pay attention to those notified in ``notify_operation``.

And the charts now reflect realistic P&L figures (The ``cash`` and ``value``
were alredy realistic)

The old logging for futures::

  2006-03-09, BUY CREATE, 3757.59
  2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 2000.00, Comm 2.00
  2006-04-11, SELL CREATE, 3788.81
  2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 2000.00, Comm 2.00
  2006-04-12, OPERATION PROFIT, GROSS 328.00, NET 324.00
  2006-04-20, BUY CREATE, 3860.00
  2006-04-21, BUY EXECUTED, Price: 3863.57, Cost: 2000.00, Comm 2.00
  2006-04-28, SELL CREATE, 3839.90
  2006-05-02, SELL EXECUTED, Price: 3839.24, Cost: 2000.00, Comm 2.00
  2006-05-02, OPERATION PROFIT, GROSS -243.30, NET -247.30

The new logging for futures::

  2006-03-09, BUY CREATE, 3757.59
  2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 2000.00, Comm 2.00
  2006-04-11, SELL CREATE, 3788.81
  2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 2000.00, Comm 2.00
  2006-04-12, OPERATION PROFIT, GROSS 328.00, NET 324.00
  2006-04-20, BUY CREATE, 3860.00
  2006-04-21, BUY EXECUTED, Price: 3863.57, Cost: 2000.00, Comm 2.00
  2006-04-28, SELL CREATE, 3839.90
  2006-05-02, SELL EXECUTED, Price: 3839.24, Cost: 2000.00, Comm 2.00
  2006-05-02, OPERATION PROFIT, GROSS -243.30, NET -247.30
  2006-05-02, BUY CREATE, 3862.24

The old logging For stocks::

  2006-03-09, BUY CREATE, 3757.59
  2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 3754.13, Comm 18.77
  2006-04-11, SELL CREATE, 3788.81
  2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 3786.93, Comm 18.93
  2006-04-12, OPERATION PROFIT, GROSS 32.80, NET -4.91
  2006-04-20, BUY CREATE, 3860.00
  2006-04-21, BUY EXECUTED, Price: 3863.57, Cost: 3863.57, Comm 19.32
  2006-04-28, SELL CREATE, 3839.90
  2006-05-02, SELL EXECUTED, Price: 3839.24, Cost: 3839.24, Comm 19.20
  2006-05-02, OPERATION PROFIT, GROSS -24.33, NET -62.84

The new logging for stocks::

  2006-03-09, BUY CREATE, 3757.59
  2006-03-10, BUY EXECUTED, Price: 3754.13, Cost: 3754.13, Comm 18.77
  2006-04-11, SELL CREATE, 3788.81
  2006-04-12, SELL EXECUTED, Price: 3786.93, Cost: 3786.93, Comm 18.93
  2006-04-12, OPERATION PROFIT, GROSS 32.80, NET -4.91
  2006-04-20, BUY CREATE, 3860.00
  2006-04-21, BUY EXECUTED, Price: 3863.57, Cost: 3863.57, Comm 19.32
  2006-04-28, SELL CREATE, 3839.90
  2006-05-02, SELL EXECUTED, Price: 3839.24, Cost: 3839.24, Comm 19.20
  2006-05-02, OPERATION PROFIT, GROSS -24.33, NET -62.84
  2006-05-02, BUY CREATE, 3862.24

And the charts (only the new ones). The difference between ``futures-like``
operations and ``stock-like`` operations can now be clearly seen and not only in
the evolution of ``cash`` and ``value``.

Commissions for futures
=======================

.. thumbnail:: ./commission-futures-updated.png

Commissions for stocks
=======================

.. thumbnail:: ./commission-stocks-updated.png


The code
========

.. literalinclude:: ./strategy-with-commission-updated.py
   :language: python
   :lines: 21-
