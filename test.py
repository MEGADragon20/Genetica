import random 

def mutate_colour(colour):
    colours = [colour]+["red", "blue"]
    weights = [0.9, 0.05, 0.05]
    return random.choices(colours, weights)

for i in range(100):
    print(mutate_colour("red"))