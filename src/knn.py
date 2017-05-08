from sklearn.neighbors import KNeighborsClassifier
from csv import DictReader, DictWriter

complaints = []
with open('../docs/dataset/REFINED_311_Service_Requests_2016.csv', 'r') as fin:
	# Complaint Type,Descriptor,Borough,Latitude,Longitude
	dr = DictReader(fin)
	for line in dr:
		complaints += [line]

cnt = Counter()
for elem in complaints:
	cnt[elem['Complaint Type']] += 1

NAttrs = 5
offset = 10
NNeigh = 10
chosenAttr = [elem[0] for elem in cnt.most_common()[offset:offset + NAttrs]]

X = []
y = []

with open('../docs/dataset/REFINED_311_Service_Requests_2016.csv', 'r') as fin:
	# Complaint Type,Descriptor,Borough,Latitude,Longitude
	dr = DictReader(fin)
	for line in dr:
		if line['Complaint Type'] in chosenAttr:
			X.append([float(line['Longitude']), float(line['Latitude'])])
			y.append(chosenAttr.index(line['Complaint Type']))

neigh = KNeighborsClassifier(n_neighbors = NNeigh)
neigh.fit(X,y)

with open('../docs/dataset/gridPoints.csv', 'r') as fin:
	dr = DictReader(fin)
	with open('../docs/dataset/knnGridResult.csv', 'w') as fout:
		fout.write(','.join(chosenAttr) + '\n')
		for line in dr:
			fout.write(str(neigh.predict([[float(line['lon']), float(line['lat'])]])[0]) + ',' + line['lon'] + ',' + line['lat'] + '\n')
