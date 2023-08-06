#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Observer Pattern**

The observer pattern is generally used to inform one or more registered
objects (observers, subscribers, objects) about a specific action of a given
observed object (observable, publisher, subject).

This implementation offers different possibilities to decorate a function/class
as an observable resp. observer.

-------------------------------------------------------------------------------
A) Observable decoration

The simplest as well as most pythonic version for decoration is to decorate
only the observable elements. This is possible, because all observer pattern
functionalities are located in the BaseClass (=BaseObservable) of the
Observable decorator while the BaseClass (=BaseObserver) of the Observer
decorator is empty, here. From both BaseClasses can be inherited to extend
their functionalities.

Example:

    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

    @Observable(observers=F(person, 'Hey, dog!'))
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")

This results in:

    1. Calling person() prints:
        person says 'Hello?'            # person is acting

    2. Calling dog() prints:
        dog acts 'Woof!'                # dog is acting, default dog
        person says 'Hey, dog!'         # person is a custom. observer to dog

Obviously, the addressed observer, the person, must be declared before the
observed, the dog. In order to make the observers more visible in the code, an
(optional) Observer decoration is supported, i.e.

    @Observer
    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

making person to an Observer, but here, with the same result as above.

Because of hierarchies in stacked observer patterns a more detailed managing
of the observed observable objects can be necessary.

Example:

    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

    @Observable(observers=F(person, 'Hey, cat!'))
    def cat(act: str = "Meow!"):
        print(f"{cat.__name__} acts '{act}'")

    @Observable(observers=[F(cat, 'Roar!'), F(person, 'Hey, dog!')])
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")

This results in:

    1. Calling person() prints:
        person says 'Hello?'            # person is acting

    2. Calling cat() prints:
        cat acts 'Meow!'                # cat    is acting
        person says 'Hey, cat!'         # person is an observer to cat

    3. Calling dog() prints:
        dog acts 'Woof!'                # dog    is acting
        cat acts 'Roar!'                # cat    is an observer to dog
        person says 'Hey, cat!'         # person is an observer to cat
        person says 'Hey, dog!'         # person is an observer to dog

The order of the reactions comes from the list order where cat observes dog
prior to person. Switching this order to

    @Observable(observers=[F(person, 'Hey, dog!'), F(cat, 'Roar!')])
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")

results in

    3. Calling dog() prints:
        dog acts 'Woof!'                # dog    is acting
        person says 'Hey, dog!'         # person is an observer to dog
        cat acts 'Roar!'                # cat    is an observer to dog
        person says 'Hey, cat!'         # person is an observer to cat

Calling dog() results in three observer calls because dog() addresses the
'observed cat' informing person about its own action. If this behavior is not
desired, dog can address the 'native cat' using cat's substitute instead, i.e.

    @Observable(observers=[F(cat.substitute.callee, 'Roar!'),
                           F(person, 'Hey, dog!')])
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")

results in

    3. Calling dog() prints:
        dog acts 'Woof!'                # dog    is acting
        cat acts 'Roar!'                # cat    is an observer to dog
        person says 'Hey, dog!'         # person is an observer to dog

And again, cat acts before person because of the order of the observer list.

-------------------------------------------------------------------------------
B) Observer decoration

In this reversed decoration the Observer decorator defines its observable.
Because an observer decoration makes use of observable methods the
observable(s) always has to be declared before any of its observer(s)!

    1) Rule: Declare Observables before Observers

For multiple decoration the **order of decoration** matters. At the end it has
to be an observable for following observers

    2) Rule: Decorate @Observer before @Observable

Example:

    @Observable
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")

    @Observable                             # 2) Rule: cat before person
    @Observer(observables=X(dog, 'Roar!'))  # 1) Rule: dog before cat
    def cat(act: str = "Meow!"):
        print(f"{cat.__name__} acts '{act}'")

    @Observer(observables=[X(dog, 'Hey, dog!'), X(cat, say='Hey, cat!')])
    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

This results in:

    1. Calling person() prints:
        person says 'Hello?'            # person is acting

    2. Calling cat() prints:
        cat acts 'Meow!'                # cat    is acting
        person says 'Hey, cat!'         # person is an observer to cat

    3. Calling dog() prints:
        dog acts 'Woof!'                # dog    is acting
        cat acts 'Roar!'                # cat    is an observer to dog
        person says 'Hey, dog!'         # person is an observer to dog

Again, the 'observable cat' person observes is not the 'native cat' observing
dog, thus, person reacts only to dog but not to the induced cat by dog. If
desired, that person reacts to the dog induced cat also, simply switch the
decoration order and address the substitute of the 'observer cat':

    @Observer(observables=X(dog, 'Roar!'))
    @Observable
    def cat(act: str = "Meow!"):
        print(f"{cat.__name__} acts '{act}'")

    @Observer(observables=[X(dog, 'Hey, dog!'),
                           X(cat.substitute.callee, say='Hey, cat!')])
    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

Then, in 3. the result will be:

    3. Calling dog() prints:
        dog acts 'Woof!'                # dog    is acting
        cat acts 'Roar!'                # cat    is an observer to dog
        person says 'Hey, cat!'         # person is an observer to cat
        person says 'Hey, dog!'         # person is an observer to dog

-------------------------------------------------------------------------------
C) Static decoration

Both techniques, A) and B), are static, in the sense, decorations are done in
pie notation evaluated at compile time. They are applied to (static) functions.

Decoration of a class by default addresses decoration of the class constructor:

    @Observable
    class Dog:
        def __init__(self):
            pass

should be understood as

    class Dog:
        @Observable
        def __init__(self):
            pass

ATTENTION:  Calling __init__ results in a new instance! This means calling the
            observable induces instantiation of a new observer object, surely
            in not any case this is the desired action - so, be careful here!

To address other methods, both decorators, Observable and Observer, support the
methods parameter for a single or even a list of methods by name strings. In
these cases the class itself remains undecorated but the listed method(s) are
decorated.

    @Observable(methods=['meth1', F('meth2', 13, key='number')])
    class A:
        def meth1(self, val=0):
            pass
        def meth2(self, val=0, key='decimal'):
            pass

should be understood as

    class A:
        @Observable
        def meth1(self, val=0):                 # Using declaration defaults!
            pass
        @Observable
        def meth2(self, val=13, key='number'):  # Using decoration defaults!
            pass

Clearly, these techniques allow to address static methods and class methods
being declared at compile time. For instance methods things are different,
because instances are not available at compile time. They are generated within
the init constructor. Therefore, instance methods are decorated best in the
object constructor.

Example:

    class Agent:
        @classmethod
        def inform(cls, value):
            print(f"Informed value is: {value}")

        def report(self, value):
            print(f"Reported value is: {value}")

    class Actor:
        def __init__(self):
            self.a = 1
            print(f"Initialization: a = {self.a}")
            self.modify = Observable(observers=[
                F(Agent.inform, 'unknown'),
                F(Agent().report, 'undef')])(self.modify)

        def modify(self, value=1):
            self.a += value
            print(f"Modification  : a = {self.a}")

Every Actor instance defines its modify method as an observable reporting every
modification of self.a to the class method Agent.inform as well as to an
instance method Agent().report. But at init no value data is available, so only
a static reporting will be feasible this way. Running

    a = Actor()
    a.modify(13)

will generate the messages:

    Initialization: a = 1
    Modification  : a = 14
    Informed value is: unknown
    Reported value is: undef

But this problem can be solved i.e. adding the attribute

    activate=Activation.NONE

to the Observable definition in init to switch off default Activation.AFTER
and add an individualized dispatch within the modify method

    self.modify.observable.dispatch(None, value)        or
    self.modify.observable.dispatch(value=value)

and the prints look like

    Initialization: a = 1
    Modification  : a = 14
    Reported value is: 13
    Informed value is: 13

-------------------------------------------------------------------------------
D) Dynamic decoration

Decoration, registration etc. can also be done outside the class(es).
Observers can be registered and unregistered on demand in the program.

Example:

    class Note:                             # Observer without decoration!
        def info(self, thing):
            print(f"Note.info: val = {thing.a}")

    class Thing:                            # Observable without decoration!
        def __init__(self, a=0):
            self._a = a
        def inc(self):
            self._a += 1
        def get_a(self):
            return self._a
        def set_a(self, value):
            self._a = value
        a = property(get_a, set_a)

Some typical actions could be:

    # Preparation
    nti = Note()                            # Note instance
    thg = Thing()                           # Thing instance

    thg.inc = Observable(thg.inc)           # Late method decoration
    Thing.set_a = Observable(Thing.set_a)   # Late property decoration
    Thing.a = property(Thing.get_a, Thing.set_a)

    thg.inc.observable.register(F(nti.info, thg))
    thg.set_a.observable.register(F(nti.info, thing=thg))

    # Usage
    thg.inc()                               # Method   observers dispatched
    thg.a = 2                               # Property observers dispatched

    thg.inc.observable.dispatch(nti.info, Thing(3))
    thg.set_a.observable.dispatch(nti.info, Thing(4))

This will print:

    Note.info: val = 1                      # from observing thg.inc()
    Note.info: val = 2                      # from observing thg.a = 2
    Note.info: val = 3                      # by thg.inc.observable
    Note.info: val = 4                      # by thg.set_a.observable
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Observer"
__module__ = "observer.py"
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

__all__ = ["Observer", "BaseObserver", "Observable", "BaseObservable"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from typing import Union
from decoratory.basic import Activation, F, Parser, X


# -----------------------------------------------------------------------------
# Classes
class BaseObservable:
    """**Observable Base Class**

    A base implementation of the (abstract) observable base class. It manages
    (abstract) observers (of F-type) within a private dictionary using the
    methods:

    register  : Register an observer for callback
    unregister: Unregister an observer
    dispatch  : Dispatch a given observer or even all observers
    observers : Dictionary of all registered observers (of F-type)

    While the methods register, unregister and observers only handles given
    data into F objects and/or collects them, the dispatch method applies F's
    eval method (without arguments!) to them. It's in the user's responsibility
    to make sure that these calls succeed, i.e. for a class or instance/object
    method of class A or an instance a = A():
     - Registration call:   F(a.method, *args, **kwargs).eval()         or
                            F('method', a, *args, **kwargs).eval()      but not
     - Dynamic call:        F('method', *args, **kwargs).eval(obj=a)
    """

    def __init__(self, *args, **kwargs) -> None:
        # Python 3.7ff.: Dictionary order is guaranteed to be insertion order.
        self.__observers = dict()  # dict of F-type observers: callee is key!

        # if args or kwargs:
        #     raise NotImplementedError(
        #     f"Abstract class {self.__class__.__name__} has no arguments.")
        self.args = args
        self.kwargs = kwargs

    # Methods of the Observer Pattern
    def register(self,
                 observer: Union[F, callable, str],
                 *observer_args,
                 **observer_kwargs) -> None:
        """**Register a function (callable) or method (str) for callback**

        @param observer:        Callback function or method str of the observer
        @param observer_args:   The (default) positional arguments for callback
        @param observer_kwargs: The (default) keyword    arguments for callback
        @rtype:                 NoneType
        """
        if isinstance(observer, F):
            if observer_args or observer_kwargs:
                observer.callee_args = observer_args
                observer.callee_kwargs = observer_kwargs
            self.__observers[observer.callee] = observer  # Override mode
        elif callable(observer) or isinstance(observer, str):
            obs = F(observer, *observer_args, **observer_kwargs)
            self.__observers[observer] = obs
        else:
            raise TypeError(f"'{observer}' cannot be registered.")

    def unregister(self,
                   observer: Union[F, callable, str, None] = None) -> None:
        """**Unregister an observer**

        If the observer parameter is omitted (None), all registered observers
        will be unregistered.

        @param observer: The (optional) observer callable to be unregistered
        @rtype:          NoneType
        """
        if observer is None:
            self.__observers.clear()
        elif isinstance(observer, F):
            self.__observers.pop(observer.callee, None)  # Quiet mode
        elif callable(observer) or isinstance(observer, str):
            self.__observers.pop(observer, None)  # Quiet mode
        else:
            raise TypeError(f"'{observer}' cannot be unregistered.")

    def dispatch(self,
                 observer: Union[F, callable, str, None] = None,
                 *observer_args,
                 **observer_kwargs) -> None:
        """**Dispatch an observer**

        If the observer parameter is omitted (None), all registered observers
        will be dispatched.

        @param observer:        The observer's callable to be dispatched
        @param observer_args:   The (default) positional arguments for dispatch
        @param observer_kwargs: The (default) keyword    arguments for dispatch
        @rtype:                 NoneType
        """
        if observer is None:
            # Registration call using default arguments, no extra eval obj!
            if observer_args or observer_kwargs:
                for obs in self.__observers.values():
                    F(obs.callee, *observer_args, **observer_kwargs).eval()
            else:
                for obs in self.__observers.values():
                    obs.eval()
        elif isinstance(observer, F):
            # Dynamic call using current/default arguments, no extra eval obj!
            if observer_args or observer_kwargs:
                F(observer.callee, *observer_args, **observer_kwargs).eval()
            else:
                observer.eval()
        elif callable(observer):
            # Dynamic call using current arguments, no extra eval obj!
            F(observer, *observer_args, **observer_kwargs).eval()
        else:
            raise TypeError(f"'{observer}' cannot be dispatched.")

    def observers(self, classbased=False) -> dict:
        """**Listing of all observers**

        Observers are collected in a dict, which is returned by default with
        classbased=False. Calling with classbased=True returns a dictionary
        with key-value-pair syntax {classname: list(methods)}.

        @param classbased: A boolean switch for returned data structure
        @return:           Dictionary of all observers
        """
        if bool(classbased):
            result = dict()
            for obs in self.__observers.values():
                *skip, cls, mtd = obs.callee.__qualname__.split(".")
                result.setdefault(cls, []).append(repr(obs))
            return result
        else:
            return self.__observers  # Has to be the default (without params)!


class Observable:
    """**Observable** (Publisher, Subject)

    Creating an observable instantiates a callable object which exposes the
    four basic observable pattern methods register, unregister, dispatch and
    observers via an observable attribute for an instance of BaseClass
    (default = BaseObservable) as well as the original decorator arguments,
    if present, like the callable to be substituted, observers, methods and
    activation point in time.
    """

    BaseClass = BaseObservable

    def __init__(self,
                 substitute: Union[callable, type] = None,
                 *args: object,
                 observers: Union[list, F, callable, str] = None,
                 methods: Union[list, F, callable, str] = None,
                 activate: Activation = Activation.AFTER,
                 **kwargs: object) -> None:
        """**Observable** (Publisher, Subject)

        @param substitute: The callable or type to be made an observable
        @param observers: (List of) callable(s) of observers
        @param methods: (List of) callable(s) of method strings
        @param activate: Dispatch activation point of time
        @rtype: NoneType
        """
        self.__set__substitute(substitute)
        self.__set__observers(observers)
        self.__set__methods(methods)
        self.activate = activate

        # Decorator Arguments Pattern
        if self.__substitute is not None:
            # Decoration without parameter(s)
            self.__set__substitute(F(self.__substitute, *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

            # Instance of BaseObservable
            self.__set__observable(Observable.BaseClass())
        else:
            # Decoration with parameter(s)
            self.__set__decorator_args(args)
            self.__set__decorator_kwargs(kwargs)

            # Instance of BaseObservable
            self.__set__observable(Observable.BaseClass(
                *self.__decorator_args, **self.__decorator_kwargs))

    def __call__(self, *args, **kwargs):
        # Decorator Arguments Pattern
        if self.__substitute is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))

            # Decoration of a type means decoration of *all* submitted methods
            if self.__methods:
                # Resolve list of methods:
                subst = self.__get__substitute().callee
                for mtd, mtd_args, mtd_kwargs in self.__methods:
                    if isinstance(mtd, str) and hasattr(subst, mtd):
                        mtds = mtd
                        mtd0 = getattr(subst, mtds)
                    elif callable(mtd):
                        mtds = mtd.__name__
                        mtd0 = mtd
                    else:
                        raise TypeError(f"{mtd} is nor a string nor callable.")
                    # noinspection PyArgumentEqualDefault
                    mtd1 = Observable(
                        None,  # Call with deco arguments (substitute is None)
                        *self.__decorator_args,
                        observers=self.__observers,
                        methods=None,  # Resolved, call to else part below!
                        activate=self.activate,
                        **self.__decorator_kwargs)(mtd0,
                                                   *mtd_args,
                                                   **mtd_kwargs)
                    setattr(subst, mtds, mtd1)

                # Return the undecorated original class
                return subst
            else:
                # Setup observers
                if self.__observers:
                    for observer in self.__observers:
                        self.__observable.register(observer)

                # Complete wrapper and return observable
                update_wrapper(self, self.__get__substitute().callee,
                               updated=())
                return self
        else:  # *** Wrapper ***
            # Dispatch BEFORE
            if self.activate & Activation.BEFORE:
                self.__observable.dispatch()

            # Delegation: apply the substitute, current before default values
            if args or kwargs:
                result = F(self.__get__substitute().callee, *args,
                           **kwargs).eval()
            else:
                result = self.__get__substitute().eval()

            # Dispatch AFTER
            if self.activate & Activation.AFTER:
                self.__observable.dispatch()

            return result

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    def __get__decorator_args(self):
        return self.__decorator_args

    def __set__decorator_args(self, value):
        self.__decorator_args = value

    decorator_args = property(__get__decorator_args)

    def __get__decorator_kwargs(self):
        return self.__decorator_kwargs

    def __set__decorator_kwargs(self, value):
        self.__decorator_kwargs = value

    decorator_kwargs = property(__get__decorator_kwargs)

    def __get__observers(self):
        return self.__observers

    def __set__observers(self, value):
        self.__observers: list = Parser.eval(value)

    observers = property(__get__observers)

    def __get__methods(self):
        return self.__methods

    def __set__methods(self, value):
        self.__methods: list = Parser.eval(value)

    methods = property(__get__methods)

    def __get__observable(self):
        return self.__observable

    def __set__observable(self, value):
        self.__observable = value

    observable = property(__get__observable)

    def __get__activate(self):
        return self.__activate

    def __set__activate(self, value):
        self.__activate = value if isinstance(
            value, Activation) else Activation.NONE

    activate = property(__get__activate, __set__activate)


class BaseObserver:
    """**Observer Base Class**

    A base implementation of the (abstract) observer base class.

    As long as this class, just like here, is an empty dummy, decoration of a
    callable as an observer is optional. If BaseObserver is overwritten and
    assigned to the observers BaseClass attribute all non captured decorator
    args & kwargs will be submitted to be used in customized class
    functionalities.
    """

    def __init__(self, *args, **kwargs):
        # if args or kwargs:
        #     raise NotImplementedError(
        #     f"Abstract class {self.__class__.__name__} has no arguments.")
        self.args = args
        self.kwargs = kwargs


class Observer:
    """**Observer** (Subscriber, Object)

    Creating an observer instantiates a callable object which exposes the
    original decorator arguments, if present, like the callable to be
    substituted, observables and methods.
   """

    BaseClass = BaseObserver

    def __init__(self,
                 substitute: Union[callable, type] = None,
                 *args: object,
                 observables: Union[list, X, callable, str] = None,
                 methods: Union[list, X, callable, str] = None,
                 **kwargs: object) -> None:
        """**Observer** (Subscriber, Object)

        @param substitute: The callable or type to be made an observable
        @param observables: (List of) callable(s) of observables
        @param methods: (List of) callable(s) of method strings
        @rtype: NoneType
            """
        self.__set__substitute(substitute)
        self.__set__observables(observables)
        self.__set__methods(methods)

        # Decorator Arguments Pattern
        if self.__substitute is not None:
            # Decoration without parameter(s)
            self.__set__substitute(F(self.__substitute, *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

            # Instance of BaseObserver
            self.__set__observer(Observer.BaseClass())
        else:
            # Decoration with parameter(s)
            self.__set__decorator_args(args)
            self.__set__decorator_kwargs(kwargs)

            # Instance of BaseObserver
            self.__set__observer(Observer.BaseClass(
                *self.__decorator_args, **self.__decorator_kwargs))

    def __call__(self, *args, **kwargs):
        # Decorator Arguments Pattern
        if self.__substitute is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))

            # Decoration of a type means decoration of *all* submitted methods
            if self.__methods:
                # Resolve list of methods:
                subst = self.__get__substitute().callee
                for mtd, mtd_args, mtd_kwargs in self.__methods:
                    if isinstance(mtd, str) and hasattr(subst, mtd):
                        mtds = mtd
                        mtd0 = getattr(subst, mtds)
                    elif callable(mtd):
                        mtds = mtd.__name__
                        mtd0 = mtd
                    else:
                        raise TypeError(f"{mtd} is nor a string nor callable.")
                    # noinspection PyArgumentEqualDefault
                    mtd1 = Observer(
                        None,  # Call with deco arguments (substitute is None)
                        *self.__decorator_args,
                        observables=self.__observables,
                        methods=None,  # Resolved, call to else part below!
                        **self.__decorator_kwargs)(mtd0,
                                                   *mtd_args,
                                                   **mtd_kwargs)
                    setattr(subst, mtds, mtd1)

                # Return the undecorated original class
                return subst
            else:
                # Register self as a callable object for callback
                # CAUTION: observables is a list of X-objects with semantics
                #     obs = X(observABLE, observER_args, observER_kwargs)
                # The arguments belong to the observer (self) but not to the
                # observable from the observables list!
                if self.__observables:
                    for observable in self.__observables:
                        if isinstance(observable.callee, Observable):
                            observable.callee.observable.register(
                                self, *observable.callee_args,
                                **observable.callee_kwargs)
                        else:
                            raise TypeError(
                                f"{observable.callee} is not an observable.")

                # Complete wrapper and return observer
                update_wrapper(self, self.__get__substitute().callee,
                               updated=())
                return self
        else:  # *** Wrapper ***
            # Delegation: apply the substitute, current before default values
            if args or kwargs:
                return F(self.__get__substitute().callee, *args,
                         **kwargs).eval()
            else:
                return self.__get__substitute().eval()

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    def __get__decorator_args(self):
        return self.__decorator_args

    def __set__decorator_args(self, value):
        self.__decorator_args = value

    decorator_args = property(__get__decorator_args)

    def __get__decorator_kwargs(self):
        return self.__decorator_kwargs

    def __set__decorator_kwargs(self, value):
        self.__decorator_kwargs = value

    decorator_kwargs = property(__get__decorator_kwargs)

    def __get__observables(self):
        return self.__observables

    def __set__observables(self, value):
        self.__observables: list = Parser.eval(value)

    observables = property(__get__observables)

    def __get__methods(self):
        return self.__methods

    def __set__methods(self, value):
        self.__methods: list = Parser.eval(value)

    methods = property(__get__methods)

    def __get__observer(self):
        return self.__observer

    def __set__observer(self, value):
        self.__observer = value

    observer = property(__get__observer)


# -----------------------------------------------------------------------------
# Simple example
if __name__ == '__main__':
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(BaseObserver, Observer, BaseObservable, Observable),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)

    # def __test01():
    #     # ---------------------------------------------------------------------
    #     # Function decoration
    #     @Observable
    #     def dog(act: str = "Woof!"):
    #         """A dog function"""
    #         print(f"{dog.__name__} acts '{act}'")
    #
    #     @Observer(observables=X(dog, 'Roar!'))
    #     @Observable
    #     def cat(act: str = "Meow!"):
    #         """A cat function"""
    #         print(f"{cat.__name__} acts '{act}'")
    #
    #     @Observer(observables=[X(dog, 'Hey, dog!'),
    #                            X(cat.substitute.callee, say='Hey, cat!')])
    #     def person(say: str = "Hello?"):
    #         """A person function"""
    #         print(f"{person.__name__} says '{say}'")
    #
    #     # Some Actions
    #     print("Calling person:")
    #     person()
    #     print("\nCalling cat:")
    #     cat()
    #     print("\nCalling dog:")
    #     dog()
    #
    #
    # def __test02():
    #     # ---------------------------------------------------------------------
    #     # Class decoration (static)
    #     class Agent:
    #         """An agent"""
    #
    #         @classmethod
    #         def inform(cls, value):
    #             """Informer"""
    #             print(f"Informed value is: {value}")
    #
    #         # noinspection PyMethodMayBeStatic
    #         def report(self, value):
    #             """Reporter"""
    #             print(f"Reported value is: {value}")
    #
    #     class Actor:
    #         """An actor"""
    #
    #         def __init__(self):
    #             self.a = 1
    #             print(f"Initialization: a = {self.a}")
    #             self.modify = Observable(observers=[
    #                 F(Agent.inform, 'unknown'),
    #                 F(Agent().report, 'undef')],
    #                 activate=Activation.NONE)(self.modify)
    #
    #         def modify(self, value=1):
    #             """Modification"""
    #             self.a += value
    #             print(f"Modification  : a = {self.a}")
    #             self.modify.observable.dispatch(value=value)
    #
    #     # Some Actions
    #     a = Actor()
    #     a.modify(13)
    #
    #
    # def __test03():
    #     # ---------------------------------------------------------------------
    #     # Class decoration (dynamic)
    #     class DftFormatter:
    #         """Default Formatter"""
    #
    #         def __init__(self, name):
    #             self.name = name
    #             self._data = 0
    #             print(f"{self.__class__.__name__}: "
    #                   f"{self.name} has data {self._data}")
    #
    #         def __str__(self):
    #             return f"{self.__class__.__name__}({self.name}, {self._data})"
    #
    #         def get_data(self):
    #             """Getter"""
    #             return self._data
    #
    #         def set_data(self, value):
    #             self._data = value
    #
    #         data = property(get_data, set_data)
    #
    #     class HexFormatter(DftFormatter):
    #         """Hex Formatter"""
    #
    #         def notify(self, resource):
    #             """Notifier"""
    #             value = hex(resource.data)
    #             print(f"{self.__class__.__name__}: "
    #                   f"{resource.name} has data {value}")
    #
    #     class BinFormatter(DftFormatter):
    #         """Binary Formatter"""
    #
    #         def notify(self, resource):
    #             """Notifier"""
    #             value = bin(resource.data)
    #             print(f"{self.__class__.__name__}: "
    #                   f"{resource.name} has data {value}")
    #
    #     # Instances
    #     print("Instantiation:")
    #     df = DftFormatter('Dfter')
    #     hf = HexFormatter('Hexer')
    #     bf = BinFormatter('Biner')
    #
    #     # Setup Observable for a property
    #     DftFormatter.set_data = Observable(DftFormatter.set_data)
    #     DftFormatter.data = property(DftFormatter.get_data,
    #                                  DftFormatter.set_data)
    #
    #     hf.notify = Observer(hf.notify)  # Optional
    #     bf.notify = Observer(bf.notify)  # Optional
    #
    #     # noinspection PyTypeHints
    #     df.set_data: Observable
    #
    #     # Register Observer with default resource argument
    #     df.set_data.observable.register(F(hf.notify, df))
    #     df.set_data.observable.register(F(bf.notify, resource=df))
    #
    #     # Change data using the property
    #     print("\nChange data: 2")
    #     df.data = 2
    #
    #     # Some additional dispatches
    #     print("\nAdditional dispatches: df, bf, all(2)")
    #     df.set_data.observable.dispatch(hf.notify, df)
    #     df.set_data.observable.dispatch(BinFormatter.notify, bf, df)
    #     print()
    #     df.set_data.observable.dispatch(resource=df)
    #
    #     # List all observers
    #     print("\nList all observers:")
    #     print(df.set_data.observable.observers())
    #     print(df.set_data.observable.observers(classbased=True))
    #
    #     # Unregister bf
    #     print("\nUnregister bf:")
    #     df.set_data.observable.unregister(bf.notify)
    #     print(df.set_data.observable.observers())
    #
    #     # Unregister all
    #     print("\nUnregister all:")
    #     df.set_data.observable.unregister()
    #     print(df.set_data.observable.observers())
    #
    #
    # # -------------------------------------------------------------------------
    # # Apply tests
    # print("----------")
    # __test01()
    # print("----------")
    # __test02()
    # print("----------")
    # __test03()
    # print("----------")
