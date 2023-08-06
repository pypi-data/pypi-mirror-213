#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Download comics from gocomic.
"""

from __future__ import annotations, generator_stop

# Standard library imports.
import os
import sys
import stat
import time
import fcntl
import atexit
import pickle
import shutil
import datetime
import subprocess
import configparser
from urllib import request
from pathlib import Path

# Third party library imports.
from selenium import webdriver
from lxml.html import fromstring
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

__date__ = "2023/03/19 19:37:43 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2011-2017 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"

FILE_MODE = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
TOUCH_FMT = "%Y%m%d0300"


class SeleniumSingleton(object):
    __instance = None

    def __init__(self):
        """Virtually private constructor."""
        if SeleniumSingleton.__instance is None:
            driverpath = None
            for path in [
                Path(i)
                for i in (
                    "/usr/bin/",
                    "/usr/lib64/chromium/",
                    "/usr/lib/chromium-browser",
                )
            ]:
                if (driverpath := path / "chromedriver").is_file():
                    break

            # https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug
            options = Options()
            options.add_argument("--headless")
            options.binary_location = "/usr/bin/google-chrome-stable"
            if os.name == "nt":
                options.add_argument(
                    "--disable-gpu"
                )  # Last I checked this was necessary.
            self.driver = webdriver.Chrome(
                executable_path=driverpath, chrome_options=options
            )
            self.driver.get("http://www.gocomics.com/")
            if self.driver.current_url.startswith("https://login.microsoftonline.com/"):
                self.ms_login()
            SeleniumSingleton.__instance = self
        else:
            raise Exception("This class is a singleton!")

    def ms_login(self):
        with (Path.home() / ".config" / "get_comics" / "login.cfg").open() as cfg_file:
            config = configparser.ConfigParser()
            config.read_file(cfg_file)
            section = config["https://login.microsoftonline.com"]
            time.sleep(3)
            action = action_chains.ActionChains(self.driver)
            action.send_keys(section["user"])
            action.send_keys(Keys.ENTER)
            action.perform()
            time.sleep(3)
            action = action_chains.ActionChains(self.driver)
            action.send_keys(section["pw"])
            action.send_keys(Keys.ENTER)
            action.perform()
            time.sleep(3)
            action.send_keys(Keys.ENTER)
            action.perform()

    @staticmethod
    def get_instance():
        """Static access method."""
        if SeleniumSingleton.__instance is None:
            SeleniumSingleton()
        return SeleniumSingleton.__instance

    def __del__(self):
        self.driver.close()


class SaveState(object):
    "Save state information on already downloaded files and dates tried"

    def __init__(self):
        self.loaded = {}
        self.tried = {}
        self.downloaded = [0, 0, 0, 0]


def savestate(state, statfile):
    "Save state dictionary."
    pickle.dump(state, statfile, pickle.HIGHEST_PROTOCOL)
    fcntl.fcntl(statfile, fcntl.LOCK_UN)


def mk_dir_tree(path):
    """Generate directory including missing upper directories."""
    if not path.is_dir():
        mode = (
            stat.S_ISGID
            | stat.S_IRWXU
            | stat.S_IRGRP
            | stat.S_IXGRP
            | stat.S_IROTH
            | stat.S_IXOTH
        )
        path.mkdir(mode=mode, parents=True)
        path.chmod(mode)


class GoComics(object):
    """Download comics from GoComics."""

    start_year = -1
    start_month = -1
    start_day = -1

    skip = {}

    max_num = 100

    gif_path_fmt = ""
    png_path_fmt = ""
    url_fmt = ""

    statefile_name = Path("")

    def __init__(self):
        self.start_date = datetime.date(
            self.start_year, self.start_month, self.start_day
        )

        self.delta = datetime.timedelta(days=1)

    def __call__(self):
        """Main routine."""
        if self.statefile_name.is_file():
            state = pickle.load(self.statefile_name.open("rb"))
            shutil.copy2(self.statefile_name, f"{self.statefile_name}_BAK")
        else:
            state = SaveState()
        statfile = open(self.statefile_name, "wb")
        fcntl.fcntl(statfile, fcntl.LOCK_EX)
        atexit.register(savestate, state, statfile)

        cur_date = datetime.date.today() + self.delta

        count = self.max_num

        cur_year = 0
        cur_month = 0

        devidor = 7
        state.downloaded = [0, 0, 0, 0]

        while (cur_date := cur_date - self.delta) >= self.start_date:
            if cur_date in self.skip:
                continue
            if count <= 0:
                break
            if cur_year != cur_date.year:
                if cur_year != 0:
                    sys.stdout.write("\r" + " " * 40)
                cur_year = cur_date.year
                sys.stdout.write(f"\rprocessing year: {cur_date:%Y}\n")
            if cur_month != cur_date.month:
                cur_month = cur_date.month
                sys.stdout.write("\r" + " " * 40)
                sys.stdout.write(f"\r{cur_date:%m} ")
            sys.stdout.flush()

            png_path = Path(f"{cur_date:{self.png_path_fmt}}")
            pic_id = None
            if not png_path.is_file():
                state.tried[f"{cur_date}"] = (
                    state.tried.get(f"{cur_date}", -1) + 1
                ) % devidor
                if state.tried[f"{cur_date}"] != 0:
                    sys.stdout.write("+")
                    state.downloaded[2] += 1
                    continue

                sys.stdout.flush()

                gif_path = Path(f"{cur_date:{self.gif_path_fmt}}")
                if not gif_path.is_file():
                    url = f"{cur_date:{self.url_fmt}}"
                    data_norm = None
                    SeleniumSingleton.get_instance().driver.get(url)
                    doc = fromstring(
                        SeleniumSingleton.get_instance().driver.page_source
                    )

                    # img = doc.xpath("//img[@class='img-fluid lazyloaded']")
                    img = doc.xpath("//picture[@class='item-comic-image']/img")

                    if len(img) == 0:
                        sys.stdout.write(f"***\nno download {png_path}\nURL: {url:s}\n")
                        state.downloaded[3] += 1
                        continue

                    data = img[0].get("src")

                    pic_id = data.split("/")[-1]

                    if state.loaded.get(pic_id) is not None:
                        sys.stdout.write(".")
                        sys.stdout.flush()
                        sys.stdout.write(
                            f"\r{png_path} is same as of {state.loaded.get(pic_id)}\n"
                        )
                        state.downloaded[3] += 1
                        count -= 1
                        continue

                    mk_dir_tree(png_path.parent)

                    res = request.urlretrieve(data, gif_path)
                    if res[1].get_content_type() == "text/html" and data != data_norm:
                        request.urlretrieve(data_norm, gif_path)

                process = subprocess.Popen(f"convert {gif_path} {png_path}", shell=True)
                os.waitpid(process.pid, 0)

                gif_path.unlink()
                png_path.chmod(FILE_MODE)

                sys.stdout.write(f"\r                    \r{png_path}\n")

                state.loaded[pic_id] = f"{cur_date:%Y %m %d}"

                state.downloaded[0] += 1

                process = subprocess.Popen(
                    f"touch -t {cur_date:{TOUCH_FMT}} {png_path}", shell=True
                )
                os.waitpid(process.pid, 0)
                # count -= 1
            else:
                state.downloaded[1] += 1
                sys.stdout.write("*")

            sys.stdout.flush()

        sys.stdout.write(
            f"\ndownloaded {state.downloaded[0]:d} strips, "
            f"kept {state.downloaded[1]:d}, "
            f"skipped {state.downloaded[2]:d}, "
            f"failed {state.downloaded[3]:d}\n"
        )


# Local Variables:
# mode: python
# compile-command: "cd ../../../ && python setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
