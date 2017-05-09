from csv import DictReader, DictWriter
from time import strptime
import numpy as np

ntypes = 20
cptypes = []

with open('../docs/dataset/data.stat', 'r') as fin:
	for i,line in enumerate(fin):
		if i >= ntypes: break
		cptypes.append(line.strip().split(',')[0])

graphs = [[0 for i in range(48)] for j in range(ntypes)]
graphs = np.asarray(graphs)

with open('../docs/dataset/Complaint by zipcode - 2016.csv', 'r') as fin:
	dr = DictReader(fin)
	for line in dr:
		if line['Complaint Type'] in cptypes:
			temp = strptime(line['Created Date'], '%m/%d/%Y %I:%M:%S %p')
			tempidx = 2 * temp.tm_hour + (1 if temp.tm_min >= 30 else 0)

			graphs[cptypes.index(line['Complaint Type'])][tempidx] += 1

graphs = graphs.T

with open('../docs/dataset/streamGraph.csv', 'w') as fout:
	fout.write(','.join(cptypes)+'\n')
	for elem in graphs:
		fout.write(','.join(map(str,elem)) + '\n')
	fout.write(','.join(map(str,graphs[0])))