import json
import matplotlib.pyplot as plt

def read():
    """ Returns all_prey_lines and all_predator_lines --> need to be added tho"""
    all_prey_lines = []
    all_predator_lines = []
    try:
        with open("logs/pvp.json", "r") as f:
            d = json.load(f)
    except FileNotFoundError:
        d = {}
    for key, value in d.items():
        prey_x_values = []
        prey_y_values = []
        predator_x_values = []
        predator_y_values = []
        prey_data = value["prey_data"]
        predator_data = value["predator_data"]
        for x,y in prey_data.items():
            prey_x_values.append(x)
            prey_y_values.append(y)
        for x,y in predator_data.items():
            predator_x_values.append(x)
            predator_y_values.append(y)
        all_prey_lines.append((prey_x_values, prey_y_values))
        all_predator_lines.append((predator_x_values, predator_y_values))

    return all_prey_lines, all_predator_lines

def avg_list_value(list_of_lists: list) -> list:
    """Every list in the given list is equally long"""
    sum_list = [0 for _ in range(max([len(i) for i in list_of_lists]))]
    divisor = len(list_of_lists)
    for sublist in list_of_lists:
        for i in range(len(sublist)):
            sum_list[i] += sublist[i]
    for i in range(len(sum_list)):
        sum_list[i] /= divisor
    return sum_list
        


fig, (ax1, ax2) = plt.subplots(2,1)



stuff1, stuff2 = read()
a = 255
for i in stuff1:
    ax1.plot(i[0], i[1], "#00" + hex(a)[-2:] + "00")
    a -= 25
a = 255
for i in stuff2:
    ax1.plot(i[0], i[1], "#" + hex(a)[-2:] + "0000")
    a -= 25


all_values_1 = []
all_values_total = []
for i in stuff1:
    all_values_1.append(i[1])

for i in range(len(stuff1)):
    all_values_total.append([])
    for j in range(len(stuff1[i][1])):
        all_values_total[i].append(stuff1[i][1][j] + stuff2[i][1][j])

ax2.plot(avg_list_value(all_values_1))
ax2.plot(avg_list_value(all_values_total))


plt.xlabel("time")
plt.ylabel("count")
plt.show()