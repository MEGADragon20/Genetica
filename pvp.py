# predator system

START_ENERGY = 500
START_PREDATORS = 20
START_PREYS = 75
START_FOODS = 75
WIDTH = 600
HEIGHT = 600

import arcade
import random
import math
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import time
import json

#chart setup

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')
ax1.set(ylabel="Count")
ax2.set(ylabel="Count")




def make_position():
    a = random.randint(1, 4)
    if a == 1:
        return (random.randint(0, WIDTH), 0, 0)
    if a == 2:
        return (0, random.randint(0, HEIGHT), 90)
    if a == 3:
        return (WIDTH, random.randint(0, HEIGHT), 180)
    if a == 4:
        return (random.randint(0, WIDTH), 800, 270)


def reproduce_prey(prey1, prey2):
    return Prey(make_position(), prey1.foods, prey1.preys)

def reproduce_predator(predator1, predator2):
    return Predator(make_position(), predator1.preys, predator1.predators)






class Screen(arcade.Window):
    def __init__(self, start_predators, start_preys, start_foods):
        super().__init__(width=WIDTH, height=HEIGHT, title="Experiment", resizable=True)
        self.predators = arcade.SpriteList()
        self.preys = arcade.SpriteList()
        self.foods = arcade.SpriteList()

        self.start_predators = start_predators
        self.start_preys = start_preys
        self.start_foods = start_foods

        self.number_of_predators = [[],[]]
        self.number_of_preys = [[],[]] 
        self.number_of_blobs_counter = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.close()
    def setup(self):
        arcade.set_background_color(arcade.color.FOREST_GREEN)
        for _ in range(self.start_predators):
            predator = Predator(make_position(), self.preys, self.predators)
            predator.energy = START_ENERGY
            self.predators.append(predator)
        for _ in range(self.start_preys):
            prey = Prey(make_position(), self.foods, self.preys)
            prey.energy = START_ENERGY
            self.preys.append(prey)
        self.counter = time.time()
        self.setup_foods()

    def setup_foods(self):
        for _ in range(self.start_foods):
            food = arcade.Sprite(filename="data/food.png", center_x=random.randint(20, WIDTH - 20), center_y=random.randint(20, HEIGHT - 20))
            self.foods.append(food)

    def on_draw(self):
        self.clear()
        self.predators.draw()
        self.preys.draw()
        self.foods.draw()

    def on_update(self, delta_time):
        if True:
            self.preys.on_update(delta_time)
            self.predators.on_update(delta_time)
        for i in self.predators:
            if i.energy <= 0:
                i.kill()
                print("F: ", len(self.predators))
        for i in self.preys:
            if i.energy <= 0:
                i.kill()
                print("Y: ", len(self.preys))

        if time.time() - self.counter > 1:
            # append graph

            self.number_of_preys[0].append(self.number_of_blobs_counter)
            self.number_of_preys[1].append(len(self.preys))
            self.number_of_predators[0].append(self.number_of_blobs_counter)
            self.number_of_predators[1].append(len(self.predators))
            self.number_of_blobs_counter += 1
            self.counter = time.time()
        while len(self.foods) < self.start_foods:
            self.foods.append(arcade.Sprite("data/food.png", center_x=random.randint(20, WIDTH - 20), center_y=random.randint(20, HEIGHT - 20)))
        


class Prey(arcade.Sprite):
    def __init__(self, position, foods, preys):
        super().__init__("data/blue.png", scale=0.8)
        self.position = position
        self.center_x = position[0]
        self.center_y = position[1]
        self.direction = position[2]
        self.energy = 0
        self.foods = foods
        self.preys = preys
        self.last_reproduction_time = time.time()


    def move_around(self):
        # Change the angle slightly
        self.direction += random.uniform(-10, 10)
        self.direction %= 360 

        # Convert angle to radians
        angle_rad = math.radians(self.direction)

        # Calculate movement
        self.center_x += math.cos(angle_rad)
        self.center_y += math.sin(angle_rad)

        # Check boundaries and bounce
        if self.center_x < 0 or self.center_x > WIDTH:
            self.direction = (180 - self.direction) % 360
            self.center_x = max(0, min(WIDTH, self.center_x))

        if self.center_y < 0 or self.center_y > HEIGHT:
            self.direction = (-self.direction) % 360
            self.center_y = max(0, min(HEIGHT, self.center_y))



    def on_update(self, delta_time=1 / 60):
        if self.energy >= 0:
            self.move_around()
            self.energy -= 1
            for i in self.foods:
                if arcade.check_for_collision(self, i):
                    self.foods.remove(i)
                    self.energy += 100
            for i in self.preys:
                if self != i and arcade.check_for_collision(self, i):
                    if time.time() - self.last_reproduction_time >= 5 and self.energy >= 150 and i.energy >= 150:
                        new_prey = reproduce_prey(self, i)
                        new_prey.energy = 500
                        self.preys.append(new_prey)
                        print("Y: ", len(self.preys))
                        i.energy -= 150
                        self.energy -= 150
                        self.last_reproduction_time = time.time()

class Predator(arcade.Sprite):
    def __init__(self, position, preys, predators):
        super().__init__("data/red.png", scale=1.2)
        self.position = position
        self.center_x = position[0]
        self.center_y = position[1]
        self.direction = position[2]
        self.energy = 0
        self.preys = preys
        self.predators = predators
        self.last_reproduction_time = time.time()


    def move_around(self):
        # Change the angle slightly
        self.direction += random.uniform(-10, 10)
        self.direction %= 360 

        # Convert angle to radians
        angle_rad = math.radians(self.direction)

        # Calculate movement
        self.center_x += math.cos(angle_rad)
        self.center_y += math.sin(angle_rad)

        # Check boundaries and bounce
        if self.center_x < 0 or self.center_x > WIDTH:
            self.direction = (180 - self.direction) % 360
            self.center_x = max(0, min(WIDTH, self.center_x))

        if self.center_y < 0 or self.center_y > HEIGHT:
            self.direction = (-self.direction) % 360
            self.center_y = max(0, min(HEIGHT, self.center_y))



    def on_update(self, delta_time=1 / 60):
        if self.energy >= 0:
            self.move_around()
            self.energy -= 1
            for i in self.preys:
                if arcade.check_for_collision(self, i):
                    self.preys.remove(i)
                    self.energy += 100
            for i in self.predators:
                if self != i and arcade.check_for_collision(self, i):
                    if time.time() - self.last_reproduction_time >= 5 and self.energy >= 150 and i.energy >= 150:
                        new_predator = reproduce_predator(self, i)
                        new_predator.energy = 500
                        self.predators.append(new_predator)
                        print("F: ", len(self.predators))
                        i.energy -= 150
                        self.energy -= 150
                        self.last_reproduction_time = time.time()

def add_log_entry(prey_data, predator_data, screen):
    entry = {}
    entry["start_predators"] = screen.start_predators
    entry["start_preys"] = screen.start_preys
    entry["start_foods"] = screen.start_foods
    entry["prey_data"] = {}
    entry["predator_data"] = {}
    for i in range(len(prey_data[0])):
        entry["prey_data"][prey_data[0][i]] = prey_data[1][i]
        entry["predator_data"][predator_data[0][i]] = predator_data[1][i]

    
    try:
        with open("logs/pvp.json", "r") as f:
            a = json.load(f)
    except FileNotFoundError:
        a = {}
    
    a[time.time()] = entry
    
    with open("logs/pvp.json", "w") as f:
        json.dump(a, f, indent=4)


# Main code to run the simulation
def main():
    screen = Screen(START_PREDATORS, START_PREYS, START_FOODS)
    screen.setup()
    arcade.run()

    prey_d = screen.number_of_preys
    for i in range(40-len(prey_d[0])):
        prey_d[0].append(len(prey_d) + i)
        prey_d[1].append(0)
    predator_d = screen.number_of_predators
    for i in range(40-len(predator_d[0])):
        predator_d[0].append(len(predator_d) + i)
        predator_d[1].append(0)
    ax1.plot(prey_d[0], prey_d[1], color = "#3D55A4")
    ax2.plot(predator_d[0], predator_d[1], color = "#C43D59")
    add_log_entry(prey_d, predator_d, screen)

if __name__ == "__main__":
    main()