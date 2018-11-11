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

