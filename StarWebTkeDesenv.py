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
  stwebdv_url = 'http://stwebdv.thyssenkruppelevadores.com.br'
  stwebdv_path = '\\\\stwebdv\\sisweb\\desenv\\'
  stwebdv_local = 'c:\\sisweb\\desenv\\'

  #stweb_url = 'http://stweb.thyssenkruppelevadores.com.br'
  #stweb_path = '\\\\stweb\\sisweb\\produ\\'
  #stweb_local = 'c:/sisweb/produ/'

  login = '/scripts/gisdesenv.pl/swfw3'
  compiler = '/scripts/gisdesenv.pl/progs/swfw0080'

  login_url = stwebdv_url + login
  compiler_url = stwebdv_url + compiler

  # Parses command line arguments
  parser = argparse.ArgumentParser(description='Fator 7 TKE Desenv Compiler.')
  parser.add_argument("filepath")
  parser.add_argument("--basepath", default=stwebdv_path)
  args = parser.parse_args()

  skip_copy = False
  skip_compile = False

  print("Building '%s'..." % args.filepath)

  if ntpath.commonprefix([args.filepath, stwebdv_path]) == stwebdv_path:
    start_path, skip_copy = stwebdv_path, True
  else:
    start_path = args.basepath

  try:
    relative_path = ntpath.relpath(args.filepath, start=start_path)
  except:
    print("Failed! Perhaps you should use the --base parameter?")
    return

  # Skips include files
  file_name, file_extension = ntpath.splitext(relative_path)
  if file_extension == ".i":
    skip_compile = True

  # Copy file to server
  if not skip_copy:
    copy_to = stwebdv_path + relative_path

    if (not copyFile(args.filepath, copy_to)):
      print("Could not copy '" + args.filepath + "' to '" + copy_to + "'. Aborting...")
      sys.exit(0)
    print("Copied '" + args.filepath + "' to '" + copy_to + "'.")

  if skip_compile:
    print("Skipping compilation for '%s'..." % relative_path)
    return

  # Creates a cookie jar and a request opener
  cj = http.cookiejar.CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

  # Login to StarWeb
  login_data = {'usuario' : 'admin', 'senha' : 'tke'}
  sendPost(opener, login_url, login_data)

  # Compiles the specified file
  compiler_data = {'Arquivo' : stwebdv_local + relative_path}
  page = sendPost(opener, compiler_url, compiler_data).decode('iso8859-1')

  # Parses the response HTML to catch messages and errors
  parser = TableParser()
  parser.feed(str(page))

if __name__ == "__main__":
  main()