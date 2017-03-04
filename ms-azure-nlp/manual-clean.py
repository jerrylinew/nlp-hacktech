import json


with open('../data/dirty.json') as data_file:
	data = json.load(data_file)

not_letters_or_digits = u'!"#%()*+,-./:\';<=>?@[\]^_`{|}~\u2019\u2026\u201c\u201d\xa0'
translate_table = dict((ord(char), u'') for char in not_letters_or_digits)

for item in data['documents']:
	print '1,' + item['text'].lower().translate(translate_table)
