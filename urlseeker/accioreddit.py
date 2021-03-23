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
global reddit_access_string
global reddit_access_token
global reddit_cookies
global reddit_token_type
global reddit_user
global reddit_user_agent

def login(user_login, passwd, client_id, client_secret, user_agent_login):
    global reddit_access_string
    global reddit_access_token
    global reddit_cookies
    global reddit_token_type
    global reddit_user
    global reddit_user_agent

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

    reddit_access_string = f"{reddit_token_type} {reddit_access_token}"

    get_saved_stories()
    #get_saved_comments()

def get_today_string():
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
    return today

def get_bookmark(title, url, subreddit):
    new_bookmark = bookmark.Bookmark(title, url)
    new_bookmark.add_tag(f"reddit:{subreddit}")
    new_bookmark.string_tags()

    return new_bookmark

def unsave_story(story_unique_id):
    global reddit_access_string
    global reddit_user_agent
    usave_url = f"{REDDIT_OAUTH_URL}/api/unsave/"
    usave_headers = {
                        "Authorization": reddit_access_string,
                        "User-Agent": reddit_user_agent,
                    }
    usave_params = {
                        "id":story_unique_id,
                    }
    unsave = requests.post(usave_url, params=usave_params,
            headers=usave_headers)

def get_saved_stories():
    global reddit_access_string
    global reddit_user
    global reddit_user_agent

    home = str(Path.home())
    today = get_today_string()

    netscape_file = bookmark.HtmlFile(f"{home}/{today}-reddit-stories-{reddit_user}.html")
    netscape_file.create_file()

    stories_url = f"{REDDIT_OAUTH_URL}/user/{reddit_user}/saved"
    stories_headers = {
                        "Authorization": reddit_access_string,
                        "User-Agent": reddit_user_agent,
                    }
    # TODO: Add a flag or parameter for type (comments v links)
    stories_params = {
                        "t":"all",
                        "type": "links",
                        "limit":"100",
                        "raw_json": "1",
                    }
    stories = requests.get(stories_url, params=stories_params,
        headers=stories_headers)

    stories_json = stories.json()
    usr_saved_stories = stories_json["data"]["children"]

    for story in usr_saved_stories:
        logging.debug(f"=== SAVED STORY ===")
        logging.debug(story)
        story_unique_id = f"{story['kind']}_{story['data']['id']}"
        title = story["data"]["title"]
        url = story["data"]["url"]
        permalink = f"https://www.reddit.com{story['data']['permalink']}"
        subreddit = story["data"]["subreddit"]
        category = story["data"]["category"]
        domain = story["data"]["domain"]
        selftext_html = story["data"]["selftext_html"]
        selftext = story["data"]["selftext"]
        author_flair_text = story["data"]["author_flair_text"]
        created_utc = story["data"]["created_utc"]
        created = story["data"]["created"]
        author = story["data"]["author"]
        logging.debug(author)

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

def get_saved_comments():
    global reddit_access_string
    global reddit_user
    global reddit_user_agent

    home = str(Path.home())
    today = get_today_string()

    netscape_file = bookmark.HtmlFile(f"{home}/{today}-reddit-comments-{reddit_user}.html")
    netscape_file.create_file()

    comments_url = f"{REDDIT_OAUTH_URL}/user/{reddit_user}/saved"
    comments_headers = {
                        "Authorization": reddit_access_string,
                        "User-Agent": reddit_user_agent,
                    }
    # TODO: Add a flag or parameter for type (comments v links)
    comments_params = {
                        "t":"all",
                        "type": "comments",
                        "limit":"100",
                        "raw_json": "1",
                    }
    comments = requests.get(comments_url, params=comments_params,
        headers=comments_headers)

    comments_json = comments.json()
    usr_saved_comments = comments_json["data"]["children"]

    for comment in usr_saved_comments:
        comment_unique_id = f"{comment['kind']}_{comment['data']['id']}"
        logging.debug("=== SAVED COMMENT ===")
        logging.debug(comment)
        logging.debug(comment_unique_id)
        title = comment["data"]["link_title"]
        logging.debug(title)
        url = comment["data"]["link_url"]
        logging.debug(f"url: {url}")
        permalink = comment["data"]["link_permalink"]
        logging.debug(f"permalink: {permalink}")
        permalink_comment = f"https://www.reddit.com{comment['data']['permalink']}"
        logging.debug(f"permalink_comment: {permalink_comment}")
        author = comment["data"]["author"]
        logging.debug(author)
        author_flair = comment["data"]["author_flair_text"]
        logging.debug(author_flair)
        subreddit = comment["data"]["subreddit"]
        logging.debug(subreddit)
        body_html = comment["data"]["body_html"]
        logging.debug(body_html)
        created_utc = comment["data"]["created_utc"]
        logging.debug(created_utc)
        created = comment["data"]["created"]

        if str(author_flair).lower() == "none":
            author_flair = ''
        else:
            author_flair = f'[{author_flair}]'
        if url == permalink:
            new_bookmark = get_bookmark(title, url, subreddit)
            netscape_file.write_bookmark(new_bookmark)

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

        else:
            print("url status unknown")

        new_bookmark_comment = get_bookmark(title, permalink_comment, subreddit)
        new_bookmark_comment.title = (
            f"{new_bookmark_comment.title} - saved comment"
        )
        netscape_file.write_bookmark(new_bookmark_comment)
        comment_line = (
                f'<p><b>saved comment:</b> {body_html}</p>'
                f'<p><b>subreddit:</b> {subreddit}'
                f'\n<b>author[flair]</b>: {author}{author_flair}</p>'
        )
        netscape_file.write_description(comment_line)
        unsave_story(comment_unique_id)

    netscape_file.write_footer()
