from sklearn.neighbors import KNeighborsClassifier
from csv import DictReader
from collections import Counter
import matplotlib.pyplot as plt

complaints = []
with open('../docs/dataset/REFINED_311_Service_Requests_2016.csv', 'r') as fin:
	# Complaint Type,Descriptor,Borough,Latitude,Longitude
	dr = DictReader(fin)
	for line in dr:
		complaints += [line]

cnt = Counter()
for elem in complaints:
	cnt[elem['Complaint Type']] += 1

complaintList = ['Noise - Residential', 'Illegal Parking', 'UNSANITARY CONDITION', 'Homeless Person Assistance', 'Rodent']
NNeigh = 20
Nchunk = 20

X = []
y = []

with open('../docs/dataset/REFINED_311_Service_Requests_2016.csv', 'r') as fin:
	# Complaint Type,Descriptor,Borough,Latitude,Longitude
	dr = DictReader(fin)
	for line in dr:
		if line['Complaint Type'] in complaintList:
			X.append([float(line['Longitude']), float(line['Latitude'])])
			y.append(complaintList.index(line['Complaint Type']))

blocksize = len(X) / Nchunk
result = []
maxscore = 0

for i in range(NNeigh):
	lb = 0
	rb = lb + blocksize + 1
	result.append([])
	print str(i + 1) + ' neighbors...'
	while rb <= len(X):
		Xte = X[lb:rb]
		Xtr = X[:lb] + X[rb:]
		yte = y[lb:rb]
		ytr = y[:lb] + y[rb:]

		neigh = KNeighborsClassifier(n_neighbors = i + 1)
		neigh.fit(Xtr,ytr)
		result[-1].append(neigh.score(Xte, yte))
		if result[-1][-1] > maxscore:
			maxscore = result[-1][-1]
			bestN = i + 1
			bestModel = neigh

		lb += blocksize
		rb += blocksize

plt.figure(figsize=(10,5))
plt.boxplot(result)
plt.xlabel('K value')
plt.ylabel('Score')
plt.title('Cross validation result')
plt.show()

neigh = bestModel
with open('../docs/dataset/gridPoints.csv', 'r') as fin:
	dr = DictReader(fin)
	with open('../docs/dataset/knnGridResult.csv', 'w') as fout:
		fout.write(','.join(complaintList) + '\n')
		for line in dr:
			fout.write(str(neigh.predict([[float(line['lon']), float(line['lat'])]])[0]) + ',' + line['lon'] + ',' + line['lat'] + '\n')
