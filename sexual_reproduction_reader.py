import json
import matplotlib.pyplot as plt

def read():
    all_lines = []
    try:
        with open("logs/sexual_reproduction.json", "r") as f:
            d = json.load(f)
    except FileNotFoundError:
        d = {}
    for key, value in d.items():
        x_values = []
        y_values = []
        data = value["data"]
        for x,y in data.items():
            x_values.append(x)
            y_values.append(y)
        all_lines.append((x_values, y_values))

    return all_lines


stuff = read()
for i in stuff:
    plt.plot(i[0], i[1])

plt.xticks(range(0, 162, 10))
plt.xlabel("time")
plt.yticks(range(0, 401, 100))
plt.ylabel("count")
plt.show()