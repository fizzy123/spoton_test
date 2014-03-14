import re, urllib, json
import urllib2

from urlparse import urlparse

from django.http import HttpResponse

def get_addresses(request):
    url = urlparse(urllib2.unquote(request.GET['url'].decode("utf8")))
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
        if url.query:
            home_url = url.path + "?" + url.query
        else:
            home_url = url.path

        if link.group() !=  home_url:
            href = url.hostname+link.group()
            if href not in links:
                links.append(href)

    html = urllib2.urlopen(url.scheme + "://" + url.hostname).read()
    m = re.search(regex, html)

    for link in re.finditer(regex, html):
        if url.query:
            home_url = url.path + "?" + url.query
        else:
            home_url = url.path

        if link.group() != home_url:
            href = url.hostname+link.group()
            if href not in links:
                links.append(href)

    json_links = json.dumps({'links':links})
    return HttpResponse(json_links, content_type="application/json")
