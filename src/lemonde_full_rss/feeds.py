import feedparser
from urllib.parse import urlsplit, urlunsplit
def normalize_url(url):
 p=urlsplit(url); return urlunsplit((p.scheme,p.netloc,p.path.rstrip('/'),'', ''))
def parse(data):
 out=[]
 for e in feedparser.parse(data).entries:
  u=normalize_url(e.get('link',''))
  if u:
   image=''
   media=e.get('media_content') or e.get('media_thumbnail') or []
   if media: image=media[0].get('url','')
   if not image and e.get('enclosures'): image=e.enclosures[0].get('href','') or e.enclosures[0].get('url','')
   if not image and e.get('image'): image=e.image.get('href','')
   out.append({'url':u,'title':e.get('title',''),'published_at':e.get('published',''), 'image_url':image})
 return out
