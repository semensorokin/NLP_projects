# -*- coding: utf-8 -*-

# http://fucking-great-advice.ru/api/
# http://fucking-great-advice.ru/api/random

import urllib2 as url2
from HTMLParser import HTMLParser
import json

res = url2.urlopen("http://fucking-great-advice.ru/api/random").read()

parser = HTMLParser()

print parser.unescape(json.loads(res)["text"])
