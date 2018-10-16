from mpl_toolkits.basemap import Basemap
import numpy as np 
import json
import matplotlib.pyplot as plt
from progressbar import ProgressBar

class GoogleLoc():
    def __init__(self):
        self.pbar = ProgressBar()
        self.map = None
        self.locations = self.importer()

    def set_map(self, m):
        self.map = m
        
    def importer(self):
        with open('Google/Standortverlauf.json') as f:
            data = json.load(f)["locations"]
        print("File loaded")
        print(str(len(data)) + " Standortdaten.")
        return data

    def init_map(self):
        fig = plt.figure(figsize=(8, 8))
        m = Basemap(projection='lcc',
                    resolution=None,
                    width=6E6, height=6E6, 
                    lat_0=53, lon_0=9,)
        m.bluemarble()
        self.map = m
        print("Map loaded")

    def converter(self, data):
        latA = list()
        lonA = list()
        for dataset in self.pbar(data):
            Lat = float(dataset['latitudeE7'])/10000000
            Lon = float(dataset['longitudeE7'])/10000000
            latA.append(Lat)
            lonA.append(Lon)
        print("Data parsed and loaded in memory")
        return latA, lonA

    def plot(self, latA, lonA):
        x, y = self.map(lonA, latA)
        self.map.plot(x, y, 'o-', markersize=5, linewidth=1) 
        print("Gernerated lines")

    def run(self):
        self.plot(*self.converter(self.locations))

if __name__ == "__main__":
    worker = GoogleLoc()
    worker.init_map()
    worker.run()
    plt.title('Google Locations')
    plt.show()