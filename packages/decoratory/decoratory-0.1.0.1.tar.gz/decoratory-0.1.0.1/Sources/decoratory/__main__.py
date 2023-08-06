#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Decoratory**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Decoratory"
__module__ = "__main__.py"
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

__all__ = []

# -----------------------------------------------------------------------------
# Libraries & Modules
from sys import argv
from os.path import dirname, join

# -----------------------------------------------------------------------------
# Parameters
module = __title__.lower()
name = __title__.capitalize()


# -----------------------------------------------------------------------------
# A Module Entry Point
def main():
    """Package information"""
    arg = argv[1].strip().lower() if len(argv) > 1 else "message"
    if arg in "--version":
        print(f"{module}: Version {__version__}, "
              f"Build {__date__} {__time__}, State '{__state__}'")
    elif arg in "--copyright":
        print(f"{__copyright__}")
    elif arg in "--license" or arg in "--licence":
        print(f"\n{'-' * 79}")
        print(f"{__title__} ships under the license: {__license__}".center(79))
        print(f"{'-' * 79}")
        try:
            with open(join(dirname(__file__), "License.txt"), "r") as f:
                txt = f.read()
            print("\n" + txt)
        except (FileNotFoundError, Exception):
            print("*** No additional data accessible. "
                  f"Please look for file 'License.txt' ***".center(79, " "))
        print(f"{'-' * 79}")
    elif arg in "--documentation":
        print(f"\n{'-' * 79}")
        try:
            with open(join(dirname(__file__), "Readme.rst"), "r") as f:
                txt = f.read()
            print("\n" + txt)
        except (FileNotFoundError, Exception):
            print("*** No additional data accessible. "
                  f"Please look for file 'Readme.rst' ***".center(79, " "))
        print(f"{'-' * 79}")
    elif arg in "--information":
        print(f"\nPeople and contact information for package {module}:\n")
        print(f"Author    : {__author__}")
        print(f"Maintainer: {__maintainer__}")
        print(f"Company   : {__company__}")
        print(f"Email     : {__email__}")
        print(f"Web       : {__url__}")
    else:
        print(f"""
-------------------------------------------------------------------------------
{__title__.upper(): ^79}
-------------------------------------------------------------------------------

{module} is a Python package you cannot execute directly from command line.

The package provides a framework for Python decorators as well as concrete 
implementations of useful decorators, e.g. Singleton, Multiton, Observable 
and a configurable Wrapper.

{module} is provided by {__company__} under the {__license__} license \
included with 
this package. It comes without any warranty, but with the intention of saving 
working time and improving code quality and productivity.

All kinds of bugs, questions, improvement suggestions, change requests etc. 
are welcome to be directed to the product maintainers email {__email__}.

The current version of the installed package is:
{module}: Version {__version__}, Build {__date__} {__time__}, \
State '{__state__}'

Syntax:   python -m {module}[.module] [option]

For information about the whole package the module command can be left empty, 
for special module information one of the following modules can be addressed:

{'singleton, multiton, wrapper, observer': ^79s}

Possible options are:

  -h, --help            show this help message
  -v, --version         show {module}[.module] version information      
  -c, --copyright       show {module}[.module] copyright statement
  -l, --license         show {module}[.module] license statement (License.txt)
      --licence         an alias to --license
  -d, --documentation   display content of the Readme.rst file
  -i, --info            people and contact information

Example: Display license statement for the multiton module:

{'python -m decoratory.multiton --license': ^79s}
         
-------------------------------------------------------------------------------
{__copyright__: <69s}{__date__: >10s}
-------------------------------------------------------------------------------
""")


# -----------------------------------------------------------------------------
# Execution
if __name__ == '__main__':
    main()
