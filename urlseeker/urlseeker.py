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
import accioicloudtabs
import acciopinboard
import accioreddit
import acciotwitter

def get_account_information():
    try:
        import accountinfo
        logging.debug(f"Importing from accountinfo.py...")
        reddit_user = accountinfo.REDDIT_USERNAME
        reddit_passwd = accountinfo.REDDIT_PASSWORD
        reddit_client_id = accountinfo.REDDIT_CLIENT_ID
        reddit_client_secret = accountinfo.REDDIT_CLIENT_SECRET
        reddit_user_agent = accountinfo.REDDIT_USER_AGENT
        newsblur_user = accountinfo.NEWSBLUR_USERNAME
        newsblur_passwd = accountinfo.NEWSBLUR_PASSWORD
        pinboard_key = accountinfo.PINBOARD_KEY
        pinboard_user = accountinfo.PINBOARD_USERNAME
        pinboard_passwd = accountinfo.PINBOARD_PASSWORD
        twitter_app_id = accountinfo.TWITTER_APP_ID
        twitter_api_key = accountinfo.TWITTER_API_KEY
        twitter_api_secret_key = accountinfo.TWITTER_API_SECRET_KEY
        twitter_access_token = accountinfo.TWITTER_ACCESS_TOKEN
        twitter_access_token_secret = accountinfo.TWITTER_ACCESS_TOKEN_SECRET
        twitter_user = accountinfo.TWITTER_USERNAME
        twitter_passwd = accountinfo.TWITTER_PASSWORD
    except ImportError:
        logging.debug(f"ImportError importing from accountinfo.py. Exiting...")
        print(f"ImportError importing from accountinfo.py. Exiting...")
        exit(1)

    if (not reddit_user or not reddit_passwd or not reddit_client_id
            or not reddit_client_secret or not reddit_user_agent
            or not newsblur_user or not newsblur_passwd
            or not pinboard_key or not pinboard_user or not pinboard_passwd
            or not twitter_app_id or not twitter_api_key
            or not twitter_api_secret_key or not twitter_access_token
            or not twitter_access_token_secret
            or not twitter_user or not twitter_passwd
        ):
        logging.info(f"Missing information to generate user. Exiting...")
        exit(1)

    return {
        "reddit_user": reddit_user,
        "reddit_passwd": reddit_passwd,
        "reddit_client_id": reddit_client_id,
        "reddit_client_secret": reddit_client_secret,
        "reddit_user_agent": reddit_user_agent,
        "newsblur_user": newsblur_user,
        "newsblur_passwd": newsblur_passwd,
        "pinboard_key": pinboard_key,
        "pinboard_user": pinboard_user,
        "pinboard_passwd": pinboard_passwd,
        "twitter_app_id": twitter_app_id,
        "twitter_api_key": twitter_api_key,
        "twitter_api_secret_key": twitter_api_secret_key,
        "twitter_access_token": twitter_access_token,
        "twitter_access_token_secret": twitter_access_token_secret,
        "twitter_user": twitter_user,
        "twitter_passwd": twitter_passwd,
    }

def main():
    fileConfig("logging_config.ini")
    logging.getLogger(__name__).addHandler(logging.NullHandler())
    logger = logging.getLogger()
    logger = logging.getLogger("urlseeker")

    user = get_account_information();

    parser = argparse.ArgumentParser(
        description="A bookmark wizard written in Python.",
        epilog="urlseeker on GitHub: https://github.com/shmcgrath/urlseeker"
    )

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
    parser.add_argument("-I", "--icloudtabs", action="store_true",
        help="Run urlseeker for iCloud Tabs. Note, this currently only \
                works on macOS.")
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
    parser.add_argument("-Y", "--youtube", action="store_true",
        help="Run urlseeker for YouTube.")
    # TODO: youtube support https://developers.google.com/youtube/v3/docs/

    args = parser.parse_args()
    logging.debug(f"args: {args}")

    if args.all:
        logging.debug("-A is flagged")
    else:
        if args.icloudtabs:
            logging.debug("icloudtabs = true")
            accioicloudtabs.get_icloud_tabs()
        if args.newsblur:
            logging.debug("newsblur = true")
            accionewsblur.login(user["newsblur_user"],
                user["newsblur_passwd"])
            accionewsblur.get_starred_stories()
        if args.reddit:
            logging.debug("reddit = true")
            accioreddit.login(user["reddit_user"], user["reddit_passwd"],
                user["reddit_client_id"], user["reddit_client_secret"],
                user["reddit_user_agent"])
        if args.twitter:
            logging.debug("twitter = true")
            acciotwitter.login(user)
        if args.pinboard:
            logging.debug("pinboard = true")
            acciopinboard.get_recent_posts(user["pinboard_key"], 100)
            acciopinboard.get_all_posts(user["pinboard_key"])

if __name__ == "__main__":
    main()
