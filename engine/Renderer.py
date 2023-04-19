import math
from typing import List
from pygame import Surface
import pygame
from TextureManager import TextureManager
from engine.Map import Map

from engine.Raycaster import Column


class Renderer:
    def __init__(self, width: int, height: int, floor_color: str, sky_color: str):
        self.width = width
        self.height = height
        self.floor_color = floor_color
        self.sky_color = sky_color

        self.font = pygame.font.SysFont('Consolas', 14)

    def render(self, screen: Surface, columns: List[Column], map: Map, texture_manager: TextureManager):
        half_height = self.height // 2

        self.draw_background(screen)

        for x, column in enumerate(columns):
            texture_name = map.get_texture_id(column.texture_index)
            texture_name = f'{texture_name}-shadow' if texture_name != 'unknown' and column.shadow else texture_name
            full_texture = texture_manager.get_texture(texture_name)
            column_texture = full_texture.subsurface(
                math.floor(64 - column.texture_coord * 64), 0, 1, 64)
            scaled_texture = pygame.transform.scale(
                column_texture, (1, column.height))
            screen.blit(
                scaled_texture, (x, half_height - (column.height / 2)))

    def draw_background(self, screen: Surface):
        half_height = self.height // 2

        pygame.draw.rect(screen, 'lightblue', (0, 0, self.width, half_height))
        pygame.draw.rect(screen, 'gray20',
                         (0, half_height, self.width, self.height))

    def debug_overlay(self, screen: Surface, fps: float):
        text = self.font.render(f'fps: {fps: .1f}', False, 'white')

        pygame.draw.rect(screen, 'black', (0, 0, 100, 25))
        screen.blit(text, (5, 5))
