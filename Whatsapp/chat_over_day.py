#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
import matplotlib.pyplot as plt

me = "Florian Vahl"
only_me = True
chat_partner = ""

with open("output.json") as f:
    chats = json.load(f)

day = [0]*24

def count(chat):
    for message in chats[chat]:
        if not(only_me) or message["author"] == me:
            day[int(datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S').strftime('%H'))] += 1

if chat_partner == "":
    for chat in chats:
        count(chat)
else:
    count(chat_partner)

lables = []
for hour, value in enumerate(day):
    lables.append(datetime.strptime(str(hour), '%H').strftime('%H:%M'))

plt.figure(figsize=(10,6))
plt.title("Chat over time", fontsize=20)
plt.xlabel('Hour', fontsize=15)
plt.ylabel('n', fontsize=15)
plt.xticks(range(len(lables)), lables, rotation='vertical')
plt.margins(0.01)
plt.tight_layout()
plt.plot(day, 'k')
plt.show()

