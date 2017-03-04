file = open('gamergate_tweets.csv', 'r')
newfile = open('gamergate.csv', 'w')

for line in file:
	a = line.split(',')
	newfile.write(a[0] + '\n')