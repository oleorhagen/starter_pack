import os
import sys
import json
from collections import OrderedDict

def user_error(msg):
    sys.exit(msg)

def package_path():
    above_dir = os.path.dirname(__file__)
    return os.path.abspath(above_dir)

def above_package_path():
    path = package_path() + "/../"
    return os.path.abspath(path)

def read_json(path):
    try:
        with open(path, "r") as f:
            return json.loads(f.read(), object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        return None

def os_release(inp):
    if not inp:
        return None
    d = OrderedDict()
    for line in inp.split("\n"):
        line = line.strip()
        if "=" not in line:
            continue
        split = line.index("=")
        assert line[split] == "="
        key = line[0:split]
        assert "=" not in key
        value = line[split+1:]
        if len(value) > 1 and value[0] == value[-1] and value[0] in ["'", '"']:
            value = value[1:-1]
        d[key] = value
    return d

def column_print(data):
    width = 0
    for key in data:
        if len(key) > width:
            width = len(key)

    for key, value in data.items():
        fill = " " * (width - len(key))
        print("{}{} : {}".format(key, fill, value))

def pretty(data):
    return json.dumps(data, indent=2)
