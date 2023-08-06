#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for get_comics.
"""

# Standard library imports.
from pathlib import Path

# Third party library imports.
import tomli
import pytest

# First party library imports.
from berhoel.get_comics import __version__

__date__ = "2022/08/09 17:51:27 Berthold Höllmann"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


@pytest.fixture
def base_path():
    base_path = Path(__file__).parent
    while not (base_path / "pyproject.toml").is_file():
        base_path = base_path.parent
    return base_path


@pytest.fixture
def config(base_path: Path):
    return base_path / "pyproject.toml"


@pytest.fixture
def toml(config: Path):
    return tomli.load(config.open("rb"))


def test_version(toml):
    """Testing for consistent version number."""
    assert __version__ == toml["tool"]["poetry"]["version"]


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%Y/%02m/%02d %02H:%02M:%02S %L\""
# End:
