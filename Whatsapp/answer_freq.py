#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
from statistics import mean
import matplotlib.pyplot as plt

class WhatsappAnswerFreq():
    def __init__(self, partner="", me="Florian Vahl", blacklist=["!Bosshood👍👌",]):
        self.me = me
        self.partner = partner
        self.threshold = 3 #Stunden
        self.blacklist = blacklist

        with open("output.json") as f:
            self.chats = json.load(f)

        self.average_values = []

    def to_timestamp(self, date_string):
        return time.mktime(datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S').timetuple())

    def calc(self, chat_partner):
        chat = self.chats[chat_partner]
        if chat[0]["author"] == self.me:
            mode = True
        else:
            mode = False 
        diff = ([],[])

        for index, message in enumerate(chat):
            last_mode = mode
            if message["author"] == self.me:
                mode = True
            else:
                mode = False
            if mode != last_mode:
                last = index - 1
                if last > 0:
                    temp = self.to_timestamp(message["time"]) - self.to_timestamp(chat[last]["time"])
                    if temp < (self.threshold * 3600):
                        if mode:
                            diff[0].append(temp)
                        else: 
                            diff[1].append(temp)
        
        result = (round(mean(diff[0])/60), round(mean(diff[1])/60))
        # print("{}: {} Minuten | {}: {} Minuten".format(me, result[0], chat_partner, result[1]))
        return result

    def plot(self):
        data = {}
        if self.partner == "":
            for chat in self.chats:
                if chat not in self.blacklist:
                    data[chat] = self.calc(chat)
        else:
            data[self.partner] = self.calc(self.partner)

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


if __name__ == "__main__":
    tool = WhatsappAnswerFreq()
    tool.plot()
