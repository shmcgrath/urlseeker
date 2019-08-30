# -*- coding: UTF-8 -*-

import requests
import json
import logging
import os
import sys
import bookmark
from collections import Mapping
from pathlib import Path

newsblurUrl = 'https://www.newsblur.com'

def login(newsblurUser, newsblurPass):
    global newsblurSessionId
    global newsblurCookies
    loginUrl = newsblurUrl + '/api/login'
    loginParams = {'username': newsblurUser, 'password': newsblurPass}

    login = requests.post(loginUrl, data=loginParams)
    logging.info('==LOGIN INFORMATION==')
    logging.info('Login Status Code: ' + str(login.status_code))
    logging.info(login.json())

    newsblurSessionId = login.cookies['newsblur_sessionid']
    logging.info('newsblur session id: ' + newsblurSessionId)
    newsblurCookies = dict(newsblur_sessionid=str(newsblurSessionId))
    logging.info('newsblurCookies:')
    logging.info(newsblurCookies)

    return newsblurSessionId

def starred_count():
    starredCount = 0

    readerUrl = newsblurUrl + '/reader/feeds'
    readerParams = {'flat': 'true'}

    reader = requests.get(readerUrl, params=readerParams, cookies=newsblurCookies)
    readerRaw = reader.json()

    starredCount = readerRaw['starred_count']

    return starredCount

def starred_pages():
    starredCount = starred_count()
    starredPages = starredCount // 10
    starredRemainder = starredCount % 10

    if starredRemainder !=0:
        starredPages+=2

    if starredRemainder ==0:
        starredPages+=1

    return starredPages

def get_bookmark_detail(starredStory):
    title = starredStory['story_title']
    url = starredStory['story_permalink']
    tags = starredStory['story_tags']
    folders = starredStory['user_tags']

    newBookmark = bookmark.Bookmark(title, url);

    for tag in tags:
        newBookmark.add_tag(tag.lower())

    for folder in folders:
        newBookmark.add_tag(folder.lower())

    newBookmark.string_tags()

    return newBookmark

# MAKE IF CHECK LOOKING TO SEE IF THE STORY COUNT IS 0
def get_starred_stories():
    home = str(Path.home())
    logging.debug('hit get_starred_stories')
    currentPage = 1
    starredPages = starred_pages()

    storiesUrl = newsblurUrl + '/reader/starred_stories'

    netscapeBookmarks = bookmark.create_html_file(home, 'newsblur')

    while currentPage < starredPages:
        storiesParams = {'page': currentPage,}
        stories = requests.get(storiesUrl, params=storiesParams,
                cookies=newsblurCookies)
        storiesRaw = stories.json()
        userStarredStories = storiesRaw['stories']

        print('Gathering starred stories from page ' + str(currentPage) + '.')
        for starredStory in userStarredStories:
            newBookmark = get_bookmark_detail(starredStory)
            bookmark.write_html_bookmark(netscapeBookmarks,
                    newBookmark.title, newBookmark.url, newBookmark.tagString)

            currentPage+=1

    bookmark.write_html_footer(netscapeBookmarks)
