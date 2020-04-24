"""
projectiles.py
Organizes classes related to projectiles
"""

import arcade

from config import SpritePaths


class Projectile(arcade.Sprite):
    """
    Represents a Projectile. Damage, sprite, speed, range, collision list?
    """
    def __init__(self, speed=7, damage=0, range=100, *args, **kwargs) -> None:
        # Set up parent class
        super().__init__()

        self.speed = speed
        self.damage = damage  # unimplemented
        self.texture = None
        self.range = range  # unimplemented
        self.collision_list = []


class Temp(Projectile):
    """
    Temporary extension of projectile to demonstrate usage
    """
    def __init__(self, *args, **kwargs) -> None:
        super(Temp, self).__init__(*args, **kwargs)
        self.texture = arcade.load_texture(SpritePaths.FROG)
        self.speed = 20
        self.scale = 1
        # collision list for who/what to collide with: wall, player, enemy

    # Can place function for starting on player or enemy
