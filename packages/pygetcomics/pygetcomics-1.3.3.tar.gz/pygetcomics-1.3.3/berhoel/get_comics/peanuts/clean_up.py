#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prepare to delete Wrong Peanut downloads based on MD5.
"""

from __future__ import annotations, generator_stop

# Standard library imports.
import sys
import hashlib
import collections
from pathlib import Path

__date__ = "2022/08/09 17:01:30 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2017, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


FILES = Path(".").glob("*/*/*.png")

HASHES = collections.defaultdict(list)

YEAR = ""

for f_name in FILES:
    m = hashlib.md5()
    year = f_name.parents[1].name
    if year != YEAR:
        print("year:", year)
        YEAR = year
    with f_name.open("rb") as data:
        [m.update(i) for i in data]
    HASHES[m.digest()].append(f_name)

for key, f_list in HASHES.items():
    if len(f_list) > 1:
        for name in f_list:
            sys.stdout.write(f"{name} ")
        sys.stdout.write("\n")

# Local Variables:
# mode: python
# compile-command: "cd ../../../ && python setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
