# load.py: Documentation/text loader.
# Copyright (C) 2013 Takahiro Yoshimura <altakey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os
import binascii
import bs4
import re

def preamble(table):
  return u'''\
drop table if exists %(table)s;
create table %(table)s (relpath varchar, content text, keyword tsvector);
begin;
''' % dict(table=table)

def postamble(table, lang=None):
  if lang:
    return u'''\
update %(table)s set keyword=to_tsvector('%(lang)s', content);
commit;
create index %(table)s_keyword_idx on %(table)s using gin(keyword);
''' % dict(table=table, lang=lang)
  else:
    return u'''\
update %(table)s set keyword=to_tsvector(content);
commit;
create index %(table)s_keyword_idx on %(table)s using gin(keyword);
''' % dict(table=table)


def load_file_doc(table, path):
  with open(path, 'r') as f:
    try:
      return load(table, path, bs4.BeautifulSoup(f.read()).find(id='doc-col').get_text())
    except AttributeError:
      return None

def load_file(table, path):
  with open(path, 'r') as f:
    try:
      return load(table, path, f.read().decode('utf-8'))
    except UnicodeDecodeError:
      if path.lower().endswith('java'):
        return load(table, path, f.read().decode('utf-8', 'ignore'))
      return None

def load(table, path, content):
  def escape(text):
    escaped = text.replace(u'\\', ur'\\').replace(ur"'", ur"''")
    return escaped
  content = re.sub(u'[\n\t ]+', u' ', content)
  return u"insert into %(table)s (relpath, content) values ('%(path)s', '%(content)s');\n" % dict(table=table, path=escape(path), content=escape(content))

if __name__ == '__main__':
  import getopt

  as_doc = False
  table = None

  try:
    o, a = getopt.getopt(sys.argv[1:], 'dv', ['--as-doc', '--verbatim'])
    if o in ('-d', '--as-doc'):   as_doc = True
    if o in ('-v', '--verbatim'): as_doc = False
    table = a[0]
  except getopt.GetoptError, e:
    raise

  sys.stdout.write(preamble(table).encode('utf-8'))
  for fn in (r[:-1] for r in sys.stdin):
    if as_doc:
      content = load_file_doc(table, fn)
    else:
      content = load_file(table, fn)
    if content:
      content = content.encode('utf-8')
      sys.stdout.write(content)
      print >>sys.stderr, '%s (%d o)' % (fn, len(content))
    else:
      print >>sys.stderr, "skipping %s" % fn
  if as_doc:
    sys.stdout.write(postamble(table, lang='english').encode('utf-8'))
  else:
    sys.stdout.write(postamble(table, lang=None).encode('utf-8'))
