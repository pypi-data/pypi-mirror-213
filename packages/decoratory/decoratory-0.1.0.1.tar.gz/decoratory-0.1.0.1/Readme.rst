
.. _top:

==============================================================================
Decoratory
==============================================================================


**Introduction**

The "decoratory" package is based on the `Decorator Arguments Pattern`_, an 
integrated concept for Python decorators with and without parameters. Thus 
all decorators created with it support complex arguments, e.g. lists of 
values and functions, without unnecessarily complicating the decoration of 
simple cases by these extensions. All implementation details are described 
on the `project homepage`_.


**Installation** ::

    pip install decoratory

After installation, basic information about the package, the individual 
modules and their methods is also available from the command line. ::

    python -m decoratory --help


**Content**

The "decoratory" package available here includes some classic decorators
implemented and functionally extended with this concept, e.g.

* `Singleton`_
* `Multiton`_
* `Wrapper`_
* `Observer`_   (coming soon...)

This is an open list that will grow over time.


**Description**

To illustrate the functionality of each module, a simple as well as a 
possibly more complex example is presented. Even if only one particular module 
is needed, it is recommended to view the preceding examples as well. For even
more examples of the full range of possibilities, again, please refer to the 
`project homepage`_.


******************************************************************************
Singleton
******************************************************************************

A `singleton pattern`_ is a design pattern that limits the instantiation of 
a class to a single (unique) instance. This is useful when exactly one unique 
object is needed i.e. to manage an expensive resource or coordinate actions 
across modules.

As a simple example serves the decoration of the class  ``Animal`` as singleton. 
In the context of the `Decorator Arguments Pattern`_, this can be done both 
without brackets (class) and with brackets (object, instance), because both 
notations describe the same functionality.

.. code-block:: python
   
    # *** example_singleton.py - class Animal with Singleton decoration

    from decoratory.singleton import Singleton

    @Singleton                      # or @Singleton()
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

If instances of the class ``Animal`` are now created, this is only done for the 
very first instantiation, and for all further instantiations always this 
"primary instance" is given back.
            
.. code-block:: python
   
    # *** example_singleton.py - creation of instances

    # Create Instances
    a = Animal(name='Bello')        # Creates Bello
    b = Animal(name='Tessa')        # Returns Bello

This can be verified by the following comparisons.

.. code-block:: python

    # *** example_singleton.py - verfication of the unique instance

    # Case 1: Static decoration using @Singleton or @Singleton()
    print(f"a = {a}")               # a = Animal('Bello')
    print(f"b = {b}")               # b = Animal('Bello')
    print(f"a is b: {a is b}")      # a is b: True
    print(f"a == b: {a == b}")      # a == b: True

If instead of the above "static decoration" using pie-notation, i.e. with 
@-notation at the class declaration, the "dynamic decoration" in Python code 
is used, additional parameters can be passed to the decorator for passing 
to the class constructor.

.. code-block:: python

    # *** example_singleton.py - dynamic decoration with extra parameters

    # Case 2: Dynamic decoration providing extra initial default values 
    Animal = Singleton(Animal, 'Bello')
    Animal()                        # Using the decorator's default 'Bello'
    Animal(name='Tessa')            # Returns Bello
    print(Animal.instance)          # Animal('Bello')

Quite generally, for all the following decorators based on this 
`Decorator Arguments Pattern`_, these two properties are always fulfilled:

.. note::
    * Decoration as a class (without parentheses) and Decoration as an instance 
      (with empty parentheses) are equivalent
    * For dynamic decoration, extra parameters can be passed, e.g. for the class 
      constructor


******************************************************************************
Multiton
******************************************************************************

A `multiton pattern`_ is a design pattern that extends the singleton pattern.
Whereas the singleton allows for exactly one instance per class, the multiton 
ensures one single (unique) *instance per key value of a dictionary*.

In this implementation the key parameter can be either any immutable type
or a callable returning such an immutable type which can be used as a key
of a dictionary. In case of an invalid key, key is set ``None`` and with only 
one key value the multiton simply collapses to a singleton, therefore the 
decoration ``@Multiton`` resp. ``@Multiton()`` or even ``@Multiton(key=17)`` 
or  ``@Multiton(key='some fixed value')`` and so on always creates a singleton.

Sometimes the key is independent of the classified object, but in many cases 
it is part of the classified object itself, as in the following example where
the key string matches the parameter ``name`` of the constructor of the 
class ``Animal``.

.. code-block:: python
   
    # *** example_multitonton.py - class Animal with Multiton decoration

    from decoratory.multiton import Multiton

    @Multiton(key='name')           # uses kwargs['name'] as key
    class Animal:
        def __init__(self, spec, name):
            self.spec = spec
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.spec}', '{self.name}')"

When instances of the class ``Animal`` are now created, this only happens for 
the *first instantiation per key value*, the initial name of the animal. For 
all subsequent instantiations, this "primary instance per key value" is 
returned. But for each new key value, a new ``Animal`` instance is created 
and stored in the internal directory.

.. code-block:: python
   
    # *** example_multitonton.py - creation of instances

    # Create Instances
    a = Animal('dog', name='Bello')
    b = Animal('cat', name='Mausi')
    c = Animal('dog', name='Tessa')

This can be verified by the following comparisons.

.. code-block:: python

    # *** example_multitonton.py - One unique instance per name

    # Case 1: key='name' references kwargs['name'] from __init__(..,name)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Tessa')

With three different names, a separate instance is created in each case. 
In contrast, the following variant distinguishes only two types (equivalence 
classes): animals with a character 'a' in their name and those without and 
thus the key values can only be ``True`` or ``False``.

.. code-block:: python

    # *** example_multitonton.py - One unique instance per equivalence class

    # Case 2: with decoration @Multiton(key=lambda spec, name: 'a' in name)
    print(a)                        # Animal('dog', 'Bello'), key=False
    print(b)                        # Animal('cat', 'Mausi'), key=True
    print(c)                        # Animal('cat', 'Mausi'), key=True

To actively control access to new equivalence classes, ``Multiton`` provides 
the ``seal()``, ``unseal()``, and ``issealed()`` methods for sealing, unsealing,
and checking the sealing state of the ``Multiton``. By default, the sealed 
state is set ``False``, so for every new key a new (unique) object is 
instantiated. When sealed (e.g. later in the process) is set ``True`` the 
dictionary has completed, i.e. restricted to the current object set and 
any new key raises a ``KeyError``.

For deeper, special requirements on the equivalence classes of a multiton 
then by means of the method ``instances()`` the internal directory can also 
be actively manipulated, which of course should be done with caution and 
generally is not recommended. 

For this reason, each object knows its multiton: Setting ``Multiton``'s ``attrib`` 
parameter while decoration to a valid attribute name string the multiton is 
attributed in the new instantiated substitute object, is the chosen name 
invalid or missing, the default attribute name ``multiton`` is chosen. 

Thus, in the above example, ``a.multiton`` would be the multiton of ``a`` 
('Bello') and ``a.multiton.instances()`` would be the directory of equivalence 
classes to which it belongs.

.. warning::
 
    Classifications into the multiton directory are done only once on
    initial key data. Subsequent changes affecting a key value are not 
    reflected in the multiton directory, i.e. the directory may then be 
    corrupted by such modifications.
    
    Therefore, **never change key related values of classified objects**!


******************************************************************************
Wrapper
******************************************************************************

As the name implies, a wrapper encloses the original function with an

* (optional) ``before`` call functionality
                
and/or

* (optional) ``after`` call functionality.

This implementation additionally supports an 

* (optional) ``replace`` call functionality.

The wrapper is all the more useful and broadly applicable the more flexible 
these three activities can be formulated. All three decorator parameters, 
``before``, ``after`` and ``replace``, can be combined with each other and 
support both single callables and (nested) lists of F-types 
(imported from module decoratory.basic, see below for details). 
In addition, ``replace`` supports passing results from successive 
replacement calls through an optional keyword argument named ``result`` 
(defaut value is None).

Even without any of these arguments, the wrapper can be used to "overwrite" 
default values, for example.

.. code-block:: python

    # *** example_wrapper.py - overwrite default parameter values

    from decoratory.wrapper import Wrapper

    # Case 1: Dynamic decoration with decorator arguments, only
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    # Function call with default parameters
    some_function()                 # value = 'original'
    some_function = Wrapper(some_function, value="changed")
    some_function()                 # value = 'changed'

The functionality of ``some_function()`` itself remains unchanged. A typical 
scenario for a wrapper is, of course, the execution of additional functionality 
before and/or after a given functionality, which itself remains unchanged, 
such as ``enter/leave`` markers, call data caches, runtime measurements, etc.

.. code-block:: python

    # *** example_wrapper.py - enclose original function

    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    # Case 2: Decoration with before and after functionalities
    def print_message(message: str = "ENTER"):
        print(message)

    @Wrapper(before=print_message, after=F(print_message, "LEAVE"))
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    some_function()                 # ENTER
                                    # value = 'original'
                                    # LEAVE

While ``before`` calls ``print_message`` with its default parameters the 
``after`` parameter uses the ``F``-function from ``decoratory.basic``. 
It has a signature ``F(callable, *args, **kwargs)`` and encapsulates the 
passing of any function with optional positional and keyword parameters. 

Finally, a more complex example illustrates the replacement of the original 
functionality with a sequence of replacement functionalities, passing a 
``result`` object of type ``int`` between successive calls.

.. code-block:: python

    # *** example_wrapper.py - enclose and replacing original function

    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    # Case 3: Decoration with before, after and multiple replacements
    def print_message(message: str = "BEFORE"):
        print(message)

    def replacement_printer(add: int = 1, *, result=None):
        result += add if isinstance(result, int) else 0
        print(f"result = {result}")
        return result

    @Wrapper(before=F(print_message, "ENTER"),
             replace=[F(replacement_printer, 1, result=0),
                      F(replacement_printer, 3),
                      F(replacement_printer, 5)],
             after=F(print_message, "LEAVE"))
    def default_printer(message: str = "DEFAULT"):
        print(message)

    default_printer()               # ENTER         (before)
                                    # result = 1    (replacement_printer, 1)
                                    # result = 4    (replacement_printer, 3)
                                    # result = 9    (replacement_printer, 5)
                                    # LEAVE         (after)
                                    # 9             (output default_printer)

The absence of the outputs of ``BEFORE`` and ``DEFAULT`` reflects the correct 
replacements by the decoration, and the order of execution is exactly as 
expected: ``before`` then ``replace`` then ``after`` and in each of these 
variables the lists are processed in ascending order.


******************************************************************************
Observer
******************************************************************************

coming soon...


.. ===========================================================================
.. _project homepage: http://evation.eu
.. _singleton pattern: https://en.wikipedia.org/wiki/Singleton_pattern
.. _multiton pattern: https://en.wikipedia.org/wiki/Multiton_pattern
.. _Decorator Arguments Pattern: http://evation.eu

`back to top <#top>`_

