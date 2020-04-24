"""
Recipes are combinations of three monsters. When a player fills a recipe they get an upgrade.
"""

import arcade

from config import SpritePaths
from enum import Enum


class Recipe(Enum):
    """
    A class of different recipes
    """

    GHOSTS = ['ghost', 'ghost', 'ghost']
    FROGS = ['frog', 'frog', 'frog']
    GHOST_FROG = ['ghost', 'ghost', 'frog']
    FROG_GHOST = ['ghost', 'frog', 'frog']


class ActiveRecipe(arcade.SpriteList):
    """
    Keeps track of the active recipe and draws it.
    """

    def __init__(self):
        super().__init__()
        self.active = Recipe.GHOSTS
        self.cycle_recipes = [self.activateFrogs, self.activateGhost]
        self.pos = 0
        self.kill_num = 0

    def render(self) -> None:
        """
        Renders all current Recipe sprites at the top right of the screen in a row.
        """
        x = 0
        for sprite in self.sprite_list:
            screen_right = arcade.get_viewport()[1] - 100
            screen_top = arcade.get_viewport()[3] - 80
            sprite.scale = 4
            sprite.center_x = screen_right - x
            sprite.center_y = screen_top

            x += 70
            sprite.draw()

    def nextRecipe(self) -> None:
        """
        Iterates to the next recipe in the list.
        """
        self.cycle_recipes[self.pos]()
        self.pos += 1
        if self.pos == len(self.cycle_recipes):
            self.pos = 0

    def addKill(self, monster_type) -> None:
        """
        Adds the kill and darkens the sprite if the monster type matches.
        :param monster_type: The monster type.
        """
        for sprite in self.sprite_list:
            if monster_type == sprite:
                sprite.color = tuple(spectrum * 0.5 for spectrum in sprite.color)
                return

    def activateGhost(self) -> None:
        """
        Make the 'Ghost' recipe the current active recipe.
        """
        self.active = Recipe.GHOSTS
        self.sprite_list = [arcade.Sprite(SpritePaths.GHOST)] * 3

    def activateFrogs(self) -> None:
        """
        Make the 'Frogs' recipe the current active recipe.
        """
        self.active = Recipe.FROGS
        self.sprite_list = [arcade.Sprite(SpritePaths.FROG)] * 3
