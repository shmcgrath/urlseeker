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

REDDIT_URL = 'https://www.reddit.com'
REDDIT_OAUTH_URL = 'https://oauth.reddit.com'

def login(user, passwd, client_id, client_secret, user_agent):
    global redditAccessToken
    global redditTokenType
    global redditCookies
    loginUrl = REDDIT_URL + '/api/v1/access_token'
    loginAuth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    loginPostData = {
                    'grant_type': 'password',
                    'username': user,
                    'password': passwd,
                    }
    loginHeaders = {
                    'user-agent': user_agent,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                    }


    login = requests.post(loginUrl, auth=loginAuth, data=loginPostData,
                            headers=loginHeaders)
    logging.info('==LOGIN INFORMATION==')
    logging.info('Login Status Code: ' + str(login.status_code))
    redditCookies = login.json()

    redditAccessToken = redditCookies['access_token']
    redditTokenType = redditCookies['token_type']
    logging.info('reddit access token: ' + redditAccessToken)
    logging.info('reddit token type: ' + redditTokenType)

    redditAccessString = redditTokenType + ' ' + redditAccessToken

    return redditAccessString

def get_today_string():
    today = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S')
    return today

def get_bookmark(title, url, subreddit):
    newBookmark = bookmark.Bookmark(title, url)
    newBookmark.add_tag(subreddit)
    newBookmark.add_tag('reddit:' + subreddit)
    newBookmark.string_tags()

    return newBookmark

def unsave_story(user_agent, redditAccessToken, uniqueId):
    unsaveUrl = REDDIT_OAUTH_URL + '/api/unsave/'
    unsaveHeaders = {
                        'Authorization': redditAccessToken,
                        'User-Agent': user_agent,
                    }
    unsaveParams = {
                        'id':uniqueId,
                    }
    unsave = requests.post(unsaveUrl, params=unsaveParams, headers=unsaveHeaders)

def get_saved_stories(username, user_agent, redditAccessToken):
    home = str(Path.home())
    today = get_today_string()
    newFileName = home + '/' + today + '-reddit-' + username + '.html'
    existingFile = os.path.isfile(newFileName)
    if existingFile:
        newFileName = newFileName = '-1'
    else:
        newFileName = newFileName
    netscapeBookmarks = bookmarkfiles.create_html_file(newFileName)

    storiesUrl = REDDIT_OAUTH_URL + '/user/' + username + '/saved/.json'
    storiesHeaders = {
                        'Authorization': redditAccessToken,
                        'User-Agent': user_agent,
                    }
    # TODO: Add a flag or parameter for type (comments v links)
    storiesParams = {
                        't':'all',
                        'type': 'links',
                        'raw_json': '1',
                        'limit':'1000',
                    }
    
    stories = requests.get(storiesUrl, params=storiesParams, headers=storiesHeaders)
    storiesJson = stories.json()
    userSavedStories = storiesJson['data']['children']

    for story in userSavedStories:
        uniqueId = story['kind'] + '_' + story['data']['id']
        title = story['data']['title']
        url = story['data']['url']
        permalink = 'https://www.reddit.com' + story['data']['permalink']
        subreddit = story['data']['subreddit']

        if url == permalink:
            newBookmark = get_bookmark(title, url, subreddit)
            bookmarkfiles.write_html_bookmark(netscapeBookmarks,
                    newBookmark.title, newBookmark.url, newBookmark.tagString)
            unsave_story(user_agent, redditAccessToken, uniqueId)
        elif url != permalink:
            newBookmarkUrl = get_bookmark(title, url, subreddit)
            bookmarkfiles.write_html_bookmark(netscapeBookmarks,
                    newBookmarkUrl.title, newBookmarkUrl.url, newBookmarkUrl.tagString)

            newBookmarkPerma = get_bookmark(title, permalink, subreddit)
            newBookmarkPerma.title = newBookmarkPerma.title + ' - reddit discussion'
            newBookmarkPerma.tagString = newBookmarkPerma.tagString + ',reddit:discussion'
            bookmarkfiles.write_html_bookmark(netscapeBookmarks,
                    newBookmarkPerma.title, newBookmarkPerma.url, newBookmarkPerma.tagString)
            unsave_story(user_agent, redditAccessToken, uniqueId)
        else:
            print('url status unknown')

    bookmarkfiles.write_html_footer(netscapeBookmarks)
