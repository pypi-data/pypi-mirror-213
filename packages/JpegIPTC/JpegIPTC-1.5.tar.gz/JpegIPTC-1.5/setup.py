"""SETUP THIS STUFF."""
import sys
from distutils.command.sdist import sdist as _sdist
from os import path

from setuptools import setup
classifiers = """
Development Status :: 3 - Alpha
License :: OSI Approved :: Artistic License
License :: OSI Approved :: GNU General Public License (GPL)
Intended Audience :: Developers
Programming Language :: Python
Topic :: Multimedia :: Graphics
Topic :: Utilities
"""

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

if sys.version_info < (2, 3):
    _setup = setup

    def setup(**kwargs):
        if "classifiers" in kwargs:
            del kwargs["classifiers"]
            _setup(**kwargs)


class sdist(_sdist, object):
    def run(self):
        import os
        res = _sdist.run(self)
        print((self.get_archive_files()))
        for fn in self.get_archive_files():
            os.system('scp -p %s gtmainbox:/var/www/html/python/' % fn)
        return res


def openfile(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname))


version = next((row.split('=', 1)[-1].strip().strip("'").strip('"')
                for row in open('JpegIPTC.py', 'r')
                if row.startswith('__version__')))
setup(  # cmdclass={'sdist': sdist},
    name='JpegIPTC',
    version=version,
    url='https://github.com/gdegoulet/JpegIPTC',
    download_url='https://github.com/gdegoulet/JpegIPTC',
    author='Guillaume Degoulet',
    author_email='jpegiptc@degoulet.net',
    maintainer='Guillaume Degoulet',
    maintainer_email='jpegiptc@degoulet.net',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license='http://www.opensource.org/licenses/gpl-license.php',
    platforms=['any'],
    description="""Jpeg Iptc data raw extract/copy""",
    classifiers=[_f for _f in classifiers.split('\n') if _f],
    py_modules=['JpegIPTC'],
    )

