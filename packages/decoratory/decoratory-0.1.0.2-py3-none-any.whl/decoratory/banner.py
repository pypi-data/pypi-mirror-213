#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Banner**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Banner"
__module__ = "banner.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "http://evation.eu"
__copyright__ = f"(c) copyright 2020-2023, {__company__}"
__created__ = "2020-01-01"
__version__ = "0.1.0.3"
__date__ = "2023-06-13"
__time__ = "18:03:50"
__state__ = "Beta"
__license__ = "PSF"

__all__ = ["__banner"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from sys import argv
from os.path import dirname, join


# -----------------------------------------------------------------------------
# Banner Display
def __banner(title, version, date, time, docs,
             author: str = __author__,
             maintainer: str = __maintainer__,
             company: str = __company__,
             email: str = __email__,
             url: str = __url__,
             copyright: str = __copyright__,
             state: str = __state__,
             license: str = __license__,
             file_license: str = join("data", "License.txt")):
    """**Banner**

    Banner is an auxiliary module for displaying package and module
    information.
    """
    module = title.lower()
    name = title.capitalize()

    arg = argv[1].strip().lower() if len(argv) > 1 else "message"
    if arg in "--version":
        print(f"{module}: Version {version}, "
              f"Build {date} {time}, State '{state}'")
    elif arg in "--copyright":
        print(f"{copyright}")
    elif arg in "--license" or arg in "--licence":
        print(f"\n{'-' * 79}")
        print(f"{title} ships under the license: {license}".center(79))
        print(f"{'-' * 79}")
        try:
            with open(join(dirname(__file__), file_license), "r") as f:
                txt = f.read()
            print("\n" + txt)
        except (FileNotFoundError, Exception):
            print("*** No additional data accessible. "
                  f"Please look for file '{file_license}' ***".center(79, " "))
        print(f"{'-' * 79}")
    elif arg in "--documentation":
        print()
        for doc in docs:
            print(f"{' ' + doc.__name__ + ' ':-^79s}\n")
            print(doc.__doc__)  # print(help(doc))
        print(f"{'-' * 79}")
    elif arg in "--information":
        print(f"\nPeople and contact information for module {module}:\n")
        print(f"Author    : {author}")
        print(f"Maintainer: {maintainer}")
        print(f"Company   : {company}")
        print(f"Email     : {email}")
        print(f"Web       : {url}")
    else:
        print(f"""
-------------------------------------------------------------------------------
{title.upper(): ^79}
-------------------------------------------------------------------------------

{module} is a Python module you cannot execute directly from command line.
This module provides a {name} decorator.

{module} is provided by {company} under the {license} license included with 
this module. It comes without any warranty, but with the intention of saving 
working time and improving code quality and productivity.

All kinds of bugs, questions, improvement suggestions, change requests etc. 
are welcome to be directed to the product maintainers email {email}.

The current version of the installed package is:
{module}: Version {version}, Build {date} {time}, State '{state}'

Syntax:   python -m decoratory.{module} [option]

Possible options are:

  -h, --help            show this help message
  -v, --version         show module {module} version information      
  -c, --copyright       show module {module} copyright statement
  -l, --license         show module {module} license statement (License.txt)
      --licence         an alias to --license
  -d, --documentation   display selected module code documentation
  -i, --info            people and contact information

-------------------------------------------------------------------------------
{copyright: <69s}{date: >10s}
-------------------------------------------------------------------------------
""")


# -----------------------------------------------------------------------------
# Entry Point
if __name__ == '__main__':
    __banner(title=__title__,
             version=__version__,
             date=__date__,
             time=__time__,
             docs=(__banner,))
