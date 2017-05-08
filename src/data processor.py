from csv import DictReader, DictWriter
import copy
from collections import Counter

def attrProc(None):
	# Complaint Type,Descriptor,City,Status,Borough,Latitude,Longitude
	with open('../docs/dataset/REFINED_311_Service_Requests_2016.csv', 'r') as fin:
		dr = DictReader(fin)
		fn = copy.copy(dr.fieldnames)
		fn.pop(fn.index('City'))
		fn.pop(fn.index('Status'))
		with open('../docs/dataset/RREFINED_311_Service_Requests_2016.csv', 'w') as fout:
			dw = DictWriter(fout, fieldnames = fn, delimiter = ',', lineterminator = '\n')
			dw.writeheader()
			for line in dr:
				line.pop('City')
				line.pop('Status')
				dw.writerow(line)

complaints = []
with open('../docs/dataset/REFINED_311_Service_Requests_2016.csv', 'r') as fin:
	# Complaint Type,Descriptor,Borough,Latitude,Longitude
	dr = DictReader(fin)
	for line in dr:
		complaints += [line]

cnt = Counter()
for elem in complaints:
	cnt[elem['Complaint Type']] += 1

with open('../docs/dataset/data.stat', 'w') as fout:
	for elem in cnt.most_common():
		fout.write(elem[0] + ',' + str(elem[1]) + '\n')

