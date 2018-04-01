# -*- coding: UTF-8 -*-

import requests
import json
import logging
import os
import sys
import bookmark
import bookmarkfiles
from collections import Mapping
from pathlib import Path

redditUrl = 'https://www.reddit.com'
redditOauthUrl = 'https://oauth.reddit.com'

def login(redditUser, redditPass, redditClientId, redditClientSecret, redditUserAgent):
    global redditAccessToken
    global redditTokenType
    global redditCookies
    loginUrl = redditUrl + '/api/v1/access_token'
    loginAuth = requests.auth.HTTPBasicAuth(redditClientId, redditClientSecret)
    loginPostData = {
                    'grant_type': 'password',
                    'username': redditUser,
                    'password': redditPass,
                    }
    loginHeaders = {
                    'user-agent': redditUserAgent,
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

def get_saved_stories(redditUsername, redditUserAgent, redditAccessToken):
    storiesUrl = redditOauthUrl + '/user/' + redditUsername + '/saved/.json'
    storiesHeaders = {
                        'Authorization': redditAccessToken,
                        'User-Agent': redditUserAgent,
                    }
    storiesParams = {
                        't':'all',
                        'type': 'links',
                        'raw_json': '1',
                    }
    
    stories = requests.get(storiesUrl, params=storiesParams, headers=storiesHeaders)
    storiesJson = stories.json()
    #logging.debug(storiesJson)
    userSavedStories = storiesJson['data']['children']
    #logging.info(userSavedStories)

    for story in userSavedStories:
        logging.info(story['kind'])
        """
        logging.info(story['data']['title'])
        logging.info(story['data']['url'])
        logging.info(story['data']['permalink'])
        logging.info(story['data']['subreddit'])
        """
