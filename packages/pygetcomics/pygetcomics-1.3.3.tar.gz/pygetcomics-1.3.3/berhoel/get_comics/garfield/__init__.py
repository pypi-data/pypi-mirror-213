#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Download Garfield comic strips.
"""

from __future__ import annotations, generator_stop

# Standard library imports.
import argparse
from pathlib import Path

# Local library imports.
from ..gocomics import GoComics

__date__ = "2023/03/19 19:35:26 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2017, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


class Garfield(GoComics):
    "Download daily Garfield comcs fromGoComics."

    # June 19, 1978
    start_year = 1978
    start_month = 6
    start_day = 19

    garfield_path = Path.home() / "Bilder" / "Garfield"

    gif_path_fmt = f'{garfield_path / "%Y" / "%m" / "%d.gif"}'
    png_path_fmt = f'{garfield_path / "%Y" / "%m" / "%d.png"}'
    url_fmt = "http://www.gocomics.com/garfield/%Y/%m/%d"

    statefile_name = garfield_path / "garfield.statfile"


def get_parser() -> argparse.ArgumentParser:
    # First party library imports.
    from berhoel.get_comics import __version__

    parser = argparse.ArgumentParser(
        prog="get_garfield", description="Download daily Garfield comics."
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    return parser


def main(args=None):
    "Main Program."
    if args is None:
        args = get_parser().parse_args()

    Garfield()()


if __name__ == "__main__":
    main()

# Local Variables:
# mode: python
# compile-command: "cd ../../../ && python setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
