#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
from statistics import mean
import matplotlib.pyplot as plt


class WhatsappFirstStrike():
    def __init__(self, file="output.json", me="Florian Vahl", partner="", blacklist=None, threshold=24):
        self.me = me
        self.partner = partner
        self.threshold = threshold

        with open(file) as f:
            self.chats = json.load(f)

        self.average_values = []

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

    def to_timestamp(self, date_string):
        return time.mktime(datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S').timetuple())

    def calc(self, partner):
        chat = self.chats[partner]
        diff = [1,1]

        for index, message in enumerate(chat):
            last = index - 1
            if last > 0:
                temp = self.to_timestamp(message["time"]) - self.to_timestamp(chat[last]["time"])
                if temp > (self.threshold * 3600):
                    if message["author"] == self.me:
                        diff[0] += 1
                    else:
                        diff[1] += 1
        # print("{} hat {} mal ein Gespräch angfangen | {} hat {} mal ein Gespräch angfangen".format(me, diff[0], partner, diff[1]))
        return round(diff[0] - diff[1]) / (abs(diff[0]) + abs(diff[1]))


    def plot(self):
        data = {}
        if self.partner == "":
            for chat in self.chats:
                if chat not in self.blacklist:
                    data[chat] = self.calc(chat)
        else:
            data[self.partner] = calc(self.partner)

        plt.figure(figsize=(10,8))
        plt.title("Chat start diff", fontsize=20)
        plt.margins(0.01)
        plt.bar(data.keys(), data.values())
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    tool = WhatsappFirstStrike()
    tool.plot()