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

def login():
    current_dts = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
