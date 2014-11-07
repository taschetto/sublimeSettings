import urllib.parse
import urllib.request
import http.cookiejar
from html.parser import HTMLParser

def sendPost(opener, url, data):
  postData = urllib.parse.urlencode(data).encode('utf-8')
  request = urllib.request.Request(url, postData)
  response = opener.open(request)
  return response.read()

class TableParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.in_td = False
  def handle_starttag(self, tag, attrs):
    if tag == 'td':
      self.in_td = True
  def handle_data(self, data):
    if self.in_td:
      data = data.strip()
      if len(data) > 0:
        print(data)
  def handle_endtag(self, tag):
    self.in_td = False

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

loginUrl = 'http://stwebdv.thyssenkruppelevadores.com.br/scripts/gisdesenv.pl/swfw3.r'
loginData = {'usuario' : 'admin', 'senha' : 'tke'}

sendPost(opener, loginUrl, loginData)

compilerUrl = 'http://stwebdv.thyssenkruppelevadores.com.br/scripts/gisdesenv.pl/progs/swfw0080'
compilerData = {'Arquivo' : 'c:/sisweb/desenv/ait/ait_aacm1.html,c:/sisweb/desenv/ait/ait_aacm2.html,c:/sisweb/desenv/ait/ait_aacm3.html,'}

page = sendPost(opener, compilerUrl, compilerData).decode('iso8859-1')

parser = TableParser()
parser.feed(str(page))