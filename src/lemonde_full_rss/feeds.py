import feedparser
from urllib.parse import urlsplit, urlunsplit
def normalize_url(url):
 p=urlsplit(url); return urlunsplit((p.scheme,p.netloc,p.path.rstrip('/'),'', ''))
def parse(data):
 out=[]
 for e in feedparser.parse(data).entries:
  u=normalize_url(e.get('link',''))
  if u: out.append({'url':u,'title':e.get('title',''),'published_at':e.get('published','')})
 return out
