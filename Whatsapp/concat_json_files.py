#!/usr/bin/env python3
import os
import json
import sys

result = {}

def concat(path, file):
    with open(path + file) as f:
        data = json.load(f)
    partner = file.replace("WhatsApp Chat mit ", "")[:-5]
    result[partner] = data


def concat_folder(path):
    for file in os.listdir(path):
        if file.endswith(".json"):
            concat(path, file)
    return json.dumps(result, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit("Usage: {} /path/to/dir".format(sys.argv[0]))

    with open("output.json", 'w') as f:
        f.write(concat_folder(path))