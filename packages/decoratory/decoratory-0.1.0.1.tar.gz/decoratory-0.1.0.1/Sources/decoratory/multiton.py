#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Multiton**

    A multiton is a design pattern that extends the singleton pattern.
    Whereas the singleton allows for exactly one instance per class, the
    multiton pattern ensures one single (unique) instance per key value
    (of a dictionary).

    In this implementation the key parameter can be either any immutable type
    or a callable returning such an immutable type which can be used as a key
    of a dictionary. In case of an invalid key, key is set None and the
    multiton simply collapses to a singleton.

    Setting the attrib parameter to a valid attribute name string the multiton
    is attributed in the new instantiated substitute object, is the name
    invalid, the attribute name 'multiton' is chosen.

    By default, the sealed parameter is set False, so for every new key a new
    (unique) object is instantiated. When sealed (e.g. later in the process)
    is set True the dictionary has completed, i.e. restricted to the current
    object set and any new key raises a KeyError.

    Warning: Classifications into the multiton directory are done only once on
             initial data, the object's __init__ parameters! Subsequent changes
             affecting the key are not reflected in the multiton directory,
             i.e. the directory may then be corrupted by such modifications.
             Therefore, never change key related values of classified objects!

    Attributes
    ----------
    substitute: object
        A type to be made a multiton.

    key: int or str or callable
        Unique (immutable) key for the instance dictionary.

    attrib: str
        Name of the attribute containing the multiton instance.

    Methods
    -------
    seal(self):
        Seal multiton of unique key instances.

    unseal(self):
        Unseal multiton of unique key instances.

    issealed(self):
        Is the multiton of unique key instances sealed?

    instances(self):
        Dictionary of all instance representations.

    Example
    -------

    from decoratory.multiton import Multiton

    # --- For alternative decorations see cases below!
    @Multiton
    class Animal:
        def __init__(self, spec, name):
            self.spec = spec
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.spec}', '{self.name}')"

    # Create instances
    a = Animal('dog', name='Bello')
    b = Animal('cat', name='Mausi')
    c = Animal('dog', name='Tessa')

    # Case 1: decoration @Multiton or @Multiton() or @Multiton(key=17) or ...
    #    ---> With no or fixed key the Multiton acts like a Singleton
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('dog', 'Bello')
    print(c)                                # Animal('dog', 'Bello')

    # Case 2: decoration Multiton(key=lambda spec, name: 'a' in name)
    #    ---> key is a function evaluating the attribute name from __init__(..)
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('cat', 'Mausi')
    print(c)                                # Animal('cat', 'Mausi')

    # Case 3: decoration Multiton(key=0)    # take args[0]
    #    ---> integer key=val references args[val] from __init__(.., spec,..)
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('cat', 'Mausi')
    print(c)                                # Animal('dog', 'Bello')

    # Case 4: decoration Multiton(key='0')  # take kwargs['0'] does not exist!
    #    ---> string key=str references kwargs[str], here leading to None
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('dog', 'Bello')
    print(c)                                # Animal('dog', 'Bello')

    # Case 5: decoration Multiton(key='name') # take kwargs['name'] does exist!
    #    ---> string key=str references kwargs[str] from __init__(..,.., name)
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('cat', 'Mausi')
    print(c)                                # Animal('dog', 'Tessa')

    # Case 6: decoration Multiton(key='name'): Seal after Bello
    #    ---> string key=str references kwargs[str] (e.g. self.name)
    Animal.instances().clear()              # Reset...
    print(Animal.instances())               # ... to an empty dictionary
    print(Animal.issealed())                # False
    a = Animal('dog', name='Bello')         # Animal('dog', 'Bello')
    Animal.seal()                           # seal it!
    print(Animal.issealed())                # True
    b = Animal('dog', name='Bello')         # Returns a-objekt from multiton
    print(a is b)                           # True
    try:
        c = Animal('dog', name='Tessa')     # KeyError, Animal is sealed!
    except KeyError as ex:
        print(f"For '{ex.args[1]}' {ex.args[0]}")
    print(Animal.instances())               # {'Bello': Animal('dog', 'Bello')}
    Animal.unseal()                         # unseal it!
    c = Animal('dog', name='Tessa')         # Animal('dog', 'Bello') now is ok!
    print(Animal.instances())               # {'Bello': Animal('dog', 'Bello'),
                                            #  'Tessa': Animal('dog', 'Tessa')}

    # Case 7: Every instance knows its multiton
    #    ---> By default object.multiton contains the multiton object
    a = Animal('dog', name='Bello')         # Animal('dog', 'Bello')
    print(a.multiton)                       # <decoratory.multiton.Multiton...>
    print(a.multiton.instances())           # {'Bello': Animal('dog', 'Bello')}

    # Case 8: Customize attribute name: Multiton(key='name', attrib='my_multi')
    #    ---> Customized object.my_multi contains the multiton object
    a = Animal('dog', name='Bello')         # Animal('dog', 'Bello')
    print(a.my_multi)                       # <decoratory.multiton.Multiton...>
    print(a.my_multi.instances())           # {'Bello': Animal('dog', 'Bello')}

    # Case 9: decoration Multiton(key=lambda spec, name: 'a' in name)
    #    ---> Warning: Corrupting the directory by changing the key!
    a = Animal('dog', name='Bello')         # Animal('dog', 'Bello')
    print(a.multiton.instances())           # {False: Animal('dog', 'Bello')}
    a.name = 'Tessa'                        # Turns key from False to True, but
    print(a.multiton.instances())           # {False: Animal('dog', 'Tessa')}
                                            # only attribute self.name changed!
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Multiton"
__module__ = "multiton.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "http://evation.eu"
__copyright__ = f"(c) copyright 2020-2023, {__company__}"
__created__ = "2020-01-01"
__version__ = "0.1.0.1"
__date__ = "2023-06-12"
__time__ = "14:49:52"
__state__ = "Beta"
__license__ = "PSF"

__all__ = ["Multiton"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from typing import Union
from decoratory.basic import F


# -----------------------------------------------------------------------------
# Classes
class Multiton:
    """**Multiton**

    A multiton is a design pattern that extends the singleton pattern.
    Whereas the singleton allows for exactly one instance per class, the
    multiton pattern ensures one single (unique) instance per key value
    (of a dictionary).

    In this implementation the key parameter can be either any immutable type
    or a callable returning such an immutable type which can be used as a key
    of a dictionary. In case of an invalid key, key is set None and the
    multiton simply collapses to a singleton.

    Setting the attrib parameter to a valid attribute name string the multiton
    is attributed in the new instantiated substitute object, is the name
    invalid, the attribute name 'multiton' is chosen.

    By default, the sealed parameter is set False, so for every new key a new
    (unique) object is instantiated. When sealed (e.g. later in the process)
    is set True the dictionary has completed, i.e. restricted to the current
    object set and any new key raises a KeyError.

    Warning: Classifications into the multiton directory are done only once on
             initial data, the object's __init__ parameters! Subsequent changes
             affecting the key are not reflected in the multiton directory,
             i.e. the directory may then be corrupted by such modifications.
             Therefore, never change key related values of classified objects!

    Attributes
    ----------
    substitute: object
        A type to be made a multiton.

    key: int or str or callable
        Unique (immutable) key for the instance dictionary.

    attrib: str
        Name of the attribute containing the multiton instance.

    Methods
    -------
    seal(self):
        Seal multiton of unique key instances.

    unseal(self):
        Unseal multiton of unique key instances.

    issealed(self):
        Is the multiton of unique key instances sealed?

    instances(self):
        Dictionary of all instance representations.

    Example
    -------

    from decoratory.multiton import Multiton

    # --- For alternative decorations see cases below!
    @Multiton
    class Animal:
        def __init__(self, spec, name):
            self.spec = spec
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.spec}', '{self.name}')"

    # Create instances
    a = Animal('dog', name='Bello')
    b = Animal('cat', name='Mausi')
    c = Animal('dog', name='Tessa')

    # Case 1: decoration @Multiton or @Multiton() or @Multiton(key=17) or ...
    #    ---> With no or fixed key the Multiton acts like a Singleton
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('dog', 'Bello')
    print(c)                                # Animal('dog', 'Bello')

    # Case 2: decoration Multiton(key=lambda spec, name: 'a' in name)
    #    ---> key is a function evaluating the attribute name from __init__(..)
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('cat', 'Mausi')
    print(c)                                # Animal('cat', 'Mausi')

    # Case 3: decoration Multiton(key=0)    # take args[0]
    #    ---> integer key=val references args[val] from __init__(.., spec,..)
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('cat', 'Mausi')
    print(c)                                # Animal('dog', 'Bello')

    # Case 4: decoration Multiton(key='0')  # take kwargs['0'] does not exist!
    #    ---> string key=str references kwargs[str], here leading to None
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('dog', 'Bello')
    print(c)                                # Animal('dog', 'Bello')

    # Case 5: decoration Multiton(key='name') # take kwargs['name'] does exist!
    #    ---> string key=str references kwargs[str] from __init__(..,.., name)
    print(a)                                # Animal('dog', 'Bello')
    print(b)                                # Animal('cat', 'Mausi')
    print(c)                                # Animal('dog', 'Tessa')

    # Case 6: decoration Multiton(key='name'): Seal after Bello
    #    ---> string key=str references kwargs[str] (e.g. self.name)
    Animal.instances().clear()              # Reset...
    print(Animal.instances())               # ... to an empty dictionary
    print(Animal.issealed())                # False
    a = Animal('dog', name='Bello')         # Animal('dog', 'Bello')
    Animal.seal()                           # seal it!
    print(Animal.issealed())                # True
    b = Animal('dog', name='Bello')         # Returns a-objekt from multiton
    print(a is b)                           # True
    try:
        c = Animal('dog', name='Tessa')     # KeyError, Animal is sealed!
    except KeyError as ex:
        print(f"For '{ex.args[1]}' {ex.args[0]}")
    print(Animal.instances())               # {'Bello': Animal('dog', 'Bello')}
    Animal.unseal()                         # unseal it!
    c = Animal('dog', name='Tessa')         # Animal('dog', 'Bello') now is ok!
    print(Animal.instances())               # {'Bello': Animal('dog', 'Bello'),
                                            #  'Tessa': Animal('dog', 'Tessa')}

    # Case 7: Every instance knows its multiton
    #    ---> By default object.multiton contains the multiton object
    a = Animal('dog', name='Bello')         # Animal('dog', 'Bello')
    print(a.multiton)                       # <decoratory.multiton.Multiton...>
    print(a.multiton.instances())           # {'Bello': Animal('dog', 'Bello')}

    # Case 8: Customize attribute name: Multiton(key='name', attrib='my_multi')
    #    ---> Customized object.my_multi contains the multiton object
    a = Animal('dog', name='Bello')         # Animal('dog', 'Bello')
    print(a.my_multi)                       # <decoratory.multiton.Multiton...>
    print(a.my_multi.instances())           # {'Bello': Animal('dog', 'Bello')}

    # Case 9: decoration Multiton(key=lambda spec, name: 'a' in name)
    #    ---> Warning: Corrupting the directory by changing the key!
    a = Animal('dog', name='Bello')         # Animal('dog', 'Bello')
    print(a.multiton.instances())           # {False: Animal('dog', 'Bello')}
    a.name = 'Tessa'                        # Turns key from False to True, but
    print(a.multiton.instances())           # {False: Animal('dog', 'Tessa')}
                                            # only attribute self.name changed!
    """

    def __init__(self,
                 substitute: type = None,
                 *args: object,
                 key: Union[int, str, callable, None] = None,
                 attrib: Union[str, None] = None,
                 **kwargs: object) -> None:
        """Set up a multiton.

        substitute is the first positional argument defining the type to be
        decorated, in pie notation:  @Multiton class A <-> A = Multiton(A).

        key is the first keyword argument and defines the dictionary key:
         - key=int: references positional arguments args[int(key)]
         - key=str: references keyword arguments kwargs[str(key)]
         - key=callable: evaluates to an immutable object, e.g. str, tuple, ...

        attrib is a string for renaming the multiton attribute name.

        Parameters:
            substitute (object): A type to be made a multiton.
            key: (int or str or callable): Unique (immutable) instance key.
            attrib: str: Name of the attribute of the multiton instance.

        Returns:
            self (object): Multiton decorator instance
        """
        self.__set__substitute(substitute)
        self.__key = key
        self.__attrib = attrib

        self.__instances = dict()  # Dictionary for unique key instances
        self.__sealed = False

        # Decorator Arguments Pattern
        if self.__substitute is not None:
            # Decoration without parameter(s)
            self.__set__substitute(F(self.__substitute, *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

            # Add attribute
            try:
                setattr(self.__get__substitute().callee, self.__attrib, self)
            except (TypeError, AttributeError, Exception):
                setattr(self.__get__substitute().callee,
                        self.__class__.__name__.lower(), self)

    def __call__(self, *args, **kwargs):
        """Apply the decorator.

        Parameters:
            substitute (object): A type to be made a singleton.

        Returns:
            instance (object): A unique object instance from multiton key.
        """
        # Decorator Arguments Pattern
        if self.__substitute is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

            # Add attribute
            try:
                setattr(self.__get__substitute().callee, self.__attrib, self)
            except (TypeError, AttributeError, Exception):
                setattr(self.__get__substitute().callee,
                        self.__class__.__name__.lower(), self)

            return self
        else:  # *** Wrapper ***
            # If no current values, take defaults
            if args or kwargs:
                subst = F(self.__get__substitute().callee, *args, **kwargs)
            else:
                subst = self.__get__substitute()

            # Calculate key from callable or read key from arguments
            try:
                if callable(self.__key):
                    d_key = self.__key(*subst.callee_args,
                                       **subst.callee_kwargs)
                elif isinstance(self.__key, int):
                    d_key = subst.callee_args[self.__key]
                else:
                    d_key = subst.callee_kwargs.get(self.__key, self.__key)
                instance = self.__instances.get(d_key, None)
            except (IndexError, KeyError, TypeError, Exception):
                d_key = None
                instance = self.__instances.get(d_key, None)

            # Create and store new or return existing instance (by key)
            if instance is None:
                if self.__sealed:
                    raise KeyError(f"{self.__name__} is sealed.", d_key)
                instance = self.__instances.setdefault(d_key, subst.eval())

            return instance

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    # Methods
    def seal(self):
        """Seal multiton of unique key instances.

        Parameters:
            None.

        Returns:
            None.
        """
        self.__sealed = True

    def unseal(self):
        """Unseal multiton of unique key instances.

        Parameters:
            None.

        Returns:
            None.
        """
        self.__sealed = False

    def issealed(self):
        """Is the multiton of unique key instances sealed?

        Parameters:
            None.

        Returns:
            True/False (bool): Seal state.
        """
        return self.__sealed

    def instances(self):
        """Dictionary of all instance representations.

        Parameters:
            None.

        Returns:
            Instance (dict): Dictionary of all multiton instances.
        """
        return self.__instances


# -----------------------------------------------------------------------------
# Entry Point
if __name__ == '__main__':
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(Multiton,),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)
