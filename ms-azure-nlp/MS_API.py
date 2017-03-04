# -*- coding: utf-8 -*-

########### Python 2.7 #############
import httplib, urllib, base64, json

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '9732ea3a595942d7bb5e2758982fe6ad',
}

#body = json.dumps(body)

file = "../data/dirty.json"
json_data = open(file).read()
json_data = unicode(json_data, errors='ignore')
body = json.loads(json_data, strict=False)

numdocs = len(body["documents"])
for i in range(100-numdocs):
    body["documents"].append({
      "id": 100-i,
      "text": body["documents"][i%numdocs]["text"]
    })

body = json.dumps(body)

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/text/analytics/v2.0/keyphrases?", body, headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    conn.close()
except Exception as e:
    print e

for x in data["documents"]:
    if len(x["keyPhrases"][0]) != 0:
      print x["keyPhrases"]