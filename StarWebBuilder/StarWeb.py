import http.cookiejar
import os
import urllib.parse
import urllib.request
from TableParser import *

class StarWeb(object):
  SUBDOMAIN = { 'gisdesenv':    'stwebdv',
                'gisgusdesenv': 'stwebdv',
                'gisprod':      'stweb',
                'gisgusprod':   'stweb' }

  BASE_URL = 'http://{s}.thyssenkruppelevadores.com.br'
  LOGIN_URL = BASE_URL + '/scripts/{e}.pl/swfw'
  BUILD_URL = BASE_URL + '/scripts/{e}.pl/progs/swfw0080'
  RUN_URL = BASE_URL + '/scripts/{e}.pl/progs/swfw0090'

  LOCAL_PATH = 'c:\\sisweb\\desenv\\ait\\'

  def __init__(self, environment, user, password):
    subdomain = StarWeb.SUBDOMAIN[environment]
    self.login_url = StarWeb.LOGIN_URL.format(s=subdomain, e=environment)
    self.build_url = StarWeb.BUILD_URL.format(s=subdomain, e=environment)
    self.run_url   = StarWeb.RUN_URL.format(s=subdomain, e=environment)
    self.credentials = {'usuario' : user, 'senha' : password}
    self.cookie_jar = http.cookiejar.CookieJar()
    self.http_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))

  def post(self, url, data):
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url, post_data)
    response = self.http_opener.open(request)
    return response.read().decode('cp1252')

  def login(self):
    message = 'Login efetuado com sucesso.'
    page = self.post(self.login_url, self.credentials)
    return message in str(page)

  def build(self, relative_file_path):
    print("Signing in to StarWeb ({u})...".format(u=self.login_url), end="", flush=True)
    if not self.login():
      print(" FAILED!\nBuild aborted!")
      return
    print(" DONE!")

    print("Building file with StarWeb ({u})...".format(u=self.build_url), end="", flush=True)
    builder_data = {'Arquivo' : StarWeb.LOCAL_PATH + relative_file_path.replace("/", "\\")}
    page = self.post(self.build_url, builder_data)
    print(" DONE!\n")

    parser = TableParser()
    return parser.feed(str(page))

  def run(self, script):
    print("Signing in to StarWeb ({u})...".format(u=self.login_url), end="", flush=True)
    if not self.login():
      print(" FAILED!\nRun aborted!")
      return
    print(" DONE!")

    print("Running script with StarWeb ({u})...".format(u=self.run_url), end="", flush=True)
    run_data = {'acao': 'executar', 'conteudoDoEditor' : script}
    page = self.post(self.run_url, run_data)
    print(" DONE!\n")

    content = XmpParser().feed(str(page))

    if content is None:
      content = TableParser().feed(str(page))

    return content