import random


class Wand:

    # All wands will have 3 params. Change out of 100 to go off, a low number and a high number for range
    def __init__(self, chance, low, high):
        self.chance = chance
        self.low = low
        self.high = high

    def roll(self):
        rand = random.random() * 100
        return rand < self.chance

    def get_points(self):
        return random.randint(self.low, self.high)

