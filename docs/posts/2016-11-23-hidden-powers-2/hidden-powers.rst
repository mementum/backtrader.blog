
.. post:: Nov 23, 2016
   :author: mementum
   :image: 1


Hidden Powers of Python (2)
###########################

Let's tackle a bit more how the *hidden powers of Python* are used in
*backtrader* and how this is implemented to try to hit the main goal: *ease of use*

What are those definitions?
***************************

For example an indicator::

  import backtrader as bt

  class MyIndicator(bt.Indicator):

      lines = ('myline',)
      params = (('period', 20),)

      ...

Anyone capable of reading python would say:

  - ``lines`` is a ``tuple``, actually containing a single item, a string

  - ``params`` is also a ``tuple``, containing another ``tuple`` with 2 items

But later on
************
Extending the example::

  import backtrader as bt

  class MyIndicator(bt.Indicator):

      lines = ('myline',)
      params = (('period', 20),)

      def __init__(self):

          self.lines.myline = (self.data.high - self.data.low) / self.p.period

It should be obvious for anyone, here that:

  - The definition of ``lines`` in the *class* has been turned into an
    attribute which can be reached as ``self.lines`` and contains in turn the
    attribute ``myline`` as specified in the definition

And

  - The definition of ``params`` in the *class* has been turned into an
    attribute which can be reached as ``self.p`` (or ``self.params``) and
    contains in turn the attribute ``period`` as specified in the definition

    And ``self.p.period`` seems to have a value, because it is being directly
    used in an arithmetic operation (obviously the value is the one from the
    definition: ``20``)

The answer: Metaclasses
***********************

``bt.Indicator`` and therefore also ``MyIndicator`` have a *metaclass* and this
allows applying *metaprogramming* concepts.

In this case *the interception of the definitions of ``lines`` and ``params``
to* make them be:

  - Attributes of the *instances*, ie: reachable as ``self.lines`` and
    ``self.params``

  - Attributes of the *classes*

  - Contain the ``atributes`` (and defined values) which are defined in them

Part of the secret
******************

For those not versed in *metaclasses*, it is more or less done so::

  class MyMetaClass(type):

      def __new__(meta, name, bases, dct):
          ...

          lines = dct.pop('lines', ())
	  params = dct.pop('params', ())

	  # Some processing of lines and params ... takes place here

	  ...

	  dct['lines'] = MyLinesClass(info_from_lines)
	  dct['params'] = MyParamsClass(info_from_params)

	  ...

Here the creation of the *class* has been intercepted and the definitions of
``lines`` and ``params`` has been replaced with a *class* based in information
extracted from the definitions.

This alone would not reach, so the creation of the instances is also
intercepted. With Pyton 3.x syntax::

    class MyClass(Parent, metaclass=MyMetaClass):

	def __new__(cls, *args, **kwargs):

            obj = super(MyClass, cls).__new__(cls, *args, **kwargs)
	    obj.lines = cls.lines()
	    obj.params = cls.params()

	    return obj

And here, in the instance *instances* of what above was defined as
``MyLinesClass`` and ``MyParamsClass`` have been put into the instance of
``MyClass``.

No, there is no conflict:

  - The *class* is so to say: "system wide" and contains its own attributes for
    ``lines`` and ``params`` which are classes

  - The *instance* is so to say: "system local" and each instance contains
    instances (different each time) of ``lines`` and ``params``

Usually one will work for example with ``self.lines`` accessing the instance,
but one could also use ``MyClass.lines`` accessing the class.

The latter gives the user access to methods, which are not meant for general
use, but this is Python and nothing can be forbidden and even less with *Open
Source*

Conclusion
**********

Metaclasses are working behind the scenes to provide a machinery which enables
almos a metalanguage by processing things like the ``tuple`` definitions of
``lines`` and ``params``

Being the goal to make the life easier for anyone using the platform
