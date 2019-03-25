#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import emoji
import re
import operator
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt


class WhatsappEmojiAnalyse():
    def __init__(self, file="output.json", me="Florian Vahl", blacklist=["!Bosshood👍👌",]):
    
        self.me = me
        self.blacklist = blacklist
    
        with open(file) as f:
            self.chats = json.load(f)
    
    def plot(self):
        # Search in all chats
        result = list()
        for chat in self.chats:
            if chat not in self.blacklist:
                result.extend(self.analyse_chat(self.chats[chat]))

        histogram = Counter(result)
        reduced_histogram = histogram.most_common(20)

        reduced_histogram = dict(reduced_histogram)

        plt.figure(figsize=(10,6))
        plt.title("Emoji counter", fontsize=20)
        plt.margins(0.01)
        plt.bar([emoji.demojize(e) for e in reduced_histogram.keys()], reduced_histogram.values())
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

     # Search in single chat
    def analyse_chat(self, messages):
        emoji_list = list()
        for message in messages:
            if message["author"] == self.me:
                for character in message["message"]:
                    if character in emoji.UNICODE_EMOJI:
                        emoji_list.append(character)
        return emoji_list


if __name__ == "__main__":
    tool = WhatsappEmojiAnalyse()
    tool.plot()