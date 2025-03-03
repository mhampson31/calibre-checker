My Calibre library was in pretty rough shape after many years of neglect and a few different manual attempts to clean up the file structure. This script is just a little tool I built to help me get it back into shape.

Currently, the tool looks through your Calibre library and compares it to what's actually on disk. It doesn't fix anything itself -- that's all up to you at the moment.

More features might or might not come. My library's in decent shape now, but I do have some more ideas if I have the time.

usage: ``python3 calibre-checker.py <location> <action>``

``location``: the directory where your books are. Importantly, your metadata.db database file has to live here. For example, "/mnt/storage/ebooks"

``action``: One of several options.
 - ``paths``: books in the Calibre database with file paths that don't exist in the library directory
 - ``files``: specific ebook files in the database that do not exist in their path (though note that missing path errors also count as missing files)
 - ``status``: a count summary of the above errors
