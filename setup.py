#!/usr/bin/env python

from distutils.core import setup

setup(
  name='alvitr',
  version='1.0',
  description='An experiment of tsearch2-based fulltext search on Android SDK and beyond',
  author='Takahiro Yoshimura',
  author_email='altakey@gmail.com',
  url='http://github.com/taky/alvitr',
  packages=['alvitr'],
  requires=['beautifulsoup4', 'sqlalchemy', 'psycopg2'],
  scripts=['scripts/query.py', 'scripts/index.sh', 'scripts/load.py'],
  data_files=[("corps", ["corps/android-14.sql.xz"]), ("etc", ["etc/create.sql"])]
  )

