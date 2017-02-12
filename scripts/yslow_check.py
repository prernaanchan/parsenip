import os
import json
from haralyzer import HarParser, HarPage

def check_har(file):
  pages = parse_har_to_pages(file);
  print 'Check Locations of JS and CSS Files'
  print check_locations()
  for page in pages:
    print 'Check Whether Files Minified'
    print check_min(page)
    print 'Check Whether Multiple Copies of Files'
    print check_repeats(page)

def parse_har_to_pages(file):
  har_pages = []
  with open(os.getcwd() + file, 'r') as f:
    har_parser = HarParser(json.loads(f.read()))

  for page in har_parser.pages:
    har_pages.append(page)

  return har_pages

def check_min(page):
  for file in page.css_files:
    if 0 > file['request']['url'].find('.min.'):
      return False
  for file in page.js_files:
    if 0 > file['request']['url'].find('.min.'):
      return False
  return True

def check_locations():
  file_lines = open(os.getcwd() + '/index.html', 'r').readlines()
  head_tags = []
  body_tags = []
  css_tags = []
  js_tags = []
  for line in range(len(file_lines)):
    if 'body' in file_lines[line]:
      body_tags.append(line)
    elif 'head' in file_lines[line]:
      head_tags.append(line)
    elif '.css' in file_lines[line]:
      css_tags.append(line)
    elif'.js' in file_lines[line]:
      js_tags.append(line)

  for tag in css_tags:
    if not (head_tags[0] < tag < head_tags[-1]):
      return False

  for tag in js_tags:
    if not (body_tags[0] < tag < body_tags[-1]):
      return False

  return True

def check_repeats(page):
  for file in page.css_files:
    if page.css_files.count(file) > 1:
      return True

  for file in page.js_files:
    if page.js_files.count(file) > 1:
      return True

  return False

# check_har('/bad.har')

pages = parse_har_to_pages('/bad.har')
print len(pages[0].css_files)






