import urllib.parse
import urllib.request
import http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

loginUrl = 'http://stwebdv.thyssenkruppelevadores.com.br/scripts/gisdesenv.pl/swfw3.r'
loginData = {'usuario' : 'admin', 'senha' : 'tke'}

postData = urllib.parse.urlencode(loginData).encode('utf-8')
request = urllib.request.Request(loginUrl, postData)
response = opener.open(request)

compilerUrl = 'http://stwebdv.thyssenkruppelevadores.com.br/scripts/gisdesenv.pl/progs/swfw0080'
compilerData = {'Arquivo' : 'c:/sisweb/desenv/ait/ait_aacm1.html,c:/sisweb/desenv/ait/ait_aacm2.html,c:/sisweb/desenv/ait/ait_aacm3.html,'}

postData = urllib.parse.urlencode(compilerData).encode('utf-8')
request = urllib.request.Request(compilerUrl, postData)
response = opener.open(request)

page = response.read()
print(page)