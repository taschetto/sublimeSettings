import urllib.parse
import urllib.request
import http.cookiejar

url = 'http://stwebdv.thyssenkruppelevadores.com.br/scripts/gisdesenv.pl/swfw3.r'
values = {'usuario' : 'admin',
          'senha' : 'tke'}

cj = http.cookiejar.CookieJar()
data = urllib.parse.urlencode(values).encode('utf-8')
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
req = urllib.request.Request(url, data)
response = opener.open(req)
cj.extract_cookies(response, req)

print(cj._cookies)