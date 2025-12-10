class Coin:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.value = 10


class Character:
    def __init__(self, started_x, started_y, speed):
        self.center_x = started_x
        self.center_y =started_y
        self.speed = speed
        self.change_x = 0
        self.change_y = 0


class Player(Character):
    def __init__(self, started_x, started_y, speed):
        super().__init__(started_x, started_y, speed)
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x = self.change_x * self.speed
        self.center_y = self.change_y * self.speed

class Enemy(Character):
    def __init__(self, started_x, started_y, speed):
        super().__init__(started_x, started_y, speed)
