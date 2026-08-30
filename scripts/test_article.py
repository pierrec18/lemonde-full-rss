import argparse,asyncio
from lemonde_full_rss.config import Settings
from lemonde_full_rss.fetchers.http import HttpArticleFetcher
from lemonde_full_rss.extractors.generic import extract
async def main():
 p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--save-html');a=p.parse_args();code,html,auth=await HttpArticleFetcher(Settings()).fetch(a.url);z=extract(html,a.url);print(f'HTTP: {code}\nAuth expired: {auth}\nHTML: {len(html)} bytes\nTitle: {z["title"]}\nText: {z["chars"]} chars\n{z["content_html"][:500]}')
 if a.save_html:open(a.save_html,'w').write(html)
asyncio.run(main())
