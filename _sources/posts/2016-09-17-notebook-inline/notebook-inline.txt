.. post:: Sep 17, 2016
   :author: mementum
   :image: 1


Notebook - Automatic Inline Plotting
####################################

Release ``1.9.1.99`` adds automatic inline plotting when running inside a
*Jupyter Notebook*.

Some of the questions around ``backtrader`` show people using the platform
inside a *Notebook* and supporting this and making it the default behavior
should make things consistent.

If the previous behavior is wished and figures must be plotted independently,
simply do::

  import backtrader as bt

  ...

  cerebro.run()

  ...

  cerebro.plot(iplot=False)

Of course and if running from a script or interactively, the default plotting
backend for ``matplotlib`` will be used as before, which will plot the charts
in separate windows.
