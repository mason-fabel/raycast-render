from dataclasses import dataclass
from pygame import Vector2


@dataclass
class Sprite:
    pos: Vector2
    texture: str


class SpriteManager:
    def __init__(self):
        self.sprite_list = {}

    def add_sprite(self, key, sprite):
        self.sprite_list[key] = sprite

    def remove_sprite(self, key):
        if key in self.sprite_list:
            del self.sprite_list[key]

    def get_sprites(self):
        return self.sprite_list.values
