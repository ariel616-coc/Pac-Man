import random
import arcade
import math

LEVEL_MAP = [
    "############A############",
    "#.......................#",
    "#.###.#.##.###.##.#.###.#",
    "#.###.#.##.###.##.#.###.#",
    "#.....#...........#.....#",
    "#.###.###.#####.###.###.#",
    "#.###.###.#####.###.###.#",
    "E.......#...#...#.......T",
    "####.####G..#..G####.####",
    "####.####G..#..G####.####",
    "T.......#...#...#.......E",
    "#.###.###.#####.###.###.#",
    "#.###.###.#####.###.###.#",
    "#N...N#...........#.....#",
    "#.###.#.##.###.##.#.###.#",
    "#.###.#.##.###.##.#.###.#",
    "#P...N..................#",
    "############A############"
]

TILE_SIZE = 32
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "THE YELLOW MAN"


class Coin(arcade.Sprite):
    def __init__(self, x, y, value=10):
        super().__init__()
        radius = TILE_SIZE // 8
        self.texture = arcade.make_circle_texture(radius * 2, arcade.color.GOLDEN_YELLOW)
        self.center_x = x
        self.center_y = y
        self.value = value


class Character(arcade.Sprite):
    def __init__(self, started_x, started_y, speed, color, radius):
        super().__init__()
        self.texture = arcade.make_circle_texture(radius * 2, color)
        self.center_x = started_x
        self.center_y = started_y
        self.speed = speed
        self.radius = radius
        self.change_x = 0
        self.change_y = 0
        self.teleport_cooldown = 0

    def move(self, delta_time):
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= delta_time

        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

        # --- מניעת בריחה מהמפה ---
        if self.left < 0:
            self.left = 0
        elif self.right > WINDOW_WIDTH:
            self.right = WINDOW_WIDTH

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > WINDOW_HEIGHT:
            self.top = WINDOW_HEIGHT


class Player(Character):
    def __init__(self, started_x, started_y, speed=3, color=arcade.color.YELLOW, radius=TILE_SIZE // 2 - 5):
        super().__init__(started_x, started_y, speed, color, radius)
        self.score = 0
        self.lives = 3
        self.started_x = started_x
        self.started_y = started_y
        self.mouth_angle = 10
        self.mouth_speed = 4
        self.mouth_dir = 1

    def animate(self):
        self.mouth_angle += self.mouth_speed * self.mouth_dir
        if self.mouth_angle > 40 or self.mouth_angle < 5:
            self.mouth_dir *= -1

    def draw_custom(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius + 6, (255, 255, 0, 60))
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, arcade.color.YELLOW)
        arcade.draw_circle_outline(self.center_x, self.center_y, self.radius, arcade.color.ORANGE, 3)

        direction_angle = 0
        if self.change_x > 0:
            direction_angle = 0
        elif self.change_x < 0:
            direction_angle = 180
        elif self.change_y > 0:
            direction_angle = 90
        elif self.change_y < 0:
            direction_angle = 270

        angle1 = math.radians(direction_angle + self.mouth_angle)
        angle2 = math.radians(direction_angle - self.mouth_angle)

        arcade.draw_triangle_filled(
            self.center_x, self.center_y,
            self.center_x + self.radius * math.cos(angle1), self.center_y + self.radius * math.sin(angle1),
            self.center_x + self.radius * math.cos(angle2), self.center_y + self.radius * math.sin(angle2),
            arcade.color.BLACK
        )
        eye_x = self.center_x + (self.change_x * 5)
        eye_y = self.center_y + self.radius // 3 + (self.change_y * 5)
        arcade.draw_circle_filled(eye_x, eye_y, 3, arcade.color.BLACK)


class Enemy(Character):
    def __init__(self, started_x, started_y, speed=3, color=arcade.color.RED, radius=TILE_SIZE // 2 - 2):
        super().__init__(started_x, started_y, speed, color, radius)
        self.time_to_change_direction = 0
        self.started_x = started_x
        self.started_y = started_y

    def pick_new_direction(self):
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        fate = random.choice(movements)
        self.change_x = fate[0]
        self.change_y = fate[1]
        self.time_to_change_direction = random.uniform(0.5, 1.5)


class Portal(arcade.Sprite):
    def __init__(self, x, y, mode):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.mode = mode
        self.toggle = True
        self.timer = 0
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, (0, 0, 0, 0))

    def draw_portal(self):
        cx, cy = self.center_x, self.center_y
        color_a = None
        color_b = None
        if self.mode == 1:
            color_a = arcade.color.PURPLE if self.toggle else arcade.color.BLACK
            color_b = arcade.color.BLACK if self.toggle else arcade.color.PURPLE
        elif self.mode == 2:
            color_a = arcade.color.YELLOW if self.toggle else arcade.color.BLUE
            color_b = arcade.color.BLUE if self.toggle else arcade.color.YELLOW
        elif self.mode == 3:
            color_a = arcade.color.RED if self.toggle else arcade.color.GREEN
            color_b = arcade.color.GREEN if self.toggle else arcade.color.RED

        arcade.draw_rect_filled(arcade.XYWH(cx, cy, 30, 30), color_a)
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, 20, 20), color_b)
        arcade.draw_rect_filled(arcade.XYWH(cx, cy, 10, 10), color_a)


class Wall(arcade.Sprite):
    def __init__(self, center_x, center_y, color=arcade.color.BLUE):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(TILE_SIZE - 1, color)
        self.center_x = center_x
        self.center_y = center_y


class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.wall_list = arcade.SpriteList()
        self.invis_wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()
        self.game_over = False
        self.player = None
        self.setup()

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.invis_wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()
        self.game_over = False

        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = (len(LEVEL_MAP) - 1 - row_idx) * TILE_SIZE + TILE_SIZE // 2

                if cell == "#":
                    self.wall_list.append(Wall(x, y))
                elif cell == "N":
                    self.invis_wall_list.append(Wall(x, y, arcade.color.BLACK))
                elif cell == ".":
                    self.coin_list.append(Coin(x, y))
                elif cell == "G":
                    self.ghost_list.append(Enemy(x, y))
                elif cell == "P":
                    self.player = Player(x, y)
                    self.player_list.append(self.player)
                elif cell == "T":
                    self.portal_list.append(Portal(x, y, 1))
                elif cell == "E":
                    self.portal_list.append(Portal(x, y, 2))
                elif cell == "A":
                    self.portal_list.append(Portal(x, y, 3))

    def handle_teleport(self, character):
        if character.teleport_cooldown > 0:
            return

        hit_portals = arcade.check_for_collision_with_list(character, self.portal_list)
        if hit_portals:

            # אם זה שחקן – התנהגות רגילה
            if isinstance(character, Player):
                current_p = hit_portals[0]
                for p in self.portal_list:
                    if p.mode == current_p.mode and p != current_p:
                        character.center_x = p.center_x + character.change_x * 5
                        character.center_y = p.center_y + character.change_y * 5
                        character.teleport_cooldown = 1.5
                        break

            # אם זו רוח – חוזרת להתחלה
            elif isinstance(character, Enemy):
                character.center_x = character.started_x
                character.center_y = character.started_y
                character.change_x = 0
                character.change_y = 0
                character.teleport_cooldown = 1.5

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        for ghost in self.ghost_list:
            arcade.draw_circle_filled(
                ghost.center_x ,
                ghost.center_y,
                ghost.radius + 8,
                (255, 0,0, 50)
            )
        self.ghost_list.draw()
        for ghost in self.ghost_list:
            # תחתית שטוחה לרוח
            arcade.draw_lrbt_rectangle_filled(
                ghost.center_x - ghost.radius,
                ghost.center_x + ghost.radius,
                ghost.center_y - ghost.radius,
                ghost.center_y,
                arcade.color.RED
            )

            # עיניים פשוטות כמו הפקמן
            arcade.draw_circle_filled(
                ghost.center_x - 6,
                ghost.center_y + 4,
                4,
                arcade.color.BLACK
            )

            arcade.draw_circle_filled(
                ghost.center_x + 6,
                ghost.center_y + 4,
                4,
                arcade.color.BLACK
            )


        for portal in self.portal_list:
            portal.draw_portal()

        self.player.draw_custom()
        arcade.draw_text(f"Score: {self.player.score}", 10, WINDOW_HEIGHT - 25, arcade.color.WHITE, 20)
        arcade.draw_text(f"Lives: {self.player.lives}", WINDOW_WIDTH - 90, WINDOW_HEIGHT - 25, arcade.color.WHITE, 20)

        if self.game_over == "win":
            arcade.draw_text("YOU WIN", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, arcade.color.GREEN, 80, anchor_x="center")
        elif self.game_over:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, arcade.color.RED, 80, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if self.game_over:
            if key == arcade.key.SPACE: self.setup()
            return
        if key == arcade.key.UP:
            self.player.change_y, self.player.change_x = 1, 0
        elif key == arcade.key.DOWN:
            self.player.change_y, self.player.change_x = -1, 0
        elif key == arcade.key.LEFT:
            self.player.change_x, self.player.change_y = -1, 0
        elif key == arcade.key.RIGHT:
            self.player.change_x, self.player.change_y = 1, 0

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0

    def on_update(self, delta_time):
        if self.game_over: return

        # שחקן
        maccabi_x, maccabi_y = self.player.center_x, self.player.center_y
        self.player.move(delta_time)
        # יישור עדין לגריד (רק אם קרוב למרכז)
        if self.player.change_x != 0:
            target_y = round(self.player.center_y / TILE_SIZE) * TILE_SIZE
            if abs(self.player.center_y - target_y) < 5:
                self.player.center_y = target_y

        if self.player.change_y != 0:
            target_x = round(self.player.center_x / TILE_SIZE) * TILE_SIZE
            if abs(self.player.center_x - target_x) < 5:
                self.player.center_x = target_x
        self.handle_teleport(self.player)
        self.player.animate()
        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x, self.player.center_y = maccabi_x, maccabi_y

        # עדכון פורטלים
        for portal in self.portal_list:
            portal.timer += delta_time
            if portal.timer > 0.4:
                portal.toggle = not portal.toggle
                portal.timer = 0

        # רוחות
        for ghost in self.ghost_list:
            hapoel_x, hapoel_y = ghost.center_x, ghost.center_y
            ghost.move(delta_time)
            self.handle_teleport(ghost)
            ghost.time_to_change_direction -= delta_time
            if ghost.time_to_change_direction <= 0: ghost.pick_new_direction()

            if arcade.check_for_collision_with_list(ghost, self.wall_list) or \
                    arcade.check_for_collision_with_list(ghost, self.invis_wall_list):
                ghost.center_x, ghost.center_y = hapoel_x, hapoel_y
                ghost.pick_new_direction()

        # מטבעות ופסילות
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            self.player.score += coin.value
            coin.remove_from_sprite_lists()
            if len(self.coin_list) == 0: self.game_over = "win"

        if arcade.check_for_collision_with_list(self.player, self.ghost_list):
            self.player.lives -= 1
            if self.player.lives <= 0:
                self.game_over = True
            else:
                self.player.center_x, self.player.center_y = self.player.started_x, self.player.started_y


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game_view = PacmanGame()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()
