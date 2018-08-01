import os
import sys
import json
from collections import OrderedDict
from cf_remote import log


def user_error(msg):
    sys.exit("cf-remote: " + msg)


def mkdir(path):
    if not os.path.exists(path):
        log.info("Creating directory: {}".format(path))
        os.mkdir(path)
    else:
        log.debug("Directory already exists: {}".format(path))


def ls(path):
    return os.listdir(path)


def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


def save_file(path, data):
    with open(path, "w") as f:
        f.write(data)


def read_json(path):
    data = read_file(path)
    if data:
        data = json.loads(data, object_pairs_hook=OrderedDict)
    return data


def pretty(data):
    return json.dumps(data, indent=2)


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
        log.debug("Cannot parse os-release file (empty)")
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
        value = line[split + 1:]
        if (len(value) > 1 and value[0] == value[-1]
                and value[0] in ["'", '"']):
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


def find_packages(path, extension=None, arch=None, os=None, hub=False):
    packages = ls(path)
    if extension:
        packages = filter(lambda p: p.endswith(extension), packages)
    if arch:
        if arch == "32":
            packages = filter(lambda p: "64" not in p, packages)
        else:
            packages = filter(lambda p: arch in p, packages)
    if hub:
        packages = filter(lambda p: "hub" in p, packages)
    else:
        packages = filter(lambda p: "hub" not in p, packages)
    return list(packages)
