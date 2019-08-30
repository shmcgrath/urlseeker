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

REDDIT_URL = "https://www.reddit.com"
REDDIT_OAUTH_URL = "https://oauth.reddit.com"
global reddit_access_token
global reddit_cookies
global reddit_token_type
global reddit_user
global reddit_user_agent

def login(user_login, passwd, client_id, client_secret, user_agent_login):
    reddit_user = user_login
    reddit_user_agent = user_agent_login
    login_url = f"{REDDIT_URL}/api/v1/access_token"
    login_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    login_post_data = {
                    "grant_type": "password",
                    "username": reddit_user,
                    "password": passwd,
                    }
    login_headers = {
                    "user-agent": reddit_user_agent,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"
                    }

    login = requests.post(login_url, auth=login_auth, data=login_post_data,
                            headers=login_headers)

    logging.info(f"Login Status Code: {login.status_code}")
    reddit_cookies = login.json()
    reddit_access_token = reddit_cookies["access_token"]
    logging.info(f"reddit_access_token: {reddit_access_token}")
    reddit_token_type = reddit_cookies["token_type"]
    logging.info(f"reddit_token_type: {reddit_token_type}")

    access_string = f"{reddit_token_type} {reddit_access_token}"

def get_today_string():
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
    return today

def get_bookmark(title, url, subreddit):
    new_bookmark = bookmark.Bookmark(title, url)
    new_bookmark.add_tag(f"reddit:{subreddit}")
    new_bookmark.string_tags()

    return new_bookmark

def unsave_story(story_unique_id):
    unsaveUrl = f"{REDDIT_OAUTH_URL}/api/unsave/"
    unsaveHeaders = {
                        "Authorization": reddit_access_token,
                        "User-Agent": reddit_user_agent,
                    }
    unsaveParams = {
                        "id":story_unique_id,
                    }
    unsave = requests.post(unsaveUrl, params=unsaveParams,
            headers=unsaveHeaders)

def get_saved_stories():
    home = str(Path.home())
    today = get_today_string()
    netscape_file = bookmark.HtmlFile(f"{home}/{today}-reddit-{reddit_user}.html")
    netscape_file.create_file()

    stories_url = f"{REDDIT_OAUTH_URL}/user/{reddit_user}/saved/.json"
    stories_headers = {
                        "Authorization": reddit_access_token,
                        "User-Agent": reddit_user_agent,
                    }
    # TODO: Add a flag or parameter for type (comments v links)
    stories_params = {
                        "t":"all",
                        "type": "links",
                        "raw_json": "1",
                        "limit":"1000",
                    }
    stories = requests.get(stories_url, params=stories_params,
        headers=stories_headers)

    stories_json = stories.json()
    usr_saved_stories = stories_json["data"]["children"]

    for story in usr_saved_stories:
        story_unique_id = f"{story['kind']}_{story['data']['id']}"
        title = story["data"]["title"]
        url = story["data"]["url"]
        permalink = f"https://www.reddit.com{story['data']['permalink']}"
        subreddit = story["data"]["subreddit"]

        if url == permalink:
            new_bookmark = get_bookmark(title, url, subreddit)
            netscape_file.write_bookmark(new_bookmark)

            unsave_story(story_unique_id)

        elif url != permalink:
            new_bookmark_url = get_bookmark(title, url, subreddit)
            netscape_file.write_bookmark(new_bookmark_url)

            new_bookmark_perma = get_bookmark(title, permalink, subreddit)
            new_bookmark_perma.title = (
                f"{new_bookmark_perma.title} - reddit discussion"
            )
            new_bookmark_perma.tagString = (
                f"{new_bookmark_perma.tagString},reddit:discussion"
            )
            netscape_file.write_bookmark(new_bookmark_perma)

            unsave_story(story_unique_id)

        else:
            print("url status unknown")

    netscape_file.write_footer()
