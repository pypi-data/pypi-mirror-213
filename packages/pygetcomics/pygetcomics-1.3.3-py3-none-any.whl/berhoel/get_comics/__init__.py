#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Download various daily comics.
"""

from __future__ import annotations, generator_stop

# Standard library imports.
import argparse

# Local library imports.
from . import peanuts, garfield

__date__ = "2023/03/18 18:04:22 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2017, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"

try:
    # Local library imports.
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0.invalid0"


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="get_comics", description="Download various periodic comics."
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    return parser


def main(args=None):
    """Get all supported comics."""
    args = get_parser().parse_args()

    print("Get Peanuts.")
    peanuts.main(args)
    print("Get Garfield.")
    garfield.main(args)


if __name__ == "__main__":
    main()

# Local Variables:
# mode: python
# compile-command: "cd ../../ && python setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
