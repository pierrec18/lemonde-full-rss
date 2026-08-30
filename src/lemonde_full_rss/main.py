import asyncio, logging, time
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from .config import Settings,load_feeds
from .database import DB
from .feeds import parse
from .fetchers.http import HttpArticleFetcher
from .fetchers.playwright import PlaywrightArticleFetcher
from .fetchers.kiosque import KiosqueArticleFetcher
from .extractors.generic import extract
logging.basicConfig(level=logging.INFO,format='%(levelname)s %(message)s');s=Settings();db=DB(s.db);session_state='unknown';last_refresh=None
async def refresh():
 global session_state,last_refresh
 try:
  async with httpx.AsyncClient(headers={'User-Agent':s.ua},timeout=20) as c:
   for slug,x in load_feeds(s.feeds).items():
    f=db.feed(slug,x['name'],x['url']); r=await c.get(x['url']); new=0
    for i in parse(r.content):
     a=db.add(i,f)
     if a['extraction_status']!='success':
      fetcher = {'playwright': PlaywrightArticleFetcher, 'kiosque': KiosqueArticleFetcher}.get(s.fetcher, HttpArticleFetcher)(s)
      code,html,auth=await fetcher.fetch(i['url'])
      if auth or code in (401,403): session_state='expired';db.update(a['id'],extraction_status='authentication_required',http_status=code,error='session expired');continue
      z=extract(html,i['url']); status='success' if z['chars']>300 else 'extraction_failed';db.update(a['id'],content_html=z['content_html'],extraction_status=status,extraction_method=s.fetcher,http_status=code,fetched_at=time.strftime('%Y-%m-%dT%H:%M:%SZ'));new+=status=='success'
    logging.info('feed_refresh feed=%s new=%s',slug,new)
  last_refresh=time.time()
 except Exception: logging.exception('feed_refresh_failed')
async def loop():
 while True: await refresh();await asyncio.sleep(s.interval)
@asynccontextmanager
async def lifespan(app):
 task=asyncio.create_task(loop());yield;task.cancel()
app=FastAPI(lifespan=lifespan)
def guard(req):
 if s.auth and req.query_params.get('token')!=s.token: raise HTTPException(401,'authentication required')
@app.get('/health')
def health():return {'status':'degraded' if session_state=='expired' else 'ok','lemonde_session':session_state,'last_refresh':last_refresh}
@app.get('/lemonde/{feed}.xml')
def rss(feed:str,request:Request):
 guard(request);return Response(render_name(feed),media_type='application/rss+xml')
def render_name(feed):
 from .rss import render
 return render(feed,db.items(None if feed=='all' else feed))
