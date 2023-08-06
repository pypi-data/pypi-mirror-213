import datetime
import os

import mkdpdf

# FILE SYSTEM
DIRECTORY_PATH_OUTPUT = os.environ.get("DIRECTORY_PATH_OUTPUT", os.getcwd())
DIRECTORY_PATH_PACKAGE = os.path.dirname(mkdpdf.__file__)
FILENAME_FULL = os.environ.get("FILENAME", None)
FILENAME = FILENAME.split(".")[0] if FILENAME_FULL and "." in FILENAME_FULL else None

# LAYOUT
DOCUMENT_EXTRA_VERTICAL_MARGIN = 30
DOCUMENT_SIDE_MARGIN = 2
GITFLAVOR_BREAK_RETURN = "\r\n"
GITFLAVOR_RETURN = "\r\n\r\n"
FORMAT = os.environ.get("FORMAT", "md")
# output render format : input template format
TEMPLATES = {
    "md": "md",
    "pdf": "html"
}

# TIME
DATE_PUBLISH = (datetime.datetime.now().isoformat()).split("T")[0]
