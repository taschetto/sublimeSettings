from html.parser import HTMLParser

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

class XmpParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.in_xmp = False
  def handle_starttag(self, tag, attrs):
    if tag == 'xmp':
      self.in_xmp = True
  def handle_data(self, data):
    if self.in_xmp:
      data = data.strip()
      if len(data) > 0:
        print(data)
  def handle_endtag(self, tag):
    self.in_xmp = False