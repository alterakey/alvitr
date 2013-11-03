-- create.sql: search functions
-- Copyright (C) 2013 Takahiro Yoshimura <altakey@gmail.com>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.

drop schema if exists opt;
create schema opr;

drop function opr.doc_by_keyword(text, integer);
drop function opr.example_by_keyword(text, integer);
drop function opr.source_by_keyword(text, integer);
drop function opr.any_by_keyword(text, integer);

create function opr.doc_by_keyword(keywords text, limit_ integer) returns table (relpath text, rank real, headline text) as $$(select * from ((select relpath,1024 as rank, null as headline from docs where relpath ilike '%'||keywords||'%' order by length(relpath) limit limit_) union all (select AA.relpath,AA.rank as rank,'' as headline from (select relpath,q,ts_rank_cd(docs.keyword,q) as rank from docs,to_tsquery('english', keywords) as q where docs.keyword @@ q order by rank desc limit limit_) as AA)) as A order by A.rank desc, length(A.relpath))$$ language sql;
create function opr.example_by_keyword(keywords text, limit_ integer) returns table (relpath text, rank real, headline text) as $$(select * from ((select relpath,1024 as rank, null as headline from examples where relpath ilike '%'||keywords||'%' order by length(relpath) limit limit_) union all (select AA.relpath,AA.rank as rank,'' as headline from (select relpath,q,ts_rank_cd(examples.keyword,q) as rank from examples,to_tsquery(keywords) as q where examples.keyword @@ q order by rank desc limit limit_) as AA)) as A order by A.rank desc, length(A.relpath))$$ language sql;
create function opr.source_by_keyword(keywords text, limit_ integer) returns table (relpath text, rank real, headline text) as $$(select * from ((select relpath,1024 as rank, null as headline from sources where relpath ilike '%'||keywords||'%' order by length(relpath) limit limit_) union all (select AA.relpath,AA.rank as rank,'' as headline from (select relpath,q,ts_rank_cd(sources.keyword,q) as rank from sources,to_tsquery(keywords) as q where sources.keyword @@ q order by rank desc limit limit_) as AA)) as A order by A.rank desc, length(A.relpath))$$ language sql;
create function opr.any_by_keyword(keywords text, limit_ integer) returns table (relpath text, rank real, headline text) as $$select * from (select * from opr.doc_by_keyword(keywords, limit_) union select * from opr.example_by_keyword(keywords, limit_) union select * from opr.source_by_keyword(keywords, limit_)) as A order by rank desc, length(relpath)$$ language sql;
