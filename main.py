import random

class Coin:
    def __init__(self, x, y, value = 10):
        self.center_x = x
        self.center_y = y
        self.value = value


class Character:
    def __init__(self, started_x, started_y, speed = 0, change_x = 0, change_y = 0):
        self.center_x = started_x
        self.center_y = started_y
        self.speed = speed
        self.change_x = change_x
        self.change_y = change_y


class Player(Character):
    def __init__(self, started_x, started_y):
        super().__init__(started_x, started_y)
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Enemy(Character):
    def __init__(self, started_x, started_y):
        super().__init__(started_x, started_y)
        self.time_to_change_direction = 0

    def pick_new_direction(self):
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        fate = random.choice(movements)
        self.change_x = fate[0]
        self.change_y = fate[1]
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self,  delta_time = 1/60):
        if self.time_to_change_direction == 0:
            self.pick_new_direction()
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
        self.time_to_change_direction -= delta_time


class Wall:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y




