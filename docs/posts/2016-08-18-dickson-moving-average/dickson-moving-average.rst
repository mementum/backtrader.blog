
.. post:: Aug 17, 2016
   :author: mementum
   :image: 1


Dickson Moving Average
######################

In one of the regular visits to `reddit Algotrading
<https://www.reddit.com/r/algotrading/>`_
I found a post about a moving average which tries to mimic the Jurik Moving
Average (aka *JMA*)

  - `JMA on Jurik Research <http://www.jurikres.com/catalog1/ms_ama.htm>`_

The *reddit* post names this average the *Dickson Moving Average* after its own
author *Nathan Dickson* (*reddit* handle)

  - `Dickson Moving Average
    <https://www.reddit.com/r/algotrading/comments/4xj3vh/dickson_moving_average/>`_

Described as an algorithm in *EasyLanguage* I had to ask about the seed values
and the nature of ``ec`` and this finally led to *Ehlers* and the *Zero Lag
Indicator*

  - `ZERO LAG <http://www.mesasoftware.com/papers/ZeroLag.pdf>`_

In order to implement the *Dickson Moving Average* into *backtrader* and given
the dependencies on *Ehlers* and also on the *Hull Moving Average*, those two
were also added to the arsenal of moving averages.

In summary the following has been added with ``Release 1.8.7.96``:

  - ``Hull Moving Average``
  - ``Zero Lag Indicator``
  - ``Dickson Moving Average``

And the results can be seen with a plot using one of the sample datas and ``btrun``::

  $ btrun --nostdstats \
      --format btcsv \
      --data ../../../backtrader/datas/2006-day-001.txt \
      --indicator :SMA \
      --indicator :EMA \
      --indicator :HMA \
      --indicator :ZeroLagIndicator \
      --indicator :DMA \
      --plot style=\'line\'

.. thumbnail:: dma-comparison.png

Now it's about getting the *Dickson Moving Average* to produce profit ... like
with any other indicator.

.. note:: Notice how the *Hull Moving Average* (aka *HMA*) starts producing
	  values a couple of values later than the rest. This is due to the
	  fact that is uses a *moving average* on *moving average* which delays
	  the initial production.

And a comparison showing how the *DMA* sits in between the middle of a
*ZeroLagIndicator* and a *HullMovingAverage*. The latter with a ``period=7`` to
match the default value inside the *Dickson Moving Average*::


  $ btrun --nostdstats \
      --format btcsv \
      --data ../../../backtrader/datas/2006-day-001.txt \
      --indicator :HMA:period=7 \
      --indicator :ZeroLagIndicator \
      --indicator :DMA \
      --plot style=\'line\'

.. thumbnail:: dma-hma-zlind-comparison.png
