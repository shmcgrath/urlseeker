# -*- coding: UTF-8 -*-

import os
import datetime
import logging
import sys
from collections import Mapping
from pathlib import Path

def get_today_string():
    today = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M')
    return today

def create_html_file(filePath, fileName):
    today = get_today_string()
    htmlFile = filePath + '/' + today + '-' + fileName + '.html'
    print('Creating Netscape HTML Bookmarks file at ' + htmlFile)
    htmlBookmarks = open(htmlFile, 'w')
    htmlBookmarks.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n')
    htmlBookmarks.write('    <!--This is an automatically generated file.\n')
    htmlBookmarks.write('    It will be read and overwritten.\n')
    htmlBookmarks.write('    Do Not Edit! -->\n')
    htmlBookmarks.write('    <Title>'+ today + ' Bookmarks</Title>\n')
    htmlBookmarks.write('    <H1>Bookmarks</H1>\n')
    htmlBookmarks.write('    <DL>')

    return htmlBookmarks

def write_html_bookmark(htmlBookmarks, title, url):
        bookmark = '\n      <DT><A HREF="' + url + '">' + title + '</A>'
        htmlBookmarks.write(bookmark)

def write_html_footer(htmlBookmarks):
    htmlBookmarks.write('\n    </DL>')
    htmlBookmarks.close()

def create_markdown_file(filePath, fileName):
    today = get_today_string()
    source = 'source'
    mdFile = filePath + fileName + '.md'
    print('Creating Markdown Bookmarks file at ' + mdFile)
    mdBookmarks = open(mdFile, 'w')
    mdBookmarks.write('# ' + today + ' ' + source + ' Bookmarks\n')

    return mdBookmarks

def write_markdown_bookmark(htmlBookmarks, title, url, tags):
    bookmark = '\n[' + title + '](' + url + ') ' + tags
    mdBookmarks.write(bookmark)

def write_markdown_footer(mdBookmarks):
    today = get_today_string()
    mdBookmarks.write('\n## Bookmark File Information')
    mdBookmarks.write('\n- Created On: ' + today)
    mdBookmarks.write('\n- Source: ')
    mdBookmarks.write('\n- Created by: [urlseeker](https://github.com/shmcgrath/urlseeker)')
    mdBookmarks.close()

def main():
    print('hello!')


if __name__ == '__main__':
    main()
