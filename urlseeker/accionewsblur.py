# -*- coding: UTF-8 -*-

import bookmark
from collections import Mapping
import datetime
import json
import logging
import os
from pathlib import Path
import requests
import sys

NEWSBLUR_URL = "https://www.newsblur.com"

def login(newsblurUser, newsblurPass):
    global newsblurSessionId
    global newsblurCookies
    loginUrl = f"{NEWSBLUR_URL}/api/login"
    loginParams = {"username": newsblurUser, "password": newsblurPass}
    login = requests.post(loginUrl, data=loginParams)
    logging.info("==LOGIN INFORMATION==")
    logging.info(f"Login Status Code: {login.status_code}")
    logging.info(login.json())

    newsblurSessionId = login.cookies["newsblur_sessionid"]
    logging.info(f"newsblurSessionId: {newsblurSessionId}")
    newsblurCookies = dict(newsblur_sessionid=str(newsblurSessionId))
    logging.info(f"newsblurCookies: {newsblurCookies}")

def starred_count():
    starredCount = 0

    readerUrl = f"{NEWSBLUR_URL}/reader/feeds"
    readerParams = {"flat": "true"}

    reader = requests.get(readerUrl, params=readerParams, cookies=newsblurCookies)
    readerRaw = reader.json()

    starredCount = readerRaw["starred_count"]

    return starredCount

def starred_pages():
    starredCount = starred_count()
    starredPages = starredCount // 10
    starredRemainder = starredCount % 10

    if starredRemainder != 0:
        starredPages+=2

    if starredRemainder == 0:
        starredPages+=1

    return starredPages

def get_bookmark_detail(story):
    title = story["story_title"]
    url = story["story_permalink"]
    tags = story["story_tags"]
    tags_user = story["user_tags"]
    folders = story["user_tags"]
    story_timestamp = story["story_timestamp"]
    starred_timestamp = story["starred_timestamp"]
    author = story["story_authors"]
    story_date = story["story_date"]
    story_content = story["story_content"]

    newBookmark = bookmark.Bookmark(title, url);

    for tag in tags:
        newBookmark.add_tag(tag.lower())

    for folder in folders:
        newBookmark.add_tag(folder.lower())

    newBookmark.string_tags()

    return newBookmark

def unstar_story(story_hash):
    """unstar_story docstring"""

    unstar_url = f"{NEWSBLUR_URL}/reader/mark_story_hash_as_unstarred"
    unstar_params = {
        "story_hash": story_hash,
    }
    unstar = requests.post(unstar_url, params=unstar_params,
        cookies=newsblurCookies)

# MAKE IF CHECK LOOKING TO SEE IF THE STORY COUNT IS 0
def get_starred_stories():
    home = str(Path.home())
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
    currentPage = 1
    starredPages = starred_pages()

    storiesUrl = f"{NEWSBLUR_URL}/reader/starred_stories"

    netscapeFile = bookmark.HtmlFile(f"{home}/{today}-bookmarks.html")
    netscapeFile.create_file()

    while currentPage < starredPages:
        storiesParams = {"page": currentPage,}
        stories = requests.get(storiesUrl, params=storiesParams,
            cookies=newsblurCookies)
        storiesRaw = stories.json()
        userStarredStories = storiesRaw["stories"]

        print(f"Gathering starred stories from page {currentPage}...")
        for starredStory in userStarredStories:
            newBookmark = get_bookmark_detail(starredStory)
            netscapeFile.write_bookmark(newBookmark)
            unstar_story(starredStory["story_hash"])

        currentPage+=1

    netscapeFile.write_footer()
