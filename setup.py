from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup


classifiers = [ 'Development Status :: 4 - Beta'
              , 'Environment :: Console'
              , 'Intended Audience :: Developers'
              , 'Intended Audience :: End Users/Desktop'
              , 'Intended Audience :: System Administrators'
              , 'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)'
              , 'Natural Language :: English'
              , 'Operating System :: MacOS :: MacOS X'
              , 'Operating System :: Microsoft :: Windows'
              , 'Operating System :: POSIX'
              , 'Programming Language :: Python :: 2.6'
              , 'Programming Language :: Python :: 2.7'
              , 'Programming Language :: Python :: Implementation :: CPython'
              , 'Topic :: Communications'
              , 'Topic :: Text Processing'
               ]

setup( author = 'Paul Jimenez'
     , author_email = 'pj@place.org'
     , classifiers = classifiers
     , description = 'NoteHandler is a Commandline Interface for Evernote'
     , entry_points = {'console_scripts': [ 'nh = notehandler:main' ]}
     , name = 'notehandler'
     , py_modules = [ 'distribute_setup', 'notehandler' ]
     , url = 'http://github.com/pjz/notehandler'
     # there must be nothing on the following line after the = other than a string constant
     , version = '0.5'
     , zip_safe = False
     , install_requires = [ 'evernote', 'cmdpy' ]
      )
