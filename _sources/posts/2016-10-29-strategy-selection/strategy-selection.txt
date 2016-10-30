
.. post:: Oct 29, 2016
   :author: mementum
   :image: 1


Strategy Selection
##################

An interesting use case has come up via `Ticket 177
<https://github.com/mementum/backtrader/issues/177>`_. In this case *cerebro*
is being used multiple times to evaluate differet strategies which are being
fetched from an external data source.

And the problem arises because:

  - *cerebro* is not meant to be run several times. This is not the 1st time
    and rather than thinking that users are doing it wrong, it seems it is a
    use case.

*backtrader* can still support this use case, but not in the direct way it has
been attempted.

Optimizing the selection
########################

The buil-in optimization in *backtrader* already does the required thing:

  - Instantiate several strategy instances and collect the results

Being the only thing that the *instances* all belong to the same *class*. This
is where Python helps by lettings us control the creation of an object.

First, let's add to very quick strategies to a script using the *Signal*
technology built in *backtrader*

.. literalinclude:: strategy-selection.py
   :language: python
   :lines: 29-41

It cannot get easier.

And now let's do the magic of delivering those two strategies.

.. literalinclude:: strategy-selection.py
   :language: python
   :lines: 43-51

Et voilá! When the class ``StFetcher`` is being instantiated, method
``__new__`` takes control of instance creation. In this case:

  - Gets the ``idx`` param which is passed to it
  - Uses this param to get a strategy from the ``_STRATS`` list in which our
    previous sample strategies have been stored

    .. note:: Nothing would prevent using this ``idx`` value to fetch
	      strategies from a server and/or a database.

  - Instantiate and return the *fecthed* strategy

Running the show
****************

.. literalinclude:: strategy-selection.py
   :language: python
   :lines: 60-63

Indeed! Optimiization it is! Rather than ``addstrategy`` we use ``optstrategy``
and pass an array of values for ``idx``. Those values will be iterated over by
the optimization engine.

Because ``cerebro`` can host several strategies in each optimization pass, the
result will contain a *list of lists*. Each sublist is the result of each
optimization pass.

In our case and with only 1 strategy per pass, we can quickly flatten the
results and extract the values of the analyzer we have added.

.. literalinclude:: strategy-selection.py
   :language: python
   :lines: 64-69

A sample run
************
::

  ./strategy-selection.py

  Strat 0 Name St0:
    - analyzer: OrderedDict([(u'rtot', 0.04847392369449283), (u'ravg', 9.467563221580632e-05), (u'rnorm', 0.02414514457151587), (u'rnorm100', 2.414514457151587)])

  Strat 1 Name St1:
    - analyzer: OrderedDict([(u'rtot', 0.05124714332260593), (u'ravg', 0.00010009207680196471), (u'rnorm', 0.025543999840699633), (u'rnorm100', 2.5543999840699634)])

Our 2 strategies have been run and deliver (as expected) different results.

.. note:: The sample is minimal but has been run with all available
	  CPUs. Executing it with ``--maxpcpus=1`` will be faster. For more
	  complex scenarios using all CPUs will be useful.

Conclusion
**********

The *Strategy Selection* use case is possible and doesn't need circumventing
any of the built-in facilities in either *backtrader* or *Python* itself.


Sample Usage
============
::

  $ ./strategy-selection.py --help
  usage: strategy-selection.py [-h] [--data DATA] [--maxcpus MAXCPUS]
                               [--optreturn]

  Sample for strategy selection

  optional arguments:
    -h, --help         show this help message and exit
    --data DATA        Data to be read in (default:
                       ../../datas/2005-2006-day-001.txt)
    --maxcpus MAXCPUS  Limit the numer of CPUs to use (default: None)
    --optreturn        Return reduced/mocked strategy object (default: False)


The code
========

Which has been included in the sources of backtrader

.. literalinclude:: strategy-selection.py
   :language: python
   :lines: 21-
