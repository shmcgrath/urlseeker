# -*- coding: UTF-8 -*-

import datetime

class Bookmark:
    """ Bookmark class containing the title, url, and tags of a bookmark."""

    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.tags = []
        self.tagString = ""
        self.description = ""

    def add_tag(self, tag):
        tag = tag.lower()
        tag = ''.join(tag.split())
        self.tags.append(tag)

    def string_tags(self):
        self.tagString = ",".join(map(str, self.tags))

class HtmlFile:
    """HtmlFile docstring"""

    def __init__(self, file_path, current_dts=None):
        self.file_path = file_path
        if current_dts is None:
            current_dts = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        self.current_dts = current_dts
        self.file_object = open(self.file_path, "w")

    def create_file(self):
        """create_file creates the HTML bookmark file at the path of the
        HtmlFile object."""

        netscape_header = (
            f"<!DOCTYPE NETSCAPE-Bookmark-file-1>"
            f"\n\t<!--This is an automatically generated file."
            f"\n\tIt will be read and overwritten."
            f"\n\tDo Not Edit! -->"
            f'<META HTTP-EQUIV="Content-Type" CONTENT="text/html; '
            f'charset=UTF-8">'
            f"\n\t<TITLE> {self.current_dts} Bookmarks</Title>"
            f"\n\t<H1> {self.current_dts} Bookmarks</H1>"
            f"\n\t<DL>"
        )

        print(f"Creating Netscape HTML Bookmarks file at {self.file_path}...")
        self.file_object.write(netscape_header)

    def write_footer(self):
        """write_footer docstring"""

        netscape_footer = (
            f"\n\t</DL>"
        )

        self.file_object.write(netscape_footer)
        self.file_object.close()

    def write_bookmark(self, bookmark):
        """write_bookmark docstring"""

        netscape_line = (
            f'\n\t<DT><A HREF="{bookmark.url}" TAGS="{bookmark.tagString}">'
            f'{bookmark.title}</A>'
        )

        self.file_object.write(netscape_line)

    def write_description(self, description):
        """write_description docstring"""

        description_line = (f'\n\t<DD>{description}')
        self.file_object.write(description_line)


class MarkdownFile:
    """MarkdownFile docstring"""
    def __init__(self, file_path, bookmark_source, current_dts=None):
        self.file_path = file_path
        self.bookmark_source = bookmark_source
        if current_dts is None:
            current_dts = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        self.current_dts = current_dts
        self.file_object = open(self.file_path, "w")

    def create_file(self):
        """create_file creates the markdown bookmark file at the path of the
        MarkdownFile object."""

        markdown_header = (
            f"# {self.current_dts} {self.bookmark_source} Bookmarks"
            f"\n## Bookmarks\n"
        )

        print("Creating Markdown Bookmarks file at {self.file_path}.")
        self.file_object.write(markdown_header)

    def write_footer(self):
        """write_footer docstring"""

        markdown_footer=(
            f"\n## Bookmark File Information"
            f"\n- Created On: {self.current_dts}"
            f"\n- Source: {self.bookmark_source}"
            f"\n- Created by: [urlseeker](https://github.com/shmcgrath/urlseeker)"
        )

        self.file_object.write(markdown_footer)
        self.file_object.close()

    def write_bookmark(self, bookmark):
        """write_bookmark docstring"""

        markdown_line = (
            f"\n- [{bookmark.title}]({bookmark.url})"
            f"\ttags: {bookmark.tagString}"
        )

        self.file_object.write(markdown_line)

def main():
    print(
        f"This file contains class definitions and should not be run directly."
    )

if __name__ == "__main__":
    main()
