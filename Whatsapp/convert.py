#!/usr/bin/env python3
import os
import json
import re
import sys

from datetime import datetime

def conv_single_file(filename):
    with open(filename) as f:
        lines = f.readlines()

    result = list()

    for line in lines:
        if re.match("\d\d\.\d\d\.\d\d, \d\d:\d\d - ", line):
            # Line contains new message
            # Split after timestamp
            [stamp, foo] = line.split(' - ', 1)
            try:
                [author, message] = foo.strip().split(': ', 1)
            except ValueError:
                # Author does not exist, set to None
                message = foo.strip()
                author = None

            # Parse timestamp to ISO format
            time = datetime.strptime(stamp, "%d.%m.%y, %H:%M").strftime('%Y-%m-%dT%H:%M:%S')

            result.append({'time': time, 'author': author, 'message': message})
        else:
            # Line break in message, append to last message
            result[-1]['message'] += '\n' + line.strip()

    output_filename = filename.replace('txt', 'json')

    with open(output_filename, 'w') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4))

    print('Messages written to "{}"'.format(output_filename))

def conv_folder(path):
    for file in os.listdir(path):
        if file.endswith(".txt"):
            conv_single_file(path + file)

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit("Usage: {} /path/to/dir".format(sys.argv[0]))

    conv_folder(path)