import trafilatura
from bs4 import BeautifulSoup
def extract(html,url=''):
 content=trafilatura.extract(html,url=url,include_links=True,include_images=True,output_format='html') or ''
 s=BeautifulSoup(html,'html.parser'); t=s.find('meta',property='og:title') or s.title
 return {'title':(t.get('content',t.text).strip() if t else ''),'content_html':content,'chars':len(BeautifulSoup(content,'html.parser').get_text())}
