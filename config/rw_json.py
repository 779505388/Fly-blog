from tool import sys_name
import json


def read_json():
    if sys_name == "Window":
        path = r".\config\config.json"
    else:
        path = "./config/config.json"
    with open(path, "rb+") as f:
        data = json.load(f)
        return data


def write_json(data):
    if sys_name == "Window":
        path = r".\config\config.json"
    else:
        path = "./config/config.json"
    with open(path, 'w') as f:
        json.dump(data, f)
