"""
Genetic heritance of speed and precision

"""
energie = 500 # energy count

import arcade
import random
import math
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import time

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


def check_if_potential_partner(blob1, blob2):
    delta_speed = abs(blob1.speed - blob2.speed)
    delta_precision = abs(blob1.precision - blob2.precision)
    if (delta_speed + delta_precision)/2 > 1:
        return False
    return True


def reproduce(blob1, blob2):
    print("reproducing")
    genes1 = blob1.genes
    genes2 = blob2.genes

    cgenes = {} # genes of offspring 
    for gene in genes1:
        p1gene1 = genes1[gene][0]
        p1gene2 = genes1[gene][1]
        p2gene1 = genes2[gene][0]
        p2gene2 = genes2[gene][1]
        p1gene = random.choice([p1gene1, p1gene2])
        p2gene = random.choice([p2gene1, p2gene2])
        if p1gene[1] == "dom" and p2gene[1] == "dom":# check if homozygous dominant
            cgene = round((p1gene[0]+p2gene[0])/2, 1)
            cgeneallele = "dom"
        elif p1gene[1] == "dom" and p2gene[1] == "rec": # check if heterozygous case 1
            cgene = p1gene[0]
            cgeneallele = "dom"
        elif p1gene[1] == "rec" and p2gene[1] == "dom":# check if heterozygous case 2
            cgene = p2gene[0]
            cgeneallele = "dom"
        elif p1gene[1] == "rec" and p2gene[1] == "rec": # check if homozygous recessive
            cgene = round((p1gene[0]+p2gene[0])/2, 1)
            cgeneallele = "rec"
        cgenes[gene] = {0: (mutate(cgene), cgeneallele), 1: random.choice([p1gene, p2gene])}
    print(cgenes)
    return Blob(make_position(), cgenes, blob1.foods, blob1.blobs)






class Screen(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width=width, height=height, title="Experiment", resizable=True)
        self.blobs = arcade.SpriteList()
        self.foods = arcade.SpriteList()
        self.playing = False

        self.speed_data = []
        self.precision_data = []
        self.count_data = []
        self.count_data_counter = 0
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.close()
    def setup(self):
        arcade.set_background_color(arcade.color.GRANNY_SMITH_APPLE)
        for _ in range(100):  
            position = make_position()
            blob_genes = {
                "speed": {
                    0: (1, random.choice(["dom", "rec"])),
                    1: (0.8, random.choice(["dom", "rec"]))
                },
                "precision": {
                    0: (1, random.choice(["dom", "rec"])),
                    1: (0.8, random.choice(["dom", "rec"]))
                }
            }
            blob = Blob(position, blob_genes, self.foods, self.blobs)
            blob.energy = energie
            self.blobs.append(blob)
        self.counter = time.time()
        self.setup_foods()
    def setup_foods(self):
        for _ in range(100):
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
                self.count_data.append((self.count_data_counter, len(self.blobs)))
                self.count_data_counter += 1

        if self.counter - time.time() > 5:
            print("new")
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
                
                            
            # setup()
            self.setup_foods()
            for blob in self.blobs:
                blob.energy = energie
                blob.foods = self.foods
            self.counter = time.time()
        while len(self.foods) < 100:
            self.foods.append(arcade.Sprite("data/food.png", center_x=random.randint(20, 780), center_y=random.randint(20, 780)))
        


class Blob(arcade.Sprite):
    def __init__(self, position, genes, foods, blobs):
        super().__init__("data/blob.png", scale=1)
        self.position = position
        self.center_x = position[0] 
        self.center_y = position[1]
        self.direction = position[2]
        self.energy = 0
        self.speed = genes["speed"][0][0] # value for speed
        self.precision = genes["precision"][0][0] # ""__""
        self.genes = genes
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
                    self.energy += 110
            for i in self.blobs:
                if self != i and arcade.check_for_collision(self, i):
                    if check_if_potential_partner(self, i) and time.time() - self.last_reproduction_time >= 5 and self.energy >= 400 and i.energy >= 400:
                        new_blob = reproduce(self, i)
                        new_blob.energy = 300
                        self.energy -= 200
                        i.energy -= 200
                        self.blobs.append(new_blob)
                        print(len(self.blobs))
                        self.last_reproduction_time = time.time()


# Main code to run the simulation
def main():
    screen = Screen(800, 800)
    screen.setup()
    arcade.run()

    sd = screen.speed_data 
    pd = screen.precision_data
    for i in range(5):
        for i in range(len(sd)):
            ax1.clear()
            ax2.clear()
            ax1.plot(sd[i][0], sd[i][1], color = "red")
            ax2.plot(pd[i][0], pd[i][1], color = "green")
            plt.pause(1)


if __name__ == "__main__":
    main()