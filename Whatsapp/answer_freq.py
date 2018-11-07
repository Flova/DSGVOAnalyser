#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
from statistics import mean
import matplotlib.pyplot as plt

def to_timestamp(date_string):
    return time.mktime(datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S').timetuple())

me = "Florian Vahl"
chat_partner = ""
threshold = 3 #Stunden
blacklist = ["!Bosshood👍👌",]

with open("output.json") as f:
    chats = json.load(f)

average_values = []

def calc(chat_partner):
    chat = chats[chat_partner]
    if chat[0]["author"] == me:
        mode = True
    else:
        mode = False 
    diff = ([],[])

    for index, message in enumerate(chat):
        last_mode = mode
        if message["author"] == me:
            mode = True
        else:
            mode = False
        if mode != last_mode:
            last = index - 1
            if last > 0:
                temp = to_timestamp(message["time"]) - to_timestamp(chat[last]["time"])
                if temp < (threshold * 3600):
                    if mode:
                        diff[0].append(temp)
                    else: 
                        diff[1].append(temp)
    
    result = (round(mean(diff[0])/60), round(mean(diff[1])/60))
    # print("{}: {} Minuten | {}: {} Minuten".format(me, result[0], chat_partner, result[1]))
    return result

data = {}
if chat_partner == "":
    for chat in chats:
        if chat not in blacklist:
            data[chat] = calc(chat)
else:
    data[chat_partner] = calc(chat_partner)

diff_diff = {}
for chat_avg in data:
    temp = data[chat_avg][0] - data[chat_avg][1]
    diff_diff[chat_avg] = temp

plt.figure(figsize=(10,8))
plt.title("Answer time", fontsize=20)
plt.margins(0.01)
plt.ylabel('Minutes', fontsize=15)
plt.bar(data.keys(), [i[1] for i in data.values()])
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,8))
plt.title("Answer time diff", fontsize=20)
plt.margins(0.01)
plt.bar(diff_diff.keys(), diff_diff.values())
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
