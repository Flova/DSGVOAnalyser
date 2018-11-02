from mpl_toolkits.basemap import Basemap
import numpy as np 
import json
import matplotlib.pyplot as plt
from google_map import GoogleLoc
from progressbar import ProgressBar

class SnapLoc():
    def __init__(self):
        self.pbar = ProgressBar()
        self.map = None
        self.locations = self.importer()

    def importer(self):
        with open('Snap/json/location_history.json') as f:
            data = json.load(f)["Locations You Have Visited"]
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
            Lat = float(dataset['Latitude, Longitude'].split(",")[0][0:6])
            Lon = float(dataset['Latitude, Longitude'].split(",")[1][0:6])
            latA.append(Lat)
            lonA.append(Lon)
        print("Data parsed and loaded in memory")
        return latA, lonA

    def plot(self, latA, lonA):
        x, y = self.map(lonA, latA)
        self.map.plot(x, y, 'o-', markersize=5, linewidth=1) 
        print("Lines drawed")

    def run(self):
        self.plot(*self.converter(self.locations))


if __name__ == "__main__":
    print("Load Snap")
    snap_worker = SnapLoc()
    snap_worker.init_map()
    snap_worker.run()
    print("Load Google")
    g_worker = GoogleLoc()
    g_worker.set_map(snap_worker.map)
    g_worker.run()
    print("Finished Google Data")
    plt.title('Snap Locations')
    plt.show()