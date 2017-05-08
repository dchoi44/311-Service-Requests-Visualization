import json
import csv
from shapely.geometry import shape, Point

south = 40.496040
west = -74.255717
north = 40.915342
east = -73.697731

Ngrid = 100
origin = [north, west]
deltax = abs(east - west) / float(Ngrid)
deltay = abs(north - south) / float(Ngrid)
grids = []
for i in range(Ngrid):
	grids += [Point(west + j * deltax, north - i * deltay) for j in range(Ngrid)]

with open('../docs/dataset/NYC.geojson', 'r') as fin:
	js = json.load(fin)

res = []
for features in js['features']:
	newgrid = []
	poly = shape(features['geometry'])
	print features['properties']['BoroName']
	for p in grids:
		if poly.contains(p):
			res += [{'lon': p.x, 'lat': p.y}]
		else:
			newgrid += [p]
	grids = newgrid

with open('../docs/dataset/gridPoints.csv', 'wb') as fout:
	fn = ['lon', 'lat']
	csvout = csv.DictWriter(fout, delimiter = ',', fieldnames = fn)
	csvout.writeheader()
	for p in res:
		csvout.writerow(p)