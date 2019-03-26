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


class WhatsappEmojiTimeAnalyse():
    def __init__(self, file="output.json", me="Florian Vahl", only_me=True, blacklist=None, size=15):
        self.me = me
        self.only_me = me
        self.size = size

        self.pbar = ProgressBar()

        with open(file) as f:
            self.chats = json.load(f)

        print("File loaded")

        self.dates = []
        for chat in self.chats:
            for message in self.chats[chat]:
                date = datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S')
                self.dates.append(time.mktime(date.timetuple()))
        self.chat_time = (min(self.dates),max(self.dates))
        print("Min/Max date found")

        # Calcs month step size
        self.time_delta = abs(self.chat_time[0] - self.chat_time[1])
        self.month_in_s = (86400 * 30.4167)
        self.month_count = int(round(self.time_delta/self.month_in_s, 0)) + 1
        self.months = list()
        
        for i in range(0, self.month_count):
            self.months.append(list())
        
        print("List init")

        if blacklist is None:
            self.blacklist = self.generate_groulist()
        else:
            self.blacklist = blacklist

    def generate_groulist(self):
            grouplist = set()
            for chat in self.chats:
                members = set()
                for message in self.chats[chat]:
                    if message["author"] is not None:
                        members.add(message["author"])
                    if len(members) > 2:
                        grouplist.add(chat)
                        break
            return grouplist

    # Search in single chat
    def analyse_chat(self, messages):
        for message in messages:
            if not(self.only_me) or message["author"] == self.me:
                timestamp = time.mktime(datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S').timetuple())
                for character in message["message"]:
                    if character in emoji.UNICODE_EMOJI:
                        month = int(round((timestamp - self.chat_time[0])/self.month_in_s, 0))
                        self.months[month].append(character)

    def plot(self):
        # Search in all chats
        for chat in self.pbar(self.chats):
            if chat not in self.blacklist:
                self.analyse_chat(self.chats[chat])

        for month, value in enumerate(self.months):
            temp_histogram = Counter(value)
            reduced_histogram = dict(temp_histogram.most_common(self.size))
            self.months[month] = reduced_histogram

        lables = [[datetime.utcfromtimestamp(self.chat_time[0] + month * self.month_in_s).strftime('%b %y')] for month, value in enumerate(self.months)]

        print(tabulate([lables[month] + list(value) for month, value in enumerate(self.months)], headers=["Monat"] + ["Platz {}.".format(i) for i in range(1, self.size + 1)]))


if __name__ == "__main__":
    tool = WhatsappEmojiTimeAnalyse()
    tool.plot()