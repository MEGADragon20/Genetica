"""
Genetic heritance of speed and precision

"""
energie = 500 # energy count
START_BLOBS = 80
START_FOODS = 100

import arcade
import random
import math
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import time
import json

# chart setup
plt.axis([0, 2, 0, 100])

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')
ax1.set(ylabel="Count")
ax2.set(ylabel="Count")




def make_position():
    a = random.randint(1, 4)
    if a == 1:
        return (random.randint(0, 800), 0, 0)
    if a == 2:
        return (0, random.randint(0, 800), 90)
    if a == 3:
        return (800, random.randint(0, 800), 180)
    if a == 4:
        return (random.randint(0, 800), 800, 270)

def mutate(value):
    a = value + (random.randint(-2, 2) / 10)
    return a

def mutate_colour(colour):
    colours = [colour]+["red", "blue"]
    weights = [0.9, 0.05, 0.05]
    return random.choices(colours, weights)[0]

def check_if_potential_partner(blob1, blob2):
    delta_speed = abs(blob1.speed - blob2.speed)
    delta_precision = abs(blob1.precision - blob2.precision)
    if (delta_speed + delta_precision)/2 > 1:
        return False
    return True


def reproduce(blob1, blob2):
    bgenes1 = blob1.binary_genes
    bgenes2 = blob2.binary_genes
    dgenes1 = blob1.decimal_genes
    dgenes2 = blob2.decimal_genes

    bgenes0 = {} # binarygenes of offspring eg. red or blue  
    dgenes0 = {} # decimal genes of offspring eg. speed, size

    for i in bgenes1:
        bgenes0[i] = mutate_colour(random.choice([bgenes1[i], bgenes2[i]]))
    
    for i in dgenes1:
        dgenes0[i] = mutate(random.choice([dgenes1[i], dgenes2[i]]))
                            
    return Blob(make_position(), bgenes0, dgenes0, blob1.foods, blob1.blobs)






class Screen(arcade.Window):
    def __init__(self, start_blobs, start_foods):
        super().__init__(width=800, height=800, title="Experiment", resizable=True)
        self.blobs = arcade.SpriteList()
        self.foods = arcade.SpriteList()
        self.playing = False

        self.start_blobs = start_blobs
        self.start_foods = start_foods

        self.speed_data = []
        self.precision_data = []
        self.number_of_blobs = [[],[]]
        self.number_of_blobs_counter = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.close()
    def setup(self):
        arcade.set_background_color(arcade.color.GRANNY_SMITH_APPLE)
        for _ in range(self.start_blobs):  
            position = make_position()
            blob_decimal_genes = {
                "speed": 1,
                "precision": 1
            }
            blob_binary_genes = {
                "colour": "red"
            }
            blob = Blob(position, blob_binary_genes, blob_decimal_genes, self.foods, self.blobs)
            blob.energy = energie
            self.blobs.append(blob)
        self.counter = time.time()
        self.setup_foods()
    def setup_foods(self):
        for _ in range(self.start_foods):
            food = arcade.Sprite(filename="data/food.png", center_x=random.randint(20, 780), center_y=random.randint(20, 780))
            self.foods.append(food)

    def on_draw(self):
        self.clear()
        self.blobs.draw()
        self.foods.draw()

    def on_update(self, delta_time):
        if True:
            self.blobs.on_update(delta_time)
        for i in self.blobs:
            if i.energy <= 0:
                i.kill()
                print(len(self.blobs))

        if time.time() - self.counter > 1:
            # append graph
            ty = {round(x, 1): 0 for x in [i / 10 for i in range(1, 30)]}
            py = {round(x, 1): 0 for x in [i / 10 for i in range(1, 30)]}

            for i in self.blobs:
                for value in ty.keys():
                    if value <= i.speed < value + 0.01:
                        ty[value] += 1

                for value in py.keys():
                    if value <= i.precision < value + 0.01:
                        py[value] += 1

            tx = list(ty.keys())
            ty_values = list(ty.values())
            px = list(py.keys())
            py_values = list(py.values())

            self.speed_data.append([tx, ty_values])
            self.precision_data.append([px, py_values])
            self.number_of_blobs[0].append(self.number_of_blobs_counter)
            self.number_of_blobs[1].append(len(self.blobs))
            self.number_of_blobs_counter += 1
            self.counter = time.time()
        while len(self.foods) < 100:
            self.foods.append(arcade.Sprite("data/food.png", center_x=random.randint(20, 780), center_y=random.randint(20, 780)))
        


class Blob(arcade.Sprite):
    def __init__(self, position, binary_genes, decimal_genes, foods, blobs):
        super().__init__("data/blob.png", scale=1)
        self.position = position
        self.center_x = position[0] 
        self.center_y = position[1]
        self.direction = position[2]
        self.energy = 0
        self.speed = decimal_genes["speed"] # value for speed
        self.precision = decimal_genes["precision"] # ""__"" precision
        colour = binary_genes["colour"]
        self.texture = arcade.load_texture("data/" + colour + ".png")
        self.binary_genes = binary_genes
        self.decimal_genes = decimal_genes
        self.foods = foods
        self.blobs = blobs
        self.last_reproduction_time = time.time()
    def duplicate(self):
        new_speed = mutate(self.speed)
        new_precision = mutate(self.precision)
        new_blob = Blob(make_position(), self.foods, new_speed, new_precision)
        return new_blob


    def move_around(self):
        # Change the angle slightly
        self.direction += random.uniform(-(10**self.precision), 10**self.precision)
        self.direction %= 360 

        # Convert angle to radians
        angle_rad = math.radians(self.direction)

        # Calculate movement
        self.center_x += math.cos(angle_rad) * self.speed
        self.center_y += math.sin(angle_rad) * self.speed

        # Check boundaries and bounce
        if self.center_x < 0 or self.center_x > 800:
            self.direction = (180 - self.direction) % 360
            self.center_x = max(0, min(800, self.center_x))

        if self.center_y < 0 or self.center_y > 800:
            self.direction = (-self.direction) % 360
            self.center_y = max(0, min(800, self.center_y))



    def on_update(self, delta_time=1 / 60):
        if self.energy >= 0:
            self.move_around()
            self.energy -= self.speed
            for i in self.foods:
                if arcade.check_for_collision(self, i):
                    self.foods.remove(i)
                    self.energy += 100
            for i in self.blobs:
                if self != i and arcade.check_for_collision(self, i):
                    if check_if_potential_partner(self, i) and time.time() - self.last_reproduction_time >= 5 and self.energy >= 150 and i.energy >= 150:
                        new_blob = reproduce(self, i)
                        new_blob.energy = 500
                        self.blobs.append(new_blob)
                        print(len(self.blobs))
                        i.energy -= 150
                        self.energy -= 150
                        self.last_reproduction_time = time.time()

def add_log_entry(data, screen):
    entry = {}
    entry["start_blobs"] = screen.start_blobs
    entry["start_foods"] = screen.start_foods
    entry["data"] = {}
    for i in range(len(data[0])):
        entry["data"][data[0][i]] = data[1][i]
    
    try:
        with open("logs/sexual_reproduction.json", "r") as f:
            a = json.load(f)
    except FileNotFoundError:
        a = {}
    
    a[time.time()] = entry
    
    with open("logs/sexual_reproduction.json", "w") as f:
        json.dump(a, f, indent=4)


# Main code to run the simulation
def main():
    screen = Screen(START_BLOBS, START_FOODS)
    screen.setup()
    arcade.run()

    sd = screen.speed_data 
    pd = screen.precision_data
    nob = screen.number_of_blobs
    ax2.plot(nob[0], nob[1], color = "#273175")
    add_log_entry(nob, screen)


    for i in range(5):
        for i in range(len(sd)):
            ax1.clear()
            ax1.plot(sd[i][0], sd[i][1], color = "red")
            ax1.plot(pd[i][0], pd[i][1], color = "green")
            plt.pause(1)

if __name__ == "__main__":
    main()