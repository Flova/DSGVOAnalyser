#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from Whatsapp.answer_freq import WhatsappAnswerFreq
from Whatsapp.chat_over_day import WhatsappChatOverDay
from Whatsapp.emoji_analyse import WhatsappEmojiAnalyse
from Whatsapp.emoji_time_analyse import WhatsappEmojiTimeAnalyse
from Whatsapp.first_strike import WhatsappFirstStrike

file="Whatsapp/output.json"

def show_all(file):
    toolbox = [ WhatsappAnswerFreq(file=file),
                WhatsappChatOverDay(file=file),
                WhatsappEmojiAnalyse(file=file),
                WhatsappEmojiTimeAnalyse(file=file),
                WhatsappFirstStrike(file=file)]

    for tool in toolbox:
        tool.plot()

if __name__ == "__main__":
    try:
        file = sys.argv[1]
    except IndexError:
        sys.exit("Usage: {} /path/to/file".format(sys.argv[0]))
    show_all(file)    