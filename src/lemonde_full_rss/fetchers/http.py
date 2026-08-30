import httpx
from lemonde_full_rss.config import load_cookies
class HttpArticleFetcher:
 def __init__(self,s):self.s=s
 async def fetch(self,url):
  async with httpx.AsyncClient(cookies=load_cookies(self.s.cookies),headers={'User-Agent':self.s.ua},timeout=20,follow_redirects=True) as c:
   r=await c.get(url); low=r.text.lower(); auth=('connexion' in low or 'login' in str(r.url) or 'paywall' in low) and len(r.text)<100000
   return r.status_code,r.text,auth
