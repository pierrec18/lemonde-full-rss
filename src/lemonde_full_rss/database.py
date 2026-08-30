import sqlite3
SCHEMA='''CREATE TABLE IF NOT EXISTS articles(id INTEGER PRIMARY KEY,url TEXT UNIQUE,canonical_url TEXT,title TEXT,subtitle TEXT,author TEXT,published_at TEXT,updated_at TEXT,fetched_at TEXT,content_html TEXT,extraction_status TEXT,extraction_method TEXT,http_status INTEGER,error TEXT,retries INTEGER DEFAULT 0);CREATE TABLE IF NOT EXISTS feeds(id INTEGER PRIMARY KEY,slug TEXT UNIQUE,name TEXT,source_url TEXT);CREATE TABLE IF NOT EXISTS article_feeds(article_id INTEGER,feed_id INTEGER,UNIQUE(article_id,feed_id));'''
class DB:
 def __init__(self,path):self.c=sqlite3.connect(path,check_same_thread=False);self.c.row_factory=sqlite3.Row;self.c.executescript(SCHEMA);self.c.commit()
 def feed(self,slug,name,url):self.c.execute('INSERT OR IGNORE INTO feeds(slug,name,source_url) VALUES(?,?,?)',(slug,name,url));self.c.commit();return self.c.execute('SELECT * FROM feeds WHERE slug=?',(slug,)).fetchone()
 def get(self,url):return self.c.execute('SELECT * FROM articles WHERE canonical_url=?',(url,)).fetchone()
 def add(self,i,f):
  self.c.execute('INSERT OR IGNORE INTO articles(url,canonical_url,title,published_at,extraction_status) VALUES(?,?,?,?,?)',(i['url'],i['url'],i.get('title',''),i.get('published_at'),'pending'));a=self.get(i['url']);self.c.execute('INSERT OR IGNORE INTO article_feeds VALUES(?,?)',(a['id'],f['id']));self.c.commit();return a
 def update(self,id,**kw):self.c.execute('UPDATE articles SET '+','.join(k+'=?' for k in kw)+' WHERE id=?',(*kw.values(),id));self.c.commit()
 def items(self,slug=None):
  q='SELECT DISTINCT a.* FROM articles a JOIN article_feeds af ON a.id=af.article_id JOIN feeds f ON f.id=af.feed_id';p=[]
  if slug:q+=' WHERE f.slug=?';p=[slug]
  return self.c.execute(q+' ORDER BY published_at DESC LIMIT 500',p).fetchall()
