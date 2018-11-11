# -*- coding: utf-8 -*-


########################
# ####### SITE ####### #
# https://newsapi.org/ #
########################


# API-KEY: ???

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


# TODO: get list of 3 news of this source
# returns
#  [(name, description, link), (name, description, link), ...]
#
def get_news(source="cnn"):
    return None


# TODO: get list of sources
# returns
#  [source_1, source_2, source_3]
#
def get_sources():
    return None