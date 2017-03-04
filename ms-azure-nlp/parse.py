import sys, json, string

fileob = "../data/obscene.txt"
fob = open(fileob)

badwords = []

for line in fob:
	badwords.append(line[:-1])

filein = "../data/andy.txt"
fileout = "../data/andyout.txt"
fin = open(filein)
fout = open(fileout, 'w')

count = 0

for i,line in enumerate(fin):
	tmp = line.split('+')
	trimmed = tmp[len(tmp)-1][1:]
	trimmed = trimmed.lower()
	
	trimmed = "".join(l for l in trimmed if l not in string.punctuation and l != '\n')
	arr = trimmed.split(' ')
	arr = [a for a in arr if a != '']
	trimmed = " ".join(arr)
	
	for bad in badwords:
		grade = 0
		if bad in arr:
			print trimmed
			while True:
				try:
					grade = int(input())
					if grade == 0 or grade == 1 or grade == -1:
						break
					else:
						print ("Please enter integer between [-1,1]")
				except Exception:
					print ("Please enter an integer")
					print trimmed				
			break
	if grade != -1:
		output = str(grade) + "," + trimmed + "\n"
		fout.write(output)
	
	if i % 1000 == 0:
		print i
print count