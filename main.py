import random

class Coin:
    def __init__(self, x, y, value = 10):
        self.center_x = x
        self.center_y = y
        self.value = value


class Character:
    def __init__(self, started_x, started_y, speed, change_x = 0, change_y = 0):
        self.center_x = started_x
        self.center_y =started_y
        self.speed = speed
        self.change_x = change_x
        self.change_y = change_y


class Player(Character):
    def __init__(self, started_x, started_y, speed):
        super().__init__(started_x, started_y, speed)
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

class Enemy(Character):
    def __init__(self, started_x, started_y, speed):
        super().__init__(started_x, started_y, speed)
        self.time_to_change_direction = 0

    def pick_new_direction(self):
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        self.change_x = random.choice(movements)
        self.change_y = random.choice(movements)
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self,  delta_time = 1/60):



class Wall:
    def __init__(self):