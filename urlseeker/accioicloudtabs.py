# -*- coding: UTF-8 -*-

import os
import datetime
import sqlite3
from sqlite3 import Error
import logging
import sys
from collections.abc import Mapping
from pathlib import Path
import bookmarkfiles

def get_today_string():
    today = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
    return today

def gather_cloud_tabs(conn, cloudTabsBookmarks):
    cloudTabsSql = 'SELECT cloud_tabs.title title, cloud_tabs.url url FROM cloud_tabs'
    c = conn.cursor()
    for row in c.execute(cloudTabsSql):
        bookmarkfiles.write_html_bookmark(cloudTabsBookmarks, str(row[0]),
                str(row[1]), "")

def create_connection(db_file):
    # create a database connection to the SQLite database
    # specified by the db_file
    # :param db_file: database file
    # :return: connection object or None
    # http://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def main():
    home = str(Path.home())
    cloudTabsLocation = home + "/Library/Safari/CloudTabs.db"
    today = bookmarkfiles.get_today_string()
    htmlFileName = home + f"/{today}-iCloudTabs.html"
    cloudTabsBookmarks = bookmarkfiles.create_html_file(htmlFileName)

    conn = create_connection(cloudTabsLocation)
    with conn:
        gather_cloud_tabs(conn, cloudTabsBookmarks)

    bookmarkfiles.write_html_footer(cloudTabsBookmarks)

if __name__ == '__main__':
    main()
