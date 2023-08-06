#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate PDF from several comic PDFs.
"""

from __future__ import annotations, generator_stop

# Standard library imports.
import datetime
from pathlib import Path

# Third party library imports.
import jinja2

__date__ = "2023/03/19 19:37:25 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2017, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


class Keep(object):
    def __init__(self):
        """Keep values."""
        self.cur_month = None

    def set_cur_month(self, inp):
        self.cur_month = inp


class GenPDF(object):
    latex_jinja_env = jinja2.Environment(
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(Path(__file__).with_name("template")),
    )

    def __init__(self, title, base_path, start_date, portrait=False):
        """Generate PDF in comics path."""
        self.title = title
        self.base_path = base_path
        self.start_date = start_date
        self.portrait = portrait

    def gen_dates(self, start_date=None, end_date=None):
        one_day = datetime.timedelta(days=1)
        now = start_date
        if now is None:
            now = self.start_date
        if end_date is None:
            end_date = datetime.date.today()
        while now <= end_date:
            yield now
            now += one_day

    def __call__(self, start_date=None, end_date=None):
        template = self.latex_jinja_env.get_template("book.tex")
        gen_dates = self.gen_dates(start_date, end_date)
        return template.render(
            portrait=self.portrait,
            dates=gen_dates,
            base_path=self.base_path,
            keep=Keep(),
        )


if __name__ == "__main__":
    base_path = Path.home() / "Bilder" / "Dilbert"
    prog = GenPDF("Dilbert", base_path, datetime.date(2016, 12, 20))
    print(prog())

# Local Variables:
# mode: python
# compile-command: "cd ../../../ && python setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
