from mpl_toolkits.basemap import Basemap
import numpy as np 
import json
import matplotlib.pyplot as plt
from google_map import GoogleLoc

print("Init finished")

with open('Snap/json/location_history.json') as f:
    data = json.load(f)["Locations You Have Visited"]
    
print("Data loaded")

fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc',
            resolution='i',
            width=6E6, height=6E6, 
            lat_0=53, lon_0=9,)
m.bluemarble()

print("Map gernerated")

latA = list()
lonA = list()

for dataset in data:
    Lat = float(dataset['Latitude, Longitude'].split(",")[0][0:6])
    Lon = float(dataset['Latitude, Longitude'].split(",")[1][0:6])
    
    latA.append(Lat)
    lonA.append(Lon)

print("Data parsed and loaded in memory")

print("Load Google")
worker = GoogleLoc()
worker.set_map(m)
worker.run()
print("Finished Google Data")

x, y = m(lonA, latA)
m.plot(x, y, 'o-', markersize=5, linewidth=1) 

print("Lines drawed")

plt.title('Snap Locations')
plt.show()