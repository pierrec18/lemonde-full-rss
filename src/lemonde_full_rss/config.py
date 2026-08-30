import os, json, yaml
from dataclasses import dataclass
@dataclass
class Settings:
 db:str=os.getenv('DATABASE_PATH','data/lemonde.db'); feeds:str=os.getenv('FEEDS_CONFIG','config/feeds.yaml'); cookies:str=os.getenv('COOKIES_PATH','secrets/lemonde-cookies.json'); interval:int=int(os.getenv('POLL_INTERVAL_SECONDS','300')); ua:str=os.getenv('USER_AGENT','lemonde-full-rss/0.1'); auth:bool=os.getenv('RSS_AUTH_ENABLED','false').lower()=='true'; token:str=os.getenv('RSS_TOKEN',''); admin_token:str=os.getenv('ADMIN_TOKEN',''); fetcher:str=os.getenv('FETCHER','http').lower()
def load_feeds(path):
 with open(path) as f:return yaml.safe_load(f).get('feeds',{})
def load_cookies(path):
 if not os.path.exists(path):return {}
 with open(path) as f:d=json.load(f)
 return {x['name']:x['value'] for x in d} if isinstance(d,list) else d
