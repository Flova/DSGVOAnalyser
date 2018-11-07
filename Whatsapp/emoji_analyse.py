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


# Search in single chat
def analyse_chat(messages):
    emoji_list = list()
    for message in messages:
        for character in message["message"]:
             if character in emoji.UNICODE_EMOJI:
                 emoji_list.append(character)
    return emoji_list

me = "Florian Vahl"

blacklist = ["Bosshood👍👌",]

with open("output.json") as f:
    chats = json.load(f)

# Search in all chats
result = list()
for chat in chats:
    if chat not in blacklist:
        result.extend(analyse_chat(chats[chat]))

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
