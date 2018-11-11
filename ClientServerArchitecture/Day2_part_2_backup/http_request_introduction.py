# -*- coding: utf-8 -*-

import urllib
import urllib2 as url

import httplib as http


def construct_url(host, path="", params={}):
    return "http://{0}/{1}?{2}".format(host, path, urllib.urlencode(params))

def construct_https_url(host, path="", params={}):
    return "https://{0}/{1}?{2}".format(host, path, urllib.urlencode(params))


def construct_path(path="", params={}):
    return "/{0}?{1}".format(path, urllib.urlencode(params))

"""
print construct_url("localhost:8888", "", {"q": "a"})
"""
# open url
"""
print url.urlopen(construct_url("localhost:8888", "", {"q": "a"})).read()
"""
# open url with custom params
"""
conn = http.HTTPConnection("localhost:8888")
conn.request("POST", construct_path("", {"x": 123}), urllib.urlencode({"name": "eman"}))

resp = conn.getresponse()

print resp.status
print resp.reason
print resp.read()

conn.close()
"""

