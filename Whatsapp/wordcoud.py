#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

me = "Florian Vahl"
only_me = True

blacklist = ["Bosshood👍👌",]

with open("output.json") as f:
    chats = json.load(f)

message_list = []
for chat in chats:
    if chat not in blacklist:
        for message in chats[chat]:
            if not(only_me) or message["author"] == me:
                message_list.append(message["message"])

text = " ".join(message_list).replace("<Medien ausgeschlossen>", "")
text = re.sub(r'\b[a-zA-Z]{1,5}\b', '', text)

# lower max_font_size
wordcloud = WordCloud(max_font_size=40, collocations=False).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()