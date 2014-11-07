import argparse
import urllib.parse
import urllib.request
import http.cookiejar
from html.parser import HTMLParser
import shutil
import ntpath
import sys

def copyFile(src, dest):
  try:
    shutil.copy(src, dest)
  except shutil.Error as e:
    print('Error: %s' % e)
    return False;
  except IOError as e:
    print('Error: %s' % e.strerror)
    return False;
  return True;

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

def path_leaf(path):
  head, tail = ntpath.split(path)
  return tail or ntpath.basename(head)

def main():
  # paths and urls
  starweb_url = 'http://stwebdv.thyssenkruppelevadores.com.br'
  loginUrl = starweb_url + '/scripts/gisdesenv.pl/swfw3'
  compilerUrl = starweb_url + '/scripts/gisdesenv.pl/progs/swfw0080'
  starweb_local_path = 'c:/sisweb/desenv/ait/'
  network_path = '\\\\stwebdv\\sisweb\\desenv\\ait\\'

  # Parses command line arguments
  parser = argparse.ArgumentParser(description='Fator 7 TKE Desenv Compiler.')
  parser.add_argument("--copy", action="store_true")
  parser.add_argument("filepath")
  args = parser.parse_args()

  # Copy file to server
  if args.copy:
    copy_path = network_path + path_leaf(args.filepath)
    if (not copyFile(args.filepath, copy_path)):
      print("Could not copy '" + args.filepath + "' to '" + copy_path + "'. Aborting...")
      sys.exit(0)
    print("Copied '" + args.filepath + "' to '" + copy_path + "'.")

  # Creates a cookie jar and a request opener
  cj = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

  # Login to StarWeb
  loginData = {'usuario' : 'admin', 'senha' : 'tke'}
  sendPost(opener, loginUrl, loginData)

  # Compiles the specifief file
  compilerData = {'Arquivo' : starweb_local_path + path_leaf(args.filepath)}
  page = sendPost(opener, compilerUrl, compilerData).decode('iso8859-1')

  # Parses the response HTML to catch messages and errors
  parser = TableParser()
  parser.feed(str(page))

if __name__ == "__main__":
  main()