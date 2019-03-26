#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
import matplotlib.pyplot as plt

class WhatsappChatOverDay():
    def __init__(self, file="output.json", partner="", me="Florian Vahl", only_me=True):
        self.me = me
        self.only_me = only_me
        self.partner = partner

        with open(file) as f:
            self.chats = json.load(f)

        self.day = [0]*24

    def count(self, chat):
        for message in self.chats[chat]:
            if not(self.only_me) or message["author"] == self.me:
                self.day[int(datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S').strftime('%H'))] += 1

    def plot(self):
        if self.partner == "":
            for chat in self.chats:
                self.count(chat)
        else:
            self.count(self.partner)

        lables = []
        for hour, value in enumerate(self.day):
            lables.append(datetime.strptime(str(hour), '%H').strftime('%H:%M'))

        plt.figure(figsize=(10,6))
        plt.title("Chat over time", fontsize=20)
        plt.xlabel('Hour', fontsize=15)
        plt.ylabel('n', fontsize=15)
        plt.xticks(range(len(lables)), lables, rotation='vertical')
        plt.margins(0.01)
        plt.tight_layout()
        plt.plot(self.day, 'k')
        plt.show()


if __name__ == "__main__":
    tool = WhatsappChatOverDay()
    tool.plot()

