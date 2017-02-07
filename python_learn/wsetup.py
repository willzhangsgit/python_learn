from distutils.core import setup
import py2exe
includes = ["encodings", "encoings.*"]
options = {
"py2exe": {"bundle_files": 2 }
}
setup(
options = options,
zipfile = None,
windows = ['firstwindow.py']
)