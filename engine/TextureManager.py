from typing import Any, Dict
import pygame


class TextureManager:
    def __init__(self, texture_path: str, texture_size: int, texture_defs: list[Dict[str, Any]]):
        self.textures: Dict[str, pygame.Surface] = {}
        self.sprite_sheet = pygame.image.load(texture_path).convert()
        self.texture_size = texture_size
        for texture_def in texture_defs:
            self.load_texture(texture_def)

    def get_texture(self, name: str):
        return self.textures[name] if name in self.textures else self.textures['unknown']

    def load_texture(self, texture_def: Dict[str, Any]):
        name = texture_def['name']
        x = texture_def['x']
        y = texture_def['y']

        self.textures[name] = self.sprite_sheet.subsurface(
            (x * self.texture_size, y * self.texture_size, self.texture_size, self.texture_size)).convert()

        if 'sprite' in name:
            self.textures[name].set_colorkey(pygame.Color(0, 255, 0))
