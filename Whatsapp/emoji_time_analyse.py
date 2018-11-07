#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import emoji
import re
import operator
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
from progressbar import ProgressBar
from tabulate import tabulate


# Search in single chat
def analyse_chat(messages):
    for message in messages:
        if not(only_me) or message["author"] == me:
            timestamp = time.mktime(datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S').timetuple())
            for character in message["message"]:
                if character in emoji.UNICODE_EMOJI:
                    month = int(round((timestamp - chat_time[0])/month_in_s, 0))
                    months[month].append(character)

me = "Florian Vahl"
only_me = True
size = 15

blacklist = ["Bosshood👍👌",]

pbar = ProgressBar()

with open("output.json") as f:
    chats = json.load(f)

print("File loaded")

dates = []
for chat in chats:
    for message in chats[chat]:
        date = datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S')
        dates.append(time.mktime(date.timetuple()))
chat_time = (min(dates),max(dates))
print("Min/Max date found")

# Calcs month step size
time_delta = abs(chat_time[0] - chat_time[1])
month_in_s = (86400 * 30.4167)
month_count = int(round(time_delta/month_in_s, 0)) + 1
months = list()
for i in range(0, month_count):
    months.append(list())
print("List init")

# Search in all chats
for chat in pbar(chats):
    if chat not in blacklist:
        analyse_chat(chats[chat])

for month, value in enumerate(months):
    temp_histogram = Counter(value)
    reduced_histogram = dict(temp_histogram.most_common(size))
    months[month] = reduced_histogram

lables = [[datetime.utcfromtimestamp(chat_time[0] + month * month_in_s).strftime('%b %y')] for month, value in enumerate(months)]

print(tabulate([lables[month] + list(value) for month, value in enumerate(months)], headers=["Monat"] + ["Platz {}.".format(i) for i in range(1, size + 1)]))