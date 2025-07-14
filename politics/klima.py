from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import random as r
from help import plot_colored_line

class Date:
    def __init__(self, year: int, month: int = 0, day: int = 0, time: int = 0):
        self.day = day
        self.month = month
        self.year = year
        self.time = time

    def __str__(self) -> str:
        return f"{self.time:02}.{self.day:02}.{self.month:02}.{self.year}"
    
def datify(date:int) -> Date:
    year = int(str(date)[0:4])
    if len(str(date))  == 4:
        return Date(year)
    month = int(str(date)[4:6])
    if len(str(date)) == 6:
        return Date(year, month)
    day = int(str(date)[6:8])
    if len(str(date)) == 8:
        return Date(year, month, day)
    time = int(str(date)[8:10])
    if len(str(date)) == 10:
        return Date(year, month, day, time)
    raise ValueError("Invalid date format")

def undatify(date: Date) -> int:
    return int(f"{date.year}{date.month:02}{date.day:02}{date.time:02}")

class Entry:
    def __init__(self, id, date, qn, tt, rf):
        self.id = id
        self.intdate = date
        self.date = datify(date)
        self.qn = qn
        self.tt = tt
        self.rf = rf

def list_avg_day(data: list[Entry]) -> list[Entry]:
    avg_data = []
    current_date = data[0].date
    current_data = []
    current_id = 0
    for entry in data:
        if entry.date.year == current_date.year and entry.date.month == current_date.month and entry.date.day == current_date.day:
            current_data.append(entry)
        else:
            if current_data:
                avg_tt = sum(e.tt for e in current_data) / len(current_data)
                avg_rf = sum(e.rf for e in current_data) / len(current_data)
                current_id += 1
                avg_entry = Entry(current_id, undatify(current_date), current_data[0].qn, avg_tt, avg_rf)
                avg_data.append(avg_entry)
            current_date = entry.date
            current_data = [entry]
    return avg_data

def list_avg_month(data: list[Entry]) -> list[Entry]:
    avg_data = []
    current_date = data[0].date
    current_data = []
    current_id = 0
    for entry in data:
        if entry.date.year == current_date.year and entry.date.month == current_date.month:
            current_data.append(entry)
        else:
            if current_data:
                avg_tt = sum(e.tt for e in current_data) / len(current_data)
                avg_rf = sum(e.rf for e in current_data) / len(current_data)
                current_id += 1
                avg_entry = Entry(current_id, undatify(current_date), current_data[0].qn, avg_tt, avg_rf)
                avg_data.append(avg_entry)
            current_date = entry.date
            current_data = [entry]
    return avg_data

def open_climate_data(filename: str) -> list[Entry]:
    with open("kilma/" + filename, 'r') as file:
        lines = file.readlines()
    entries = []
    id = 0
    for line in lines[1:]:
        parts = line.split(";")
        if len(parts) < 4:
            continue  # Skip malformed lines
        id += 1
        date = parts[1]
        qn = int(parts[2])
        tt = float(parts[3])
        if tt < -100:
            print(f"Invalid temperature value: {tt} in line: {id}")
        rf = float(parts[4])
        entries.append(Entry(id, date, qn, tt, rf))
    return entries




def plot_yearly():
    flughafen = open_climate_data('flughafen.txt')
    stadt = open_climate_data('stadt.txt')

    flughafen = flughafen

    fig, axes = plt.subplots(3, 2)
    axes = axes.flatten()
    tt, rf, att, arf, mtt, mrf = axes.flatten()
    tt.set_title('Temperatur')
    tt.set_xlabel('Datum')
    tt.set_ylabel('Temperatur in °C')
    #tt.xaxis.set_major_locator(plticker.MultipleLocator(66))

    rf.set_title('Niederschlag')
    rf.set_xlabel('Datum')
    rf.set_ylabel('Niederschlag in mm')
    #rf.xaxis.set_major_locator(plticker.MultipleLocator(66))

    plot_colored_line(tt, flughafen, 'id', 'tt', label='Temperatur')
    plot_colored_line(rf, flughafen, 'id', 'rf', label='Niederschlag', cmap_name='Blues')
    #plot_colored_line(tt, stadt, 'id', 'tt', label='Temperatur')
    #plot_colored_line(rf, stadt, 'id', 'rf', label='Niederschlag', cmap_name='Blues')
    #
    avg_day_flughafen = list_avg_day(flughafen)

    plot_colored_line(att, avg_day_flughafen, 'id', 'tt', label='Tagesdurchschnitt')
    plot_colored_line(arf, avg_day_flughafen, 'id', 'rf', label='Tagesdurchschnitt', cmap_name='Blues')
    
    month_flughafen = list_avg_month(avg_day_flughafen)
    plot_colored_line(mtt, month_flughafen, 'id', 'tt', label='Monatsdurchschnitt')
    plot_colored_line(mrf, month_flughafen, 'id', 'rf', label='Monatsdurchschnitt', cmap_name='Blues')
    plt.tight_layout()
    plt.show()

plot_yearly()