import urllib.parse
import urllib.request

url = 'http://stwebdv.thyssenkruppelevadores.com.br/scripts/gisdesenv.pl/swfw3.r'
values = {'usuario' : 'admin',
          'senha' : 'tke'}

data = urllib.parse.urlencode(values)
data = data.encode('utf-8') # data should be bytes
req = urllib.request.Request(url, data)
response = urllib.request.urlopen(req)
the_page = response.read()
print(the_page)