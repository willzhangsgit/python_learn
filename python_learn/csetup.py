from distutils.core import setup
import py2exe
includes = ["encodings", "encoings.*"]
options = {
"py2exe": {"bundle_files": 1 }
}
setup(
options = options,
zipfile = None,
console = ['meizei_gif1.py']
)