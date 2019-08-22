# -*- coding: UTF-8 -*-

class Bookmark:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.tags = []
        self.tagString = ''

    def add_tag(self, tag):
        tag = tag.lower()
        tag = ''.join(tag.split())
        self.tags.append(tag)

    def string_tags(self):
        self.tagString = ','.join(map(str, self.tags))

