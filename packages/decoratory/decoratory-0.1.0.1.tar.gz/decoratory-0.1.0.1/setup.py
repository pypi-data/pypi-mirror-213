#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
"""**Decorators**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "decoratory"
__module__ = "setup.py"
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

# -----------------------------------------------------------------------------
# Libraries
from os.path import join
from setuptools import setup, find_packages
from setuptools.command.install import install

# -----------------------------------------------------------------------------
# Parameters
root = "Sources"

with open("Readme.rst", "r") as f:
    description = f.read()

with open("Requirements.txt", "r") as f:
    requirements = [str(req) for req in f.read().splitlines() if req]


def version_check():
    """Keep versions in sync"""
    from Sources.decoratory.__main__ import __version__ as version
    assert version == __version__, (
        f"\n\n{'':=^79s}\n"
        f"{' Version mismatch: __main__.version != setup.version ':=^79s}\n"
        f"{'':=^79s}")


# -----------------------------------------------------------------------------
# Excecute
setupargs = dict(
    # General
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=f'{__author__} <{__email__}>',
    maintainer=f'{__author__}',
    maintainer_email=f'{__author__} <{__email__}>',
    url=__url__,
    download_url=__url__,
    description='Decorators: Singleton, Multiton, Observer, generic Wrapper.',
    long_description=description,
    long_description_content_type='text/x-rst',
    project_urls={
        'Projekt': __url__,
        'Release Notes': __url__,
        'Download': __url__},
    keywords='decorator singleton multiton observer wrapper',
    # Technical
    license=__license__,
    platforms=['Operating System :: OS Independent'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'],
    # Modules, Files and Data
    # https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#finding-simple-packages
    packages=find_packages(where=root),
    package_dir={"": root},
    package_data={},
    py_modules=[],
    data_files=[(f"lib/site-packages/{__title__}",
                 ["License.txt", "Readme.rst", "Requirements.txt"])],
    entry_points={},
    # Dependencies
    python_requires='>=3.7',
    setup_requires=[],
    install_requires=requirements,
    # Post install
    # cmdclass={'install': CustomInstall},
)
setup(**setupargs)

version_check()
