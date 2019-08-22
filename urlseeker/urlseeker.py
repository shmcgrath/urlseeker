# -*- coding: UTF-8 -*-

import requests
import json
import os
import sys
import bookmarkfiles
import accionewsblur
import accioreddit
from collections import Mapping
import logging
from logging.config import fileConfig


def account_information():
    logging.debug('account_information started')
    try:
        import accountinfo
        logging.debug('trying import')
        redditUsername = accountinfo.REDDIT_USERNAME
        redditPassword = accountinfo.REDDIT_PASSWORD
        redditClientId = accountinfo.REDDIT_CLIENT_ID
        redditClientSecret = accountinfo.REDDIT_CLIENT_SECRET
        redditUserAgent = accountinfo.REDDIT_USER_AGENT
        newsblurUsername = accountinfo.NEWSBLUR_USERNAME
        newsblurPassword = accountinfo.NEWSBLUR_PASSWORD
    except ImportError:
        logging.debug('error in import')
        print('error importing account information from accountinfo.py')
        exit(1)

    if not redditUsername or not redditPassword or not redditClientId or not redditClientSecret or not redditUserAgent or not newsblurUsername or not newsblurPassword:
        logging.info('hitting the not')
        exit(1)

    return {
        'redditUsername': redditUsername,
        'redditPassword': redditPassword,
        'redditClientId': redditClientId,
        'redditClientSecret': redditClientSecret,
        'redditUserAgent': redditUserAgent,
        'newsblurUsername': newsblurUsername,
        'newsblurPassword': newsblurPassword,
    }

def main():
    fileConfig('logging_config.ini')
    logging.getLogger(__name__).addHandler(logging.NullHandler())
    logger = logging.getLogger()
    logger = logging.getLogger('urlseeker')
    logging.debug('main called')
    user = account_information();
    logging.debug('main finished')
    #TODO: gather args about what services i should be pulling down when i run
    # the script (all, reddit, newsblur, twitter, pinboard, hacker news)
    #TODO: add a flag for various output types (bookmark, to pinboard, csv, markdown)
    #accionewsblur.login(user['newsblurUsername'], user['newsblurPassword'])
    #accionewsblur.get_starred_stories()
    redditAccessToken = accioreddit.login(user['redditUsername'], user['redditPassword'], user['redditClientId'], user['redditClientSecret'], user['redditUserAgent'])
    accioreddit.get_saved_stories(user['redditUsername'], user['redditUserAgent'], redditAccessToken)

if __name__ == '__main__':
    main()
