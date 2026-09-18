from datetime import datetime,timezone
from email.utils import format_datetime,parsedate_to_datetime
from xml.sax.saxutils import escape

def format_rss_date(value):
 if not value:
  return format_datetime(datetime.now(timezone.utc))
 try:
  if isinstance(value,datetime):
   date=value
  else:
   text=str(value).strip()
   try:
    date=datetime.fromisoformat(text.replace('Z','+00:00'))
   except ValueError:
    date=parsedate_to_datetime(text)
  if date.tzinfo is None:
   date=date.replace(tzinfo=timezone.utc)
  return format_datetime(date.astimezone(timezone.utc))
 except (TypeError,ValueError,OverflowError):
  return format_datetime(datetime.now(timezone.utc))

def render(name,items,base=''):
 rows=[]
 for a in items:
  if a['extraction_status']!='success':continue
  pub=a['published_at'] or a['fetched_at'] or ''
  date=format_rss_date(pub)
  image = f'<p><img src="{escape(a["image_url"])}" alt="" /></p>' if a['image_url'] else ''
  rows.append(f'<item><title>{escape(a["title"] or "")}</title><link>{escape(a["url"])}</link><guid isPermaLink="true">{escape(a["url"])}</guid><pubDate>{date}</pubDate><description>{escape(a["title"] or "")}</description><content:encoded><![CDATA[{image}{a["content_html"] or ""}]]></content:encoded></item>')
 return '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel><title>'+escape(name)+'</title><link>https://www.lemonde.fr/</link><description>Articles complets accessibles avec abonnement</description>'+''.join(rows)+'</channel></rss>'
