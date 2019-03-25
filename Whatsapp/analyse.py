#!/usr/bin/env python3
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt

partner = "Jana"
me = "Florian Vahl"

with open("output.json") as f:
    messages = json.load(f)[partner]

counter = 0
for message in messages:
    if message["author"] == me:
        counter += 1
print("Anzahl Messages (Gesendet|Empfangen): ({}|{})".format(counter, len(messages)-counter))

dates = []
for message in messages:
    date = datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S')
    dates.append(time.mktime(date.timetuple()))

chat_time = (min(dates),max(dates))

# Calcs month step size
time_delta = abs(chat_time[0] - chat_time[1])
month_in_s = (86400 * 30.4167)
month_count = int(round(time_delta/month_in_s, 0)) + 1

months = [0]*(month_count)


# Annotates lables
lables = list()
for counter, month in enumerate(months):
    month = datetime.utcfromtimestamp(chat_time[0] + counter * month_in_s).strftime('%b %y')
    lables.append(month)

def plot_chat_freq():    
    # Counts messages for each month
    for message in messages:
        message_time = time.mktime(datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S').timetuple())
        month = int(round((message_time - chat_time[0])/month_in_s, 0))
        months[month] += 1

    # Converts values for plotting
    ys = months
    xs = list(range(0, month_count))
    plt.figure(figsize=(10,8))
    plt.title("Chat mit {}".format(partner), fontsize=20)
    plt.xlabel('Month', fontsize=15)
    plt.ylabel('Messages', fontsize=15)
    plt.xticks(xs, lables, rotation='vertical')
    plt.margins(0.01)
    plt.plot(xs, ys, 'bo', xs, ys, 'k')
    for x, y in zip(xs, ys):
        if y > 0:
            plt.annotate(y, xy = (x, y))
    plt.show()

def plot_each_chat_freq():
    months = ([0]*(month_count), [0]*(month_count))

    # Counts messages for each month
    for message in messages:
        message_time = time.mktime(datetime.strptime(message["time"], '%Y-%m-%dT%H:%M:%S').timetuple())
        month = int(round((message_time - chat_time[0])/month_in_s, 0))
        if message["author"] == me:
            months[0][month] += 1
        else:
            months[1][month] += 1

    # Converts values for plotting
    ys = months
    xs = list(range(0, month_count))
    plt.figure(figsize=(10,8))
    plt.title("Chat mit {}".format(partner), fontsize=20)
    plt.xlabel('Month', fontsize=15)
    plt.ylabel('Messages', fontsize=15)
    plt.xticks(xs, lables, rotation='vertical')
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
    plot_chat_freq()
    plot_each_chat_freq()
