#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Wrapper**

    A wrapper encloses the original function with an

     - (optional) before call functionality, and/or
     - (optional) after  call functionality, and/or

    substitutes the original functionality with an

     - (optional) replace call functionality.

    All three decorator parameters, before, after and replace, can be combined
    with each other and support both single callables and (nested) lists of
    F-types (imported from module decoratory.basic, see below for details).
    In addition, replace supports passing results from successive replacement
    calls through an optional keyword argument named result (defaut value is
    None).

    Attributes
    ----------
    substitute: object (getter)
        A type to be made a multiton.

    before: callable or list
        (List of) callable(s) to be executed before substitute.

    replace: callable or list
        (List of) callable(s) replacing the substitute.

    after: callable or list
        (List of) callable(s) to be executed after substitute.

    Methods
    -------
        None.

    Example
    -------

    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    # --- Overwrite default parameter values

    # Case 1: Dynamic decoration with decorator arguments, only
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    # Function call with default parameters
    some_function()                 # value = 'original'
    some_function = Wrapper(some_function, value="changed")
    some_function()                 # value = 'changed'

    # Case 2: Static decoration with before and after functionalities
    def print_message(message: str = "ENTER"):
        print(message)

    @Wrapper(before=print_message, after=F(print_message, "LEAVE"))
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    # Function call with decoration: before and after
    some_function()                 # ENTER
                                    # value = 'original'
                                    # LEAVE

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

    # Function call with decoration: before, after and replacement
    default_printer()               # ENTER         (before)
                                    # result = 1    (replacement_printer, 1)
                                    # result = 4    (replacement_printer, 3)
                                    # result = 9    (replacement_printer, 5)
                                    # LEAVE         (after)
                                    # 9             (output default_printer)
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Wrapper"
__module__ = "wrapper.py"
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

__all__ = ["Wrapper"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from decoratory.basic import F, Parser


# -----------------------------------------------------------------------------
# Classes
class Wrapper:
    """**Wrapper**

    A wrapper encloses the original function with an

     - (optional) before call functionality, and/or
     - (optional) after  call functionality, and/or

    substitutes the original functionality with an

     - (optional) replace call functionality.

    All three decorator parameters, before, after and replace, can be combined
    with each other and support both single callables and (nested) lists of
    F-types (imported from module decoratory.basic, see below for details).
    In addition, replace supports passing results from successive replacement
    calls through an optional keyword argument named result (defaut value is
    None).

    Attributes
    ----------
    substitute: object (getter)
        A type to be made a multiton.

    before: callable or list
        (List of) callable(s) to be executed before substitute.

    replace: callable or list
        (List of) callable(s) replacing the substitute.

    after: callable or list
        (List of) callable(s) to be executed after substitute.

    Methods
    -------
        None.

    Example
    -------

    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    # --- Overwrite default parameter values

    # Case 1: Dynamic decoration with decorator arguments, only
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    # Function call with default parameters
    some_function()                 # value = 'original'
    some_function = Wrapper(some_function, value="changed")
    some_function()                 # value = 'changed'

    # Case 2: Static decoration with before and after functionalities
    def print_message(message: str = "ENTER"):
        print(message)

    @Wrapper(before=print_message, after=F(print_message, "LEAVE"))
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    # Function call with decoration: before and after
    some_function()                 # ENTER
                                    # value = 'original'
                                    # LEAVE

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

    # Function call with decoration: before, after and replacement
    default_printer()               # ENTER         (before)
                                    # result = 1    (replacement_printer, 1)
                                    # result = 4    (replacement_printer, 3)
                                    # result = 9    (replacement_printer, 5)
                                    # LEAVE         (after)
                                    # 9             (output default_printer)
    """

    def __init__(self,
                 substitute: callable or type = None,
                 *args: object,
                 before: callable or list = None,
                 replace: callable or list = None,
                 after: callable or list = None,
                 **kwargs: object) -> None:
        """
        substitute is the first positional argument defining the type to be
        decorated, in pie notation:  @Wrapper class A <-> A = Wrapper(A).

        Parameters:
            substitute (object): A type to be made a wrapper.
            before (object): (List of) callable(s) to be executed before
            replace (object): (List of) callable(s) replacing the substitute
            after (object): (List of) callable(s) to be executed after

        Returns:
            self (object): Wrapper decorator instance
        """
        self.__set__substitute(substitute)
        self.__set__before(before)
        self.__set__replace(replace)
        self.__set__after(after)

        # Decorator Arguments Pattern
        if self.__substitute is not None:
            # Decoration without parameter(s)
            self.__set__substitute(F(self.__substitute, *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

    def __call__(self, *args, **kwargs):
        # Decorator Arguments Pattern
        if self.__substitute is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())
            return self
        else:  # *** Wrapper ***
            # Action BEFORE
            if self.__before:
                for before in self.__before:
                    before.eval()

            # Delegation vs. REPLACE
            if self.__replace:
                # Replacement
                result = None
                if args or kwargs:
                    for replace in self.__replace:
                        d = replace.callee.__kwdefaults__
                        if d and 'result' in d:
                            d['result'] = result
                        result = F(replace.callee, *args, **kwargs).eval()
                else:
                    for replace in self.__replace:
                        d = replace.callee.__kwdefaults__
                        if d and 'result' in d:
                            d['result'] = result
                        result = replace.eval()
            else:
                # Delegation
                if args or kwargs:
                    result = F(self.__get__substitute().callee, *args,
                               **kwargs).eval()
                else:
                    result = self.__get__substitute().eval()

            # Action AFTER
            if self.__after:
                for after in self.__after:
                    after.eval()

            return result

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    def __get__before(self):
        return self.__before

    def __set__before(self, value):
        self.__before: list = Parser.eval(value)

    before = property(__get__before)

    def __get__replace(self):
        return self.__replace

    def __set__replace(self, value):
        self.__replace: list = Parser.eval(value)

    replace = property(__get__replace)

    def __get__after(self):
        return self.__after

    def __set__after(self, value):
        self.__after: list = Parser.eval(value)

    after = property(__get__after)


# -----------------------------------------------------------------------------
# Simple example
if __name__ == '__main__':
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(Wrapper,),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)
