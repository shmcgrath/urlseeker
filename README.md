# urlseeker
Move bookmarks between local files and various online services.

# PyCloudTabs
Python script that reads the iCloud tab database on macOS and pulls open tabs into an HTML Bookmark file. The output HTML file (YYYY-DD-MM-HH.MM-iCloudTabs.html) is saved to the user's home directory. PyCloudTabs only works on macOS.

## Netscape Bookmark File Format
The documentation on the Netscape Bookmark File Format can be found [here](https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa753582(v=vs.85)).

Fields founds on exported Firefox bookmarks:
- ADD_DATE (numeric timestamp)
- LAST_MODIFIED (numeric timestamp)
- SHORTCUTURL (string)
- TAGS (comma separated words, no spaces after commas)
- <DT> tags with H3 are folders
