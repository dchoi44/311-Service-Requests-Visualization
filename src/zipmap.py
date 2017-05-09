from csv import DictReader
from collections import Counter
from math import log

nCompl = Counter()
zips = []
with open('../docs/dataset/zips of NY.csv', 'r') as fin:
	for line in fin:
		zips.append(line.strip())

with open('../docs/dataset/Complaint by zipcode - 2016.csv', 'r') as fin:
	dr = DictReader(fin)
	for line in dr:
		zc = line['Incident Zip']
		try:
			if zc in zips:
				nCompl[zc] += 1
		except:
			pass

with open('../docs/dataset/complaints_ZC.csv', 'w') as fout:
	fout.write('ZC, number\n')
	elemplev = len(nCompl) / 9
	lev = 8
	i = 0
	for elem in nCompl.most_common():
		i += 1
		if i > elemplev and lev != 0:
			i = 1
			lev -= 1
		fout.write(elem[0] + ',' + str(lev) + '\n')