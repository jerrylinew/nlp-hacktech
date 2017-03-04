import requests

data =  {"id": "nlp-hacktech",
 "storageDataLocation": "nlp-hacktech/train.csv"}

r = requests.post('https://www.googleapis.com/prediction/v1.6/projects/nlp-hacktech/trainedmodels', data)

print(r.json)