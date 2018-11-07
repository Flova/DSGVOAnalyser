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
threshold = 24 #Stunden
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
    diff = [1,1]

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
                if temp > (threshold * 3600):
                    if mode:
                        diff[0] += 1
                    else: 
                        diff[1] += 1
    # print("{} hat {} mal ein Gespräch angfangen | {} hat {} mal ein Gespräch angfangen".format(me, diff[0], chat_partner, diff[1]))
    return round(diff[0] - diff[1]) / (abs(diff[0]) + abs(diff[1]))

data = {}
if chat_partner == "":
    for chat in chats:
        if chat not in blacklist:
            data[chat] = calc(chat)
else:
    data[chat_partner] = calc(chat_partner)

plt.figure(figsize=(10,8))
plt.title("Chat start diff", fontsize=20)
plt.margins(0.01)
plt.bar(data.keys(), data.values())
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()