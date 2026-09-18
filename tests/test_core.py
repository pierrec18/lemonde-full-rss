from lemonde_full_rss.feeds import normalize_url
from lemonde_full_rss.extractors.generic import extract
from lemonde_full_rss.rss import render
from lemonde_full_rss.database import DB
from tempfile import NamedTemporaryFile
def test_normalize(): assert normalize_url('https://www.lemonde.fr/a/?utm_source=x')=='https://www.lemonde.fr/a'
def test_extract():
 z=extract('<html><head><meta property="og:title" content="Titre"></head><body><article><p>Texte suffisamment long pour le test.</p></article></body></html>','https://x')
 assert z['title']=='Titre'
def test_rss():
 x={'title':'T','url':'https://www.lemonde.fr/a','extraction_status':'success','content_html':'<p>Bonjour</p>','published_at':'2026-01-01T00:00:00Z','fetched_at':'','image_url':''}
 out=render('Test',[x]);assert '<content:encoded>' in out and 'https://www.lemonde.fr/a' in out

def test_rss_preserves_rfc822_publication_date():
 x={'title':'T','url':'https://www.lemonde.fr/a','extraction_status':'success','content_html':'<p>Bonjour</p>','published_at':'Wed, 16 Sep 2026 21:00:00 +0200','fetched_at':'2026-09-18T19:00:00Z','image_url':''}
 out=render('Test',[x])
 assert '<pubDate>Wed, 16 Sep 2026 19:00:00 +0000</pubDate>' in out

def test_database_sorts_normalized_dates():
 with NamedTemporaryFile() as f:
  db=DB(f.name); feed=db.feed('une','une','https://example.test/une.xml')
  db.add({'url':'https://example.test/old','title':'Old','published_at':'Wed, 16 Sep 2026 21:00:00 +0200','image_url':''},feed)
  db.add({'url':'https://example.test/new','title':'New','published_at':'Fri, 18 Sep 2026 18:53:02 +0200','image_url':''},feed)
  assert [row['title'] for row in db.items('une')][:2] == ['New','Old']
