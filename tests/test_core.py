from lemonde_full_rss.feeds import normalize_url
from lemonde_full_rss.extractors.generic import extract
from lemonde_full_rss.rss import render
def test_normalize(): assert normalize_url('https://www.lemonde.fr/a/?utm_source=x')=='https://www.lemonde.fr/a'
def test_extract():
 z=extract('<html><head><meta property="og:title" content="Titre"></head><body><article><p>Texte suffisamment long pour le test.</p></article></body></html>','https://x')
 assert z['title']=='Titre'
def test_rss():
 x={'title':'T','url':'https://www.lemonde.fr/a','extraction_status':'success','content_html':'<p>Bonjour</p>','published_at':'2026-01-01T00:00:00Z','fetched_at':''}
 out=render('Test',[x]);assert '<content:encoded>' in out and 'https://www.lemonde.fr/a' in out
