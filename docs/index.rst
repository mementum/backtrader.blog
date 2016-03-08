
backtrader - Python backtesting
===============================

``backtrader`` offers a complete backtesting platform with this (not fully
comprehensive) list of features:

  - Index 0 approach to access the currently produced (or to be produced) data
  - Index -1 approach to access the last produced data (to remain Pythonic)
  - Multiple Strategies at the same time
  - Multiple Datas at the same Time
  - Datas with different timeframes can be mixed (days and weeks)
  - Data Resampling
  - Data Replaying (i.e: indicators/strategies see 5 bars in a weekly timeframe)
  - Indicators (several) which can of course take datas and/or indicators as input
  - Natural python language/operations for Indicator development and object
    comparison/operations (arithmetic, logical operators)
    As much as permitted by Pthon overriding capabilities (if, and, or cannot
    be overriden ... but they are provided as logical functions)
  - Broker implementation with AtMarket, AtClose, AtLimit, Stop, StopLimit
    orders
  - Commission schemes supporting futures-like and stocks-like objects and
    customizable
  - Event based (strategy/indicator 'next' will be called with all subordinate
    indicators calculated and data fetched)
  - Vector (in the form on inner for loops) based for a one shot calculation
    This applies to indicators ... Strategies always are executed one step at a
    time
  - Strategy optimization (including multicore support)
  - Plotting support for visual inspection

The Blog Entries
----------------

.. postlist:: 5
   :format: {title} by {author} on {date}
   :excerpts:
   :list-style: circle

.. toctree::
   :hidden:

   about.rst
