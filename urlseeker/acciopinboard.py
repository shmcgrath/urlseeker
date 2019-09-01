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

PINBOARD_URL = "https://api.pinboard.in/v1"

def get_recent_posts(pinboard_key, count):
    """get_recent_posts docstring"""

    get_recent_url = f"{PINBOARD_URL}/posts/recent"
    recent_params = {
            "auth_token": pinboard_key,
            "format": "json",
            "count": count
    }

    recent_posts_req = requests.get(get_recent_url, params=recent_params)
    recent_posts_res = recent_posts_req.json()
    with open ("pinboard-recent.json", mode='w', encoding='utf-8' ) as jf:
        json.dump(recent_posts_res, jf, ensure_ascii=False, indent=4)

def get_all_posts(pinboard_key):
    """get_all_posts docstring"""

    get_all_url = f"{PINBOARD_URL}/posts/all"
    all_params = {
            "auth_token": pinboard_key,
            "format": "json",
    }

    all_posts_req = requests.get(get_all_url, params=all_params)
    all_posts_res = all_posts_req.json()
    with open ("pinboard-all.json", mode='w', encoding='utf-8' ) as jf:
        json.dump(all_posts_res, jf, ensure_ascii=False, indent=4)
