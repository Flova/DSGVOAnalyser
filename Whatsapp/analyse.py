#!/usr/bin/env python3
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt


class WhatsappAnalyseFreq():
    def __init__(self, partner="Jana", me="Florian Vahl"):

        self.partner = partner
        self.me = me

        with open("output.json") as f:
            self.messages = json.load(f)[self.partner]

        counter = 0
        for message in self.messages:
            if message["author"] == self.me:
                counter += 1
        print("Anzahl Messages (Gesendet|Empfangen): ({}|{})".format(counter, len(self.messages)-counter))

        dates = []
        for message in self.messages:
            date = datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S')
            dates.append(time.mktime(date.timetuple()))

        self.chat_time = (min(dates),max(dates))

        # Calcs month step size
        time_delta = abs(self.chat_time[0] - self.chat_time[1])
        self.month_in_s = (86400 * 30.4167)
        self.month_count = int(round(time_delta/self.month_in_s, 0)) + 1

        self.months = [0]*(self.month_count)


        # Annotates lables
        self.lables = list()
        for counter, month in enumerate(self.months):
            month = datetime.utcfromtimestamp(self.chat_time[0] + counter * self.month_in_s).strftime('%b %y')
            self.lables.append(month)

    def plot_chat_freq(self):    
        # Counts messages for each month
        for message in self.messages:
            message_time = time.mktime(datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S').timetuple())
            month = int(round((message_time - self.chat_time[0])/self.month_in_s, 0))
            self.months[month] += 1

        # Converts values for plotting
        ys = self.months
        xs = list(range(0, self.month_count))
        plt.figure(figsize=(10,8))
        plt.title("Chat mit {}".format(self.partner), fontsize=20)
        plt.xlabel('Month', fontsize=15)
        plt.ylabel('Messages', fontsize=15)
        plt.xticks(xs, self.lables, rotation='vertical')
        plt.margins(0.01)
        plt.plot(xs, ys, 'bo', xs, ys, 'k')
        for x, y in zip(xs, ys):
            if y > 0:
                plt.annotate(y, xy = (x, y))
        plt.show()

    def plot_each_chat_freq(self):
        self.months = ([0]*(self.month_count), [0]*(self.month_count))

        # Counts messages for each month
        for message in self.messages:
            message_time = time.mktime(datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S').timetuple())
            month = int(round((message_time - self.chat_time[0])/self.month_in_s, 0))
            if message["author"] == self.me:
                self.months[0][month] += 1
            else:
                self.months[1][month] += 1

        # Converts values for plotting
        ys = self.months
        xs = list(range(0, self.month_count))
        plt.figure(figsize=(10,8))
        plt.title("Chat mit {}".format(self.partner), fontsize=20)
        plt.xlabel('Month', fontsize=15)
        plt.ylabel('Messages', fontsize=15)
        plt.xticks(xs, self.lables, rotation='vertical')
        plt.margins(0.01)
        plt.plot(xs, ys[0], 'bo', xs, ys[0], 'k')
        plt.plot(xs, ys[1], 'bo', xs, ys[1], 'r--')
        for x, y1, y2 in zip(xs, ys[0], ys[1]):
            if y1 > 0:
                plt.annotate(y1, xy = (x, y1))
            if y2 > 0:
                plt.annotate(y2, xy = (x, y2))
        plt.show()

if __name__ == "__main__":
    tool = WhatsappAnalyseFreq()
    tool.plot_chat_freq()
    tool.plot_each_chat_freq()
