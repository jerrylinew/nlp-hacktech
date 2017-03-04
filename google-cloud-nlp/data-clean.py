import json, string

dirty_file = open('dirty.txt', 'r')
training = open('train1.csv', 'w')

dirty = []

for line in dirty_file:
	dirty.append(line)

dirty[-1] += '\n'
dirty = [' ' + item[:-1] + ' ' for item in dirty]

not_letters_or_digits = u'!"#%()*+,-./:;<=>?@[\]^_`{|}~\u2019\u2026\u201c\u201d\xa0'
translate_table = dict((ord(char), u'') for char in not_letters_or_digits)

with open('../data/gamergate.json') as data_file:
	data = [' ' + json.loads(line)['text'].lower().translate(translate_table) + ' ' for line in data_file]

for item in data:
	rating = 0
	for word in dirty:
		if word in item:
			print(item)
			while True:
				try:
					rating = int(input())
					if rating == 0 or rating == 1 or rating == -1:
						break
					else:
						print "Please enter a 0 or 1.\n"
				except Exception:
					print "Please enter a 0 or 1.\n"
			break
	if rating != -1:
		training.write(str(rating) + ',' + item + '\n')


