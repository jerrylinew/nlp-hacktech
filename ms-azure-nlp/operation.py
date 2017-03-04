# -*- coding: utf-8 -*-

########### Python 2.7 #############
import httplib, urllib, base64, json, time

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '9732ea3a595942d7bb5e2758982fe6ad',
}

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("GET", "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/operations/4f3431841499411e95e1b8302bd1ee6e", "{body}", headers)
    response = conn.getresponse()
    data = response
    output = json.loads(data.read())
    conn.close()
except Exception as e:
    print e

for x in output["operationProcessingResult"]["topics"]:
    print x["keyPhrase"], x["score"]



