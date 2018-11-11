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
    "apiKey": "e9a1e1cf82e94fb497c5e16ac436a990"
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
    params = {
        "source": source,
        "apiKey": "e9a1e1cf82e94fb497c5e16ac436a990",
        "language": "ru"
    }

    print BASE_URL + METHOD + "?" + url.urlencode(params)

    res = url2.urlopen(BASE_URL + METHOD + "?" + url.urlencode(params)).read()


    return "\n".join([
        """=== {0} ===\n{1}\nlink:  {2}\n"""
            .format(a["title"].encode('utf8'), a["description"].encode('utf8'), a["url"])
        for a in json.loads(res)["articles"][:3]
    ])

