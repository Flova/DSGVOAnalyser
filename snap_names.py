import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import json
import numpy as np 

with open('Snap/json/snap_history.json') as f:
    data = json.load(f)

with open('Snap/json/friends.json') as f:
    friends = json.load(f)["Friends"]

f = dict()
for friend in friends:
    f[friend["Username"]] = friend["Display Name"]
friends = f

def count_names(jsonobj, key):
    counter = dict()
    for a in jsonobj:
        try:
            counter[a[key]] += 1
        except KeyError:
            counter[a[key]] = 1
    lists = sorted(counter.items())
    x, y = zip(*lists)
    names = list()
    for index, value in enumerate(x):
        names.append(friends[value])
    return names, y

plt.subplot(1,2,1)
plt.bar(*count_names(data["Received Snap History"], "From"), width=0.2, color='b', align='center')
plt.ylabel('Snaps')
plt.xlabel('User')
plt.xticks(rotation=90)
plt.title('Snap History (Empfangen)')
plt.subplot(1,2,2)
plt.bar(*count_names(data["Sent Snap History"], "To"), width=0.2, color='b', align='center')
plt.ylabel('Snaps')
plt.xlabel('User')
plt.xticks(rotation=90)
plt.title('Snap History (Gesendet)')
plt.show()