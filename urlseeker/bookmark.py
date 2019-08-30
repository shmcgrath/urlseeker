# -*- coding: UTF-8 -*-

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
        self.tagString = ','.join(map(str, self.tags))

class HtmlFile:
    """HtmlFile docstring"""
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileObject = open(self.filePath, 'w')

    def create_file(self):
        """create_file creates the HTML bookmark file at the path of the
        HtmlFile object."""

        currentDTS = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S')
        print('Creating Netscape HTML Bookmarks file at ' + self.filePath)
        self.fileObject.write(f"<!DOCTYPE NETSCAPE-Bookmark-file-1> \
            \n\t<!--This is an automatically generated file. \
            \n\tIt will be read and overwritten. \
            \n\tDo Not Edit! --> \
            \n\t<Title> {currentDTS} Bookmarks</Title> \
            \n\t<H1> {currentDTS} Bookmarks</H1> \
            \n\t<DL>")

    def write_footer(self):
        """write_footer docstring"""
        self.fileObject.write('\n\t</DL>')
        self.fileObject.close()

    def write_bookmark(self, bookmark):
        """write_bookmark docstring"""
        title = bookmark.title
        url = bookmark.url
        tags = bookmark.tagString
        htmlLine = f'\n\t<DT><A HREF="{url}" TAGS="{tags}">{title}</A>'
        self.fileObject.write(htmlLine)

class MarkdownFile:
    """MarkdownFile docstring"""
    def __init__(self, filePath, bookmarkSource):
        self.filePath = filePath
        self.bookmarkSource = bookmarkSource
        self.fileObject = open(self.filePath, 'w')

    def create_file(self):
        """create_file creates the markdown bookmark file at the path of the
        MarkdownFile object."""

        currentDTS = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        print('Creating Markdown Bookmarks file at ' + mdFile)
        self.fileObject.write(f"# {currentDTS} {self.bookmarkSource} Bookmarks\n \
                ## Bookmarks\n")


    def write_footer(self):
        """write_footer docstring"""
        currentDTS = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        self.fileObject.write(f"\n## Bookmark File Information \
            \n- Created On: {currentDTS} \
            \n- Source: {self.bookmarkSource} \
            \n- Created by: \
            [urlseeker](https://github.com/shmcgrath/urlseeker)")
        self.fileObject.close()

    def write_bookmark(self, bookmark):
        """write_bookmark docstring"""
        title = bookmark.title
        url = bookmark.url
        tags = bookmark.tagString
        markdownLine = f"\n- [{title}]({url})\ttags: {tags}"
        self.fileObject.write(markdownLine)

def main():
    print("This file only contains class definitions and should not be \
            run directly.")

if __name__ == "__main__":
    main()
