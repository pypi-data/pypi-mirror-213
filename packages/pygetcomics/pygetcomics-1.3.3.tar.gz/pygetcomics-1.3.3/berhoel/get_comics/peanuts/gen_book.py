#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate Book of all Peanuts comics from images.
"""

from __future__ import annotations, generator_stop

# Standard library imports.
import datetime
from pathlib import Path

__date__ = "2023/03/19 19:38:06 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2017, 2022 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


START_YEAR = 1950
START_MONTH = 10
START_DAY = 2

START_DATE = datetime.date(START_YEAR, START_MONTH, START_DAY)
TODAY = datetime.date.today()

DELTA = datetime.timedelta(days=1)

PATH_FMT = f'{(Path("%Y") / "%m" / "%d")}'


class PeanutsBook(object):
    """Generate LaTeX file for Peanuts comic book."""

    def __init__(self, fname):
        self.cur_date = START_DATE
        self.fname = fname
        self.grpath = None
        self.outp_done = False
        self.side_weekd = 1
        self.side_sund = 2
        self.with_sund = False
        self.days = []

    def run(self):
        """Do the actual processing."""
        with self.fname.open("w") as out:
            self.write_prologue(out)

            while self.cur_date <= TODAY:
                self.wr_image(self.cur_date)
                if self.cur_date.isoweekday() == 7 and self.outp_done:
                    side_weekd = self.side_weekd
                    if self.side_weekd == 2 and self.with_sund:
                        out.write("\\clearpage\n")
                        self.side_weekd = 1
                    for func, path, date in self.days:
                        self.graphicspath(out, path)
                        func(out, path.name, date)
                    if self.with_sund or side_weekd == 2:
                        out.write("\\clearpage\n")
                        self.side_weekd = 1
                    else:
                        self.side_weekd = 2
                    self.outp_done = False
                    self.with_sund = False
                    self.days = []

                self.cur_date += DELTA

            self.write_epilog(out)

    def write_prologue(self, out):
        """Write LaTeX prologue."""
        out.write(
            r"""\documentclass[a4paper,landscape]{book}
\usepackage{graphicx}
\usepackage{textpos}
\usepackage{multicol}
\usepackage[textwidth=277.0mm,textheight=189.9mm,headsep=1mm]{geometry}
\makeatletter
\TPGrid[12mm,12mm]{2}{6}
\setlength{\parindent}{0pt}
\usepackage{fontspec}
%\setmainfont[Ligatures={Common,Rare,Historic}, Numbers=OldStyle]{Linux Libertine O}
\usepackage{libertine}[Ligatures={Common,Rare,Historic}, Numbers=OldStyle]
\begin{document}
\begin{multicols}{2}
"""
        )

    def wr_image(self, date):
        """Write information for including image."""
        path = Path(f"{date:{PATH_FMT}}")
        if (path := path.with_suffix(".png")).is_file():
            weekday = date.isoweekday()
            self.days.append(
                (
                    {
                        1: self.do_mo,
                        2: self.do_di,
                        3: self.do_mi,
                        4: self.do_do,
                        5: self.do_fr,
                        6: self.do_sa,
                        7: self.do_so,
                    }[weekday],
                    path,
                    date,
                )
            )
            self.outp_done = True

    def graphicspath(self, out, path):
        """Write appropriate Graphicspath information."""
        grpath = path.parent
        if grpath != self.grpath:
            out.write(f"\\graphicspath{{{{{grpath}}}}}\n")
            self.grpath = grpath

    def do_mo(self, out, fname, date):
        "Place Monday figure."
        self.place_img(out, self.side_weekd, 1, fname, date)

    def do_di(self, out, fname, date):
        "Place Tuesday figure."
        self.place_img(out, self.side_weekd, 2, fname, date)

    def do_mi(self, out, fname, date):
        "Place Wednesday figure."
        self.place_img(out, self.side_weekd, 3, fname, date)

    def do_do(self, out, fname, date):
        "Place Thursday figure."
        self.place_img(out, self.side_weekd, 4, fname, date)

    def do_fr(self, out, fname, date):
        "Place Friday figure."
        self.place_img(out, self.side_weekd, 5, fname, date)

    def do_sa(self, out, fname, date):
        "Place Saturday figure."
        self.place_img(out, self.side_weekd, 6, fname, date)

    def do_so(self, out, fname, date):
        "Place Sunday figure."
        self.place_img(out, self.side_sund, 1, fname, date)
        self.with_sund = True

    def place_img(self, out, x, y, fname, date):
        "Place image in grid."
        fac = "" if (date.isoweekday() == 7) else 1.0 / 7.0
        out.write(
            f"""\
\\begin{{textblock}}{{1}}({x-1:d},{y-1:d})
  {date:%a %d. %B %Y}\\par
  \\centering%
    \\includegraphics[width=.95\\linewidth,height={fac}\\textheight,%
         keepaspectratio]{{{fname}}}
\\end{{textblock}}
"""
        )

    def write_epilog(self, out):
        "Write LaTeX epilogue."
        out.write(
            r"""\end{multicols}
\end{document}
"""
        )


def main():
    "Main processing"
    book = PeanutsBook(fname=Path("Peanuts_book.tex"))
    book.run()


if __name__ == "__main__":
    main()

# Local Variables:
# mode: python
# compile-command: "cd ../../../ && python setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
