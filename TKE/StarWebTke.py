import argparse
import filecmp
import http.cookiejar
import ntpath
import os
import shutil
import sys
import urllib.parse
import urllib.request
import time

from html.parser import HTMLParser

class Builder(object):
  NETWORK_PATH = '\\\\stwebdv\\sisweb\\desenv\\'

  def __init__(self, args):
    self.args = args
    try:
      self.relative_path = ntpath.relpath(self.args.filepath, start=self.args.work_dir)
    except:
      try:
        self.relative_path = ntpath.relpath(self.args.filepath, start="T:\desenv")
      except:
        print("Failed! Perhaps you should use the --work_dir parameter?")
        sys.exit(0)

  def copy(self):
    print("Checking file paths...", end="", flush=True)
    destination_path = Builder.NETWORK_PATH + self.relative_path
    files_are_the_same = shutil._samefile(self.args.filepath, destination_path)
    print(" DONE!")

    if files_are_the_same:
      print("Files are the same. Skipping copy!")
      return
    else:
      print("Copying file to '" + destination_path + "'...", end="", flush=True)

    success = False
    try:
      shutil.copy(self.args.filepath, destination_path)
      success = True
    except shutil.Error as e:
      print(" FAILED!\n\tError: %s" % e)
    except OSError as e:
      print(" FAILED!\n\tOS Error: {m} ({n}).".format(m=e.strerror, n=e.errno))

    if (not success):
      print("\nBuild aborted!")
      sys.exit(0)

    print(" DONE!")

  def build(self):
    file_name, file_extension = ntpath.splitext(self.relative_path)
    if file_extension == ".i":
      print("Skipping build for {e} files.".format(e=file_extension))
      return

    star_web = StarWeb(self.args.env)
    star_web.build(self.relative_path)

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

class StarWeb(object):
  SUBDOMAIN = { 'gisdesenv':    'stwebdv',
                'gisgusdesenv': 'stwebdv',
                'gisprod':      'stweb',
                'gisgusprod':   'stweb' }

  BASE_URL = 'http://{s}.thyssenkruppelevadores.com.br'
  LOGIN_URL = BASE_URL + '/scripts/{e}.pl/swfw'
  BUILD_URL = BASE_URL + '/scripts/{e}.pl/progs/swfw0080'

  CREDENTIALS = {'usuario' : os.environ['starweb_user'], 'senha' : os.environ['starweb_password']}
  LOCAL_PATH = 'c:\\sisweb\\desenv\\'

  def __init__(self, environment):
    subdomain = StarWeb.SUBDOMAIN[environment]
    self.login_url = StarWeb.LOGIN_URL.format(s=subdomain, e=environment)
    self.build_url = StarWeb.BUILD_URL.format(s=subdomain, e=environment)
    self.cookie_jar = http.cookiejar.CookieJar()
    self.http_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))

  def post(self, url, data):
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url, post_data)
    response = self.http_opener.open(request)
    return response.read()

  def login(self):
    message = 'Login efetuado com sucesso.'
    page = self.post(self.login_url, StarWeb.CREDENTIALS)
    return message in str(page)

  def build(self, relative_file_path):
    print("Signing in to StarWeb ({u})...".format(u=self.login_url), end="", flush=True)
    if not self.login():
      print(" FAILED!\nBuild aborted!")
      return
    print(" DONE!")

    print("Building file with StarWeb ({u})...".format(u=self.build_url), end="", flush=True)
    builder_data = {'Arquivo' : StarWeb.LOCAL_PATH + relative_file_path}
    page = self.post(self.build_url, builder_data).decode('iso8859-1')
    print(" DONE!\n")

    parser = TableParser()
    return parser.feed(str(page))

def main():
  parser = argparse.ArgumentParser(description='Fator 7 TKE Builder.')
  parser.add_argument("filepath")
  parser.add_argument("--work_dir", default='\\\\stwebdv\\sisweb\\desenv\\')
  parser.add_argument("--env", default="gisgusdesenv")
  args = parser.parse_args()

  print("File:     {f}\nWork dir: {d}\nEnv:      {e}\n".format(f=args.filepath, d=args.work_dir, e=args.env))

  builder = Builder(args)
  builder.copy()
  builder.build()

if __name__ == "__main__":
  main()