"""
Normal iteration of the project

"""
energie = 800


import arcade
import random
import math

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



class Screen(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width=width, height=height, title="Experiment")
        self.blobs = arcade.SpriteList()
        self.foods = arcade.SpriteList()
        self.playing = False

    def setup(self):
        arcade.set_background_color(arcade.color.GRANNY_SMITH_APPLE)
        for _ in range(100):  
            position = make_position()
            blob = Blob(position, self.foods)
            self.blobs.append(blob)
    def setup_foods(self):
        for _ in range(100):
            food = arcade.Sprite(filename="data/food.png", center_x=random.randint(20, 780), center_y=random.randint(20, 780))
            self.foods.append(food)

    def on_draw(self):
        self.clear()
        self.blobs.draw()
        self.foods.draw()

    def on_update(self, delta_time):
        if self.playing == True:
            self.blobs.on_update(delta_time)
            energy_sum = 0
            for i in self.blobs:
                i.energy -= 1
                energy_sum += i.energy
        
            if energy_sum < 0:
                self.playing = False
                for i in self.blobs:
                    if i.food == 0:
                        self.blobs.remove(i)
                    elif i.food >= 2:        
                        self.blobs.append(i.duplicate())
                    i.food = 0
                self.playing = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.playing == False:
            print("count: ",len(self.blobs))
            self.playing = True
            self.setup_foods()
            for blob in self.blobs:
                blob.energy = energie
                blob.foods = self.foods

        


class Blob(arcade.Sprite):
    def __init__(self, position, foods):
        super().__init__("data/blob.png", scale=1)
        self.center_x = position[0]
        self.center_y = position[1]
        self.direction = position[2]
        self.energy = 0
        self.last_food = 1
        self.food = 0
        self.foods = foods

    def duplicate(self):
            return Blob(make_position(), self.foods)


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
        if self.center_x < 0 or self.center_x > 800:
            self.direction = (180 - self.direction) % 360
            self.center_x = max(0, min(800, self.center_x))

        if self.center_y < 0 or self.center_y > 800:
            self.direction = (-self.direction) % 360
            self.center_y = max(0, min(800, self.center_y))



    def on_update(self, delta_time=1 / 60):
        if self.energy >= 0:
            self.move_around()
            for i in self.foods:
                if arcade.check_for_collision(self, i):
                    self.foods.remove(i)
                    self.food += 1


# Main code to run the simulation
def main():
    screen = Screen(800, 800)
    screen.setup()
    arcade.run()


if __name__ == "__main__":
    main()
