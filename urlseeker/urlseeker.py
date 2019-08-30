#!/usr/bin/python3
# -*- coding: UTF-8 -*-

""" Move bookmarks between local files and various online services."""

import argparse
import bookmark
from collections import Mapping
import datetime
import json
import logging
from logging.config import fileConfig
import os
from pathlib import Path
import requests
import sys
import accionewsblur
import accioreddit

def get_today_string():
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
    return today

def account_information():
    logging.debug("account_information started")
    try:
        import accountinfo
        logging.debug("trying import")
        redditUsername = accountinfo.REDDIT_USERNAME
        redditPassword = accountinfo.REDDIT_PASSWORD
        redditClientId = accountinfo.REDDIT_CLIENT_ID
        redditClientSecret = accountinfo.REDDIT_CLIENT_SECRET
        redditUserAgent = accountinfo.REDDIT_USER_AGENT
        newsblurUsername = accountinfo.NEWSBLUR_USERNAME
        newsblurPassword = accountinfo.NEWSBLUR_PASSWORD
    except ImportError:
        logging.debug("error in import")
        print("error importing account information from accountinfo.py")
        exit(1)

    if (not redditUsername or not redditPassword or not redditClientId or
        not redditClientSecret or not redditUserAgent or not newsblurUsername or
        not newsblurPassword):
        logging.info("hitting the not")
        exit(1)

    return {
        "redditUsername": redditUsername,
        "redditPassword": redditPassword,
        "redditClientId": redditClientId,
        "redditClientSecret": redditClientSecret,
        "redditUserAgent": redditUserAgent,
        "newsblurUsername": newsblurUsername,
        "newsblurPassword": newsblurPassword,
    }

def main():
    fileConfig("logging_config.ini")
    logging.getLogger(__name__).addHandler(logging.NullHandler())
    logger = logging.getLogger()
    logger = logging.getLogger("urlseeker")
    logging.debug("main called")
    user = account_information();
    logging.debug("main finished")

    home = str(Path.home())
    print(home)
    parser = argparse.ArgumentParser(
        description="Move bookmarks between local files and various online \
        services.",
        epilog="urlseeker on GitHub: https://github.com/shmcgrath/urlseeker")
    parser.add_argument("-t", "--type", action="store", type=str,
            choices=["csv", "html", "json", "markdown", "pinboard"],
            help="Set where to store or output  retrieved bookmarks. \
                    The default output is an HTML Netscape bookmark file.\n \
                    The following words  are accetped as arguments for this \
                    flag:\n- 'html': outputs bookmarks to a local HTML file. \
                    \n- 'md': outputs bookmarks to a local markdown file. \
                    \n- 'pinboard': sends retrieved bookmarks to \
                    Pinboard.in.\nIf Pinboard is the destination and a source, \
                    all non-Pinboard bookmarks will go to Pinboard and all \
                    Pinboard bookmarks will be pulled to an HTML bookmark file.")
    parser.add_argument("-o", "--output", action="store", type=str,
            help="Set output file location and name of bookmarks file. \
                    This string should be the complete path and file name \
                    without a filetype / extensiton. \
                    The default file location and name is \
                    '~/YYYY.MM.DD-urlseek-bookmarks.{ext}' where 'ext' is \
                    the filetype of the --type choice (if a file is created. \
                    There is no need to pass in a file extension, as one will \
                    be automatically added. If a file extension/type is \
                    passed in as part of the path, it will be ignored and the \
                    filetype will be added to the end of the string.")
    parser.add_argument("-i", "--input", action="store", type=str,
            help="Set input file location and name. This argument is required \
                    if any of the sources are local files.")
    parser.add_argument("-A", "--all", action="store_true",
            help="Run urlseeker for all services. This does not include local \
                    files. Please note, this is the default behavior.")
    #TODO: if -A is given do all but any ones that are also designated
    parser.add_argument("-C", "--csv", action="store_true",
            help="Run urlseeker for a local csv file.")
    parser.add_argument("-F", "--file", action="store_true",
            help="Run urlseeker for a local bookmark file (Netscape/HTML).")
    parser.add_argument("-H", "--hackernews", action="store_true",
            help="Run urlseeker for Hacker News.")
    parser.add_argument("-J", "--json", action="store_true",
            help="Run urlseeker for a local json file.")
    parser.add_argument("-M", "--markdown", action="store_true",
            help="Run urlseeker for a local markdown file.")
    parser.add_argument("-N", "--newsblur", action="store_true",
            help="Run urlseeker for NewsBlur")
    parser.add_argument("-P", "--pinboard", action="store_true",
            help="Run urlseeker for Pinboard. If this option is selected and \
                    the output type is pinboard, the pinboard bookmarks will \
                    not be re-sent to pinboard. Instead, all pinboard \
                    bookmarks will be pulled to a bookmark HTML file. \
                    Any additional sources will be sent to Pinboard.")
    # TODO: add date range support for pulling down pinboard bookmarks
    parser.add_argument("-R", "--reddit", action="store_true",
            help="Run urlseeker for reddit.")
    parser.add_argument("-T", "--twitter", action="store_true",
            help="Run urlseeker for twitter.")
    args = parser.parse_args()
    logging.debug(args)
    if args.all:
        logging.debug("-A is flagged")
    else:
        if args.newsblur:
            logging.debug("newsblur = true")
            accionewsblur.login(user["newsblurUsername"],
                user["newsblurPassword"])
            accionewsblur.get_starred_stories()
        if args.reddit:
            logging.debug("reddit = true")
            accioreddit.login(user["redditUsername"], user["redditPassword"],
                user["redditClientId"], user["redditClientSecret"],
                user["redditUserAgent"])
            accioreddit.get_saved_stories()

if __name__ == "__main__":
    main()
