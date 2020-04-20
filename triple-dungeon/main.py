"""
main.py
The main class used to load the game.
Holds the main game window, as well as manages basic functions for organizing the game.
"""
import random

import arcade

from config import Config
from map import Dungeon
from mobs import Player


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, Config.SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.floor_list = None
        self.enemy_list = None
        self.player = None

        self.dungeon = None

        # list to keep track of keypresses
        self.prev_keypress = []

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.BLACK)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists

        self.enemy_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player = Player()
        self.player.scale = 1

        # Create the dungeon
        self.dungeon = Dungeon()

        self.player.center_x, self.player.center_y = random.choice(self.dungeon.levelList).center()

        # Create monsters
        # This needs to be updated to comply with the new mobs.py code
        # self.enemy_list.append(Enemy("resources/images/monsters/ghost/ghost1.png", 200, 200, 4))
        # self.enemy_list.append(Enemy("resources/images/monsters/frog/frog1.png", 200, 1000, 4))

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.dungeon.getWalls())

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        x, y = self.player.center_x, self.player.center_y + 100
        arcade.draw_text(f"({x}, {y})", x, y, arcade.color.WHITE, 15)

        # Draw our sprites
        self.dungeon.render()
        self.player.draw()
        self.enemy_list.draw()
        self.wall_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = Config.PLAYER_MOVEMENT_SPEED
            self.prev_keypress.append(key)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -Config.PLAYER_MOVEMENT_SPEED
            self.prev_keypress.append(key)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -Config.PLAYER_MOVEMENT_SPEED
            self.prev_keypress.append(key)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = Config.PLAYER_MOVEMENT_SPEED
            self.prev_keypress.append(key)
        elif key == 65307:
            self.close()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
            self.prev_keypress.remove(key)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
            self.prev_keypress.remove(key)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
            self.prev_keypress.remove(key)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0
            self.prev_keypress.remove(key)
        if self.prev_keypress:
            self.on_key_press(self.prev_keypress.pop(0), 0)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        self.player.update_animation()
        changed = False  # Track if we need to change the viewport

        # Below manages all scrolling mechanics
        # Scroll left
        left_boundary = self.view_left + Config.LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True
        # Scroll right
        right_boundary = self.view_left + Config.SCREEN_WIDTH - Config.RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True
        # Scroll up
        top_boundary = self.view_bottom + Config.SCREEN_HEIGHT - Config.TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True
        # Scroll down
        bottom_boundary = self.view_bottom + Config.BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                Config.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                Config.SCREEN_HEIGHT + self.view_bottom)


def main() -> None:
    """
    Setups up window classes and runs the game.
    """

    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
