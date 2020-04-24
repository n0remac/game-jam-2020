'''
Recipes are combinations of three monsters. When a player fills a recipe they get an updgrade
'''

import arcade

from config import SpritePaths


class Recipe():
    '''
    A class of different recipes
    '''

    GHOSTS = ['ghost', 'ghost', 'ghost']
    FROGS = ['frog', 'frog', 'frog']
    GHOST_FROG = ['ghost', 'ghost', 'frog']
    FROG_GHOST = ['ghost', 'frog', 'frog']


class ActiveRecipe(arcade.SpriteList):
    '''
    Keeps track of the active recipe and draws it.
    '''

    def __init__(self):
        super().__init__()
        self.active = Recipe.GHOSTS
        self.cycle_recipes = [self.activateFrogs, self.activateGhost]
        self.pos = 0
        self.kill_num = 0


    def render(self) -> None:
        x = 0
        for sprite in self.sprite_list:
            screen_right = arcade.get_viewport()[1] - 100
            screen_top = arcade.get_viewport()[3] - 80
            sprite.scale = 4
            sprite.center_x = screen_right - x
            sprite.center_y = screen_top

            x += 70
            sprite.draw()

    def next_recipe(self):
        self.cycle_recipes[self.pos]()
        self.pos += 1
        if self.pos == len(self.cycle_recipes):
            self.pos = 0

    def add_kill(self, monster_type):
        for sprite in self.sprite_list:
            if monster_type in "ghost":
                r, g, b = sprite.color
                darken = lambda c, s: c * (1 - s)
                r = darken(r, .5)
                g = darken(g, .5)
                b = darken(b, .5)
                sprite.color = (r, g, b)
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
