# -*- coding: utf-8 -*-

# https://newsapi.org/

# API-KEY: e9a1e1cf82e94fb497c5e16ac436a990

import urllib2 as url2
import urllib as url
import json

BASE_URL = "https://newsapi.org/v1/"
METHOD = "articles"
PARAMS = {
    "source": "cnn",
    "apiKey": "???"
}

res = url2.urlopen(BASE_URL + METHOD + "?" + url.urlencode(PARAMS)).read()

"""
for a in json.loads(res)["articles"][:3]:
    print
    print "Title: " + a["title"]
    print "Description: " + a["description"]
    print "Link: " + a["url"]
    print
"""

def get_news(source="cnn"):
    return None