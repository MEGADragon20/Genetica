import json

def read():
    try:
        with open("logs/sexual_reproduction.json", "r") as f:
            a = json.load(f)
    except FileNotFoundError:
        a = {}
    return a
print(read())