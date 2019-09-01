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

TWITTER_URL = ""
TWITTER_OAUTH_URL = ""
#"twitter_app_id": twitter_app_id,
#"twitter_api_key": twitter_api_key,
#"twitter_api_secret_key": twitter_api_secret_key,
#"twitter_access_token": twitter_access_token,
#"twitter_access_token_secret": twitter_access_token_secret,
#"twitter_user": twitter_user,
#"twitter_passwd": twitter_passwd,

def login(user):
    current_dts = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
