
Extending an Indicator
----------------------

.. post:: Jul 21, 2015
   :author: mementum
   :image: 1
   :redirect: posts/2015-07-20
   :excerpt: 2

In Object Oriented Programming, and of course in Python itself, extension of an
existing class can be achieved in two ways.

  - Inheritance (or subclassing)
  - Composition (or embedding)

In :ref:`developing-an-indicator`, the indicator ``Trix`` was developed in just
a couple lines of code. The `ChartSchool - Trix
<http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:trix>`_
reference literature has a ``Trix`` with a signal line showing the similarities
with MACD.

Let's "compose" ``MyTrixSignal`` using the already developed ``Trix``

.. literalinclude:: ./mytrix.py
   :language: python
   :lines: 41-49

Some things had to be repeated in the definition such as the name of the
``trix`` line and the ``period`` to use for calculation. A new line ``signal``
and the corresponding ``sigperiod`` parameter have been defined.

The 2-liner is a good result.

Now let's go for *inheritance*, but first recalling how ``Trix`` looks like:

.. literalinclude:: ./mytrix.py
   :language: python
   :lines: 28-39

Using ``Trix`` as the base class, this is the aspect of ``TrixSignal``

.. literalinclude:: ./mytrix.py
   :language: python
   :lines: 51-59

The inherited indicator ends up also being a 2-liner but:

  - No redefinition of the ``trix`` line is needed
  - No redefinition of the ``period`` parameter is needed

Both are inherited from the base class ``Trix``. And the calculation of the
``trix`` line is done in the base class ``__init__`` method:

  - super(MyTrixSignalInherited, self).__init__()

The choice of **composition** vs **inheritance** is a classic. This example is
not meant to clarify which is better but more to show that:

.. note:: Inheritance works even in the presence of the metadefinitions of
	  **lines** and **params**, which also inherit from the metadefinitions
	  of the base class

And finally the code and charts for both versions when put in action.

1. The first one shows the **inherited** version

.. literalinclude:: ./mytrixsignalinherited.py
   :language: python
   :lines: 21-

.. thumbnail:: ./trixsignal-inherited.png

2. The first one shows the **composed** version

.. literalinclude:: ./mytrixsignalcomposed.py
   :language: python
   :lines: 21-

.. thumbnail:: ./trixsignal-composed.png
