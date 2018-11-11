# -*- coding: utf-8 -*-


##################################
# ########### SITE ############# #
# ##### http://fixer.io/ ####### #
##################################

# http://api.fixer.io/latest
# http://api.fixer.io/latest?base=RUB
# http://api.fixer.io/latest?symbols=USD,GBP

import urllib2 as url2
import json

res = url2.urlopen("http://api.fixer.io/latest?base=RUB").read()

print res

print json.loads(res)["rates"]["EUR"]
print json.loads(res)["rates"]["USD"]


# TODO: return currencies
# returns
# [ ("USD", 54.12), ("EUR", 63.212) ]
#   or for current base if mentioned
# [ ("JPY", 21.221) ]
def xchange(base=None):
    return None
