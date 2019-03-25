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
char_list = "der die und in den von zu das mit sich des auf für ist im dem nicht ein Die eine als auch es an werden aus er hat daü sie nach wird bei einer Der um am sind noch wie einem über einen Das so Sie zum war haben nur oder aber zur bis mehr durch man sein wurde sei In Prozent hatte kann gegen vom können schon wenn habe seine Mark ihre dann unter wir soll ich eines Es Jahr zwei Jahren diese dieser wieder keine Uhr seiner worden Und will zwischen Im immer Millionen Ein was sagte"
# text = re.sub("|".join(char_list.split(" ")), "", text)

# lower max_font_size
wordcloud = WordCloud(max_font_size=40, collocations=False).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()