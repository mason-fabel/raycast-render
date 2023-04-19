from typing import Any, Dict
import pygame


class TextureManager:
    def __init__(self, texture_path: str, texture_size: int, textures: list[Dict[str, Any]]):
        self.textures: Dict[str, pygame.Surface] = {}
        self.texture_sheet = pygame.image.load(texture_path)
        self.texture_size = texture_size
        for texture in textures:
            self.load_texture(texture)

    def get_texture(self, name: str):
        return self.textures[name] if name in self.textures else self.textures['unknown']

    def load_texture(self, texture_def: Dict[str, Any]):
        name = texture_def['name']
        x = texture_def['x']
        y = texture_def['y']

        self.textures[name] = self.texture_sheet.subsurface(
            (x * self.texture_size, y * self.texture_size, self.texture_size, self.texture_size))
