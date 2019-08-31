# -*- coding: UTF-8 -*-

import bookmark
from collections.abc import Mapping
import datetime
import logging
import os
from pathlib import Path
import sqlite3
from sqlite3 import Error
import sys

def get_icloud_tabs():
    """ get_icloud_tabs docstring """

    CLOUD_TABS_LOCATION = f"{HOME}/Library/Safari/CloudTabs.db"
    HOME = str(Path.HOME())
    current_dts = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M")

    netscapeFile = bookmark.htmlFile(f"{HOME}/{current_dts}-iCloudTabs.html")

    try:
        conn = sqlite3.connect(CLOUD_TABS_LOCATION)
    except Error as e:
        print(f"There has been an error: {e}")

    with conn:
        cloudTabsSql="SELECT ct.title title, ct.url url FROM cloud_tabs AS ct"
        c = conn.cursor()

        for row in c.execute(cloudTabsSql):
            row_bookmark = bookmark.Bookmark(f"{row[0]}", f"{row[1]}")
            netscapeFile.write_bookmark(row_bookmark)

    netscapeFile.write_footer()

def main():
    get_icloud_tabs()

if __name__ == '__main__':
    main()
