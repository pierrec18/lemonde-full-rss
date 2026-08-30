from datetime import datetime,timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape
def render(name,items,base=''):
 rows=[]
 for a in items:
  if a['extraction_status']!='success':continue
  pub=a['published_at'] or a['fetched_at'] or ''
  try: date=format_datetime(datetime.fromisoformat(pub.replace('Z','+00:00'))) if pub else format_datetime(datetime.now(timezone.utc))
  except ValueError: date=format_datetime(datetime.now(timezone.utc))
  image = f'<p><img src="{escape(a["image_url"])}" alt="" /></p>' if a['image_url'] else ''
  rows.append(f'<item><title>{escape(a["title"] or "")}</title><link>{escape(a["url"])}</link><guid isPermaLink="true">{escape(a["url"])}</guid><pubDate>{date}</pubDate><description>{escape(a["title"] or "")}</description><content:encoded><![CDATA[{image}{a["content_html"] or ""}]]></content:encoded></item>')
 return '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel><title>'+escape(name)+'</title><link>https://www.lemonde.fr/</link><description>Articles complets accessibles avec abonnement</description>'+''.join(rows)+'</channel></rss>'
