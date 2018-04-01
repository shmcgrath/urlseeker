# -*- coding: UTF-8 -*-

import requests
import json
import logging
import os
import sys
from collections import Mapping

class Bookmark:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)
