import os
import json
from haralyzer import HarParser, HarPage

def check_har(file):
  all_errors = []
  pages = parse_har_to_pages(file)
  for page in pages:
    if '.html' in page.title:
      file = ''
      for char in pages[0].title:
        file += chr(ord(char))
      all_errors += check_locations(file.split('/')[-1])
    all_errors += check_min(page)
    all_errors += check_security(page)
  return all_errors

def parse_har_to_pages(file):
  har_pages = []
  with open(os.getcwd() + file, 'r') as f:
    har_parser = HarParser(json.loads(f.read()))

  for page in har_parser.pages:
    har_pages.append(page)

  return har_pages

def check_min(page):
  min_errors = []
  for file in page.css_files:
    if 0 > file['request']['url'].find('.min.'):
      min_errors.append({'location': file['request']['url'], 'message': 'Minify external CSS scripts.'})
  for file in page.js_files:
    if 0 > file['request']['url'].find('.min.'):
      min_errors.append({'location': file['request']['url'], 'message': 'Minify external JS scripts.'})
  return min_errors

def check_locations(file):
  location_errors = []
  file_lines = open(os.getcwd() + '/' + file, 'r').readlines()
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
      location_errors.append({'location': file_lines[tag], 'message': 'CSS tags should be placed in the head.'})

  for tag in js_tags:
    if not (body_tags[0] < tag < body_tags[-1]):
      location_errors.append({'location': file_lines[tag], 'message': 'JS tags should be placed at the end of the body.'})

  location_errors += check_repeats(file_lines, css_tags)
  location_errors += check_repeats(file_lines, js_tags)

  return location_errors

def check_repeats(file_line_array, tag_array):
  for line in tag_array:
    for other_line in tag_array[1:]:
      if file_line_array[line] == file_line_array[other_line]:
        return {'location': [file_line_array[line], file_line_array[other_line]], 'message': 'You have duplicate calls.'}

def check_security(page):
  security_errors = []
  requests = page.get_requests
  for request in requests:
    if len(request['request']['queryString']) > 0:
      if request['request']['url'].find('https') < 0:
        security_errors.append({'location': request['request']['url'], 'message': 'Your API call is unsecured.'})
      for item in request['request']['queryString']:
        for val in item.values():
          if 'key' in val:
            security_errors.append({'location': request['request']['url'], 'message': "Value of " + val + " should not be sent in the query parameters."})
  return security_errors



print 'Bad.har'
for item in check_har('/bad.har'):
  print item









