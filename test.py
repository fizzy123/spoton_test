import re
import urllib2

from urlparse import urlparse

url = urlparse("http://www.sfmoma.org/exhib_events/exhibitions/513")
path = url.path

for section in path.split('/'):
    numbers_found = re.search(r"\d+", section)
    letters_found = re.search(r"[a-zA-Z]+", section)

    if numbers_found:
        if letters_found:
            print letters_found.group() 
            path = path.replace(section,'[a-zA-Z0-9\-]+',1)
        else:
            path = path.replace(section,'[0-9\-]+',1)

query = url.query
if query:
    query = "\?" + query
    m = re.search(r"=\d+", query)
    while m:
        query = query.replace(m.group(), "=[a-zA-Z0-9\-]+",1)
        m = re.search(r"=\d+", query)
regex = re.compile(path+query)        
links = []

html = urllib2.urlopen(url.geturl()).read()
m = re.search(regex, html)

for link in re.finditer(regex, html):
    if link.group() != url.path + "?" + url.query:
        href = url.hostname+link.group()
        if href not in links:
            links.append(href)
for link in links:
    print link
