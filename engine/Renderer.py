from dataclasses import dataclass
import math
import pygame
from pygame import Color, Surface, Vector2
from typing import List
from engine.Map import Map
from engine.Player import Player
from engine.Raycaster import Column
from engine.TextureManager import TextureManager


@dataclass
class Sprite:
    pos: Vector2
    texture_name: str


class Renderer:
    def __init__(self, width: int, height: int, floor_color: str, sky_color: str):
        self.width = width
        self.height = height
        self.floor_color = floor_color
        self.sky_color = sky_color

    def render(self, screen: Surface, columns: List[Column], player: Player, world_map: Map, texture_manager: TextureManager):
        z_buffer = list(map(lambda c: c.depth, columns))

        sprites: List[Sprite] = [
            Sprite(Vector2(1.5, 1.5), "sprite-column"),
            Sprite(Vector2(2.5, 1.5), "sprite-column"),
            Sprite(Vector2(3.5, 1.5), "sprite-column"),
            Sprite(Vector2(1.5, 3.5), "sprite-barrel"),
            Sprite(Vector2(2.5, 4.5), "sprite-barrel"),
            Sprite(Vector2(4, 4), "sprite-blood"),
            Sprite(Vector2(3, 5), "sprite-blood-skeleton"),
            Sprite(Vector2(3.5, 5.5), "sprite-barrel"),
        ]

        self.draw_background(screen)
        self.draw_walls(screen, columns, world_map, texture_manager)

        for sprite in sprites:
            self.draw_sprite(screen, sprite, z_buffer, player, texture_manager)

    def draw_background(self, screen: Surface):
        half_height = self.height // 2

        pygame.draw.rect(screen, self.sky_color,
                         (0, 0, self.width, half_height))
        pygame.draw.rect(screen, self.floor_color,
                         (0, half_height, self.width, self.height))

    def draw_walls(self, screen: Surface, columns: List[Column], map: Map, texture_manager: TextureManager):
        half_height = self.height // 2

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

    def draw_sprite(self, screen: Surface, sprite: Sprite, z_buffer: List[float], player: Player, texture_manager: TextureManager):
        sprite_pos = sprite.pos - player.pos

        # matrix multiplication magic?
        inverse_determinant = 1.0 / \
            (player.plane.x * player.dir.y - player.dir.x * player.plane.y)

        # transform sprite with inverse camera matrics
        transform = Vector2(
            inverse_determinant *
            (player.dir.y * sprite_pos.x - player.dir.x * sprite_pos.y),
            inverse_determinant *
            (-player.plane.y * sprite_pos.x + player.plane.x * sprite_pos.y),
        )

        if transform.y <= 0:
            return

        sprite_screen_x = int((self.width // 2) *
                              (1 + transform.x / transform.y))

        sprite_width = abs(int(self.height / transform.y))
        sprite_height = abs(int(self.height / transform.y))

        screen_pos = Vector2(
            sprite_screen_x - sprite_width // 2,
            int(max(self.height // 2 - sprite_height // 2, 0))
        )

        scaled_texture = pygame.transform.scale(
            texture_manager.get_texture(sprite.texture_name),
            (sprite_width, sprite_height))

        for stripe in range(sprite_width):
            column = int(screen_pos.x + stripe)

            if not (transform.y > 0 and column >= 0 and column < self.width and transform.y < z_buffer[column]):
                continue

            stripe_texture = scaled_texture.subsurface(
                stripe, 0, 1, sprite_height)
            screen.blit(stripe_texture, (screen_pos.x + stripe, screen_pos.y))
