import json, string

training = open('.csv', 'r')

dirty = []

for line in dirty_file:
	dirty.append(line)

dirty[-1] += '\n'
dirty = [' ' + item[:-1] + ' ' for item in dirty]

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


