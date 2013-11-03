# query.py: Query issuer.
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
import sqlalchemy as sa

def query(c, type_, keywords, limit):
    return c.execute(
        sa.sql.text(
            u'select relpath,rank,headline from opr.%(type)s_by_keyword(:keywords, :limit_)' % dict(type=type_),
        ),
        keywords=u'&'.join(keywords),
        limit_=limit
    )

if __name__ == '__main__':
    import sys
    import getopt

    def help(e=None):
        if e:
            print >>sys.stderr, e
        print >>sys.stderr, "usage: %s [--limit=n] [--docs] [--examples] [--sources] <keyword> ..." % sys.argv[0]
        sys.exit(1)

    limit = 100
    type_ = 'any'

    try:
        opts, keywords = getopt.getopt(sys.argv[1:], 'l:des', ['limit=','docs','examples','sources'])
        for o, a in opts:
            if o in ('-l', '--limit'): limit = int(a)
            if o in ('-d', '--docs'): type_ = 'doc'
            if o in ('-e', '--examples'): type_ = 'example'
            if o in ('-s', '--sources'): type_ = 'source'
    except getopt.GetoptError, e:
        help(e)

    if not keywords:
        help()

    keywords = u' '.join((unicode(text, 'utf-8') for text in keywords)).split(u' ')
    e = sa.create_engine('postgres://localhost/')
    with e.connect() as c:
        print 'Searching %r (limiting to %d)' % (keywords, limit)
        for relpath, rank, headline in query(c, type_, keywords, limit):
            print 'link:1:%.01f:http://developer.android.com/%s' % (rank, relpath.replace('docs/', ''))
