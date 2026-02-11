import random
import arcade


TILE_SIZE = 32

class Coin(arcade.Sprite):
    def __init__(self, x, y, value = 10):
        super().__init__()
        radius = TILE_SIZE // 8
        texture = arcade.make_circle_texture(radius * 2, arcade.color.GOLDEN_YELLOW)
        self.texture = texture
        self.width = texture.width
        self.height = texture.height
        self.center_x = x
        self.center_y = y
        self.value = value


class Character (arcade.Sprite):
    def __init__(self, started_x, started_y, speed = 0, change_x = 0, change_y = 0, color = arcade.color.YELLOW):
        super().__init__()
        radius = TILE_SIZE // 2 - 2
        texture = arcade.make_circle_texture(radius * 2, color)
        self.texture = texture
        self.center_x = started_x
        self.center_y = started_y
        self.speed = speed
        self.width = texture.width
        self.height = texture.height
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
    def __init__(self, started_x, started_y, color = arcade.color.RED):
        super().__init__(started_x, started_y, color)

        self.time_to_change_direction = 0

    def pick_new_direction(self):
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        fate = random.choice(movements)
        self.change_x = fate[0]
        self.change_y = fate[1]
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self, delta_time = 1/60):
        if self.time_to_change_direction == 0:
            self.pick_new_direction()
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
        self.time_to_change_direction -= delta_time


class Wall(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        radius = TILE_SIZE
        texture = arcade.make_soft_square_texture(center_x,center_y , radius , arcade.color.BLUE)
        self.width = texture.width
        self.height = texture.height
        self.texture = texture
        self.center_x = center_x
        self.center_y = center_y


class PacmanGame:
    def __init__(self):
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player = None
        self.game_over = False
        self.background_color = arcade.color.BLACK
        self.start_x = 0
        self.start_y = 0

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.game_over = False
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (row - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2
                if LEVEL_MAP[x, y] is wall:
                    self.wall_list.append((x, y))

                elif LEVEL_MAP[x, y] is coin:
                    self.coin_list.append((x, y))

                elif LEVEL_MAP[x, y] is ghost:
                    self.ghost_list.append((x, y))

                elif LEVEL_MAP[x, y] is player:
                    self.player_list.append((x, y))

    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()

        arcade.draw_text(
            f"Score: {self.player.score}",
            10, self.player.height - 30,
            arcade.color.WHITE, 16
        )

        arcade.draw_text(
            f"Lives: {self.player.lives}",
            10, self.player.height - 55,
            arcade.color.WHITE, 16
        )

        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                self.player.width // 2,
                self.player.height // 2,
                arcade.color.RED,
                40,
                anchor_x="center",
                anchor_y="center"
            )

    def on_key_press(self, key, modifiers):
        """
        מטפלת בלחיצות מקשים מהמקלדת.

        המתודה מגיבה לקלט של המשתמש בהתאם למצב המשחק:
        - במצב הפסד: לחיצה על מקש SPACE מאתחלת את המשחק מחדש.
        - בזמן משחק פעיל: חיצי המקלדת משנים את כיוון התנועה של השחקן.

        :param key: המקש שנלחץ (קבוע מתוך arcade.key)
        :param modifiers: מקשי עזר שנלחצו יחד עם המקש (Shift, Ctrl וכו')
        :return: None
        """

        # מצב הפסד – אתחול מחדש

        if self.game_over:
            # אם המשחק נגמר, רק SPACE פעיל לצורך התחלה מחדש
            if key == arcade.key.SPACE:
                self.setup()
            return  # מונע המשך טיפול במקשים אחרים

        # משחק פעיל – שליטה בשחקן

        # חץ למעלה – תנועה למעלה (ציר Y חיובי)
        if key == arcade.key.UP:
            self.player.change_y = 1
            self.player.change_x = 0  # מבטיח תנועה בציר אחד בלבד

        # חץ למטה – תנועה למטה (ציר Y שלילי)
        elif key == arcade.key.DOWN:
            self.player.change_y = -1
            self.player.change_x = 0

        # חץ שמאלה – תנועה שמאלה (ציר X שלילי)
        elif key == arcade.key.LEFT:
            self.player.change_x = -1
            self.player.change_y = 0

        # חץ ימינה – תנועה ימינה (ציר X חיובי)
        elif key == arcade.key.RIGHT: 
            self.player.change_x = 1
            self.player.change_y = 0

    def on_update(self, delta_time):
        if self.game_over:
            return "GAME OVER"
        maccabi_x = self.center_x
        maccabi_y = self.center_y
        self.player.move()
        player_wall_collision = arcade.check_for_collision_with_list(self.wall_list, self.player)
        if len(player_wall_collision) > 0:
            self.center_y = maccabi_y
            self.center_x = maccabi_x

        for ghost in self.ghost_list:
            hapoel_x = self.ghost.center_x
            hapoel_y = self.ghost.center_y
            self.enemy.pick_new_direction()
            self.enemy.move()
            ghost_wall_collision = arcade.check_for_collision_with_list(self.wall_list, ghost)
            if len(ghost_wall_collision) > 0:
                while True:
                    self.ghost.center_y = hapoel_y
                    self.ghost.center_x = hapoel_x
                    self.enemy.pick_new_direction()
                    self.enemy.move()
                    ghost_wall_collision = arcade.check_for_collision_with_list(self.wall_list,
                                                                                ghost)
                    if len(ghost_wall_collision) == 0:
                        break
        player_coin_collision = arcade.check_for_collision_with_list(self.coin_list, self.player)
        for coin in player_coin_collision:
            self.player.score += coin.value
            self.coin_list.remove(coin)







