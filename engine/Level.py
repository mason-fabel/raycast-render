import sys
from typing import Any
import pygame
from pygame import Surface, Vector2

from engine.Map import Map
from engine.Player import Player
from engine.Raycaster import Raycaster
from engine.Renderer import Renderer
from engine.TextureManager import TextureManager
from input.InputHandler import InputHandler


class Level:
    def __init__(self, level_data: Any):
        self.map = Map(level_data['tiles'], level_data['tile-defs'])
        self.input_handler = InputHandler()
        self.player = Player(
            Vector2(level_data['player']['pos']),
            Vector2(level_data['player']['dir']),
            Vector2(level_data['player']['cam']),
            level_data['player']['speed'],
            level_data['player']['rot_speed'],
            self.map)
        self.raycaster = Raycaster(1024, 768)
        self.texture_manager = TextureManager(
            level_data['textures']['path'],
            level_data['textures']['size'],
            level_data['textures']['texture-defs'])
        self.renderer = Renderer(1024, 768, 'gray50', 'gray30')

        self.clock = pygame.time.Clock()
        self.fps = 0
        self.delta_time = 1
        self.running = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    def update(self):
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.fps)

        keys = pygame.key.get_pressed()
        commands = self.input_handler.handle_keys(keys)
        self.player.update(commands, self.delta_time)

    def draw(self, window: Surface):
        columns = self.raycaster.cast_rays(self.player, self.map)

        self.renderer.render(window, columns, self.player,
                             self.map, self.texture_manager)

        pygame.display.set_caption(
            f'Raycast Renderer - {self.clock.get_fps(): .1f} fps')

    def run(self, window: Surface):
        while self.running:
            self.check_events()
            self.update()
            self.draw(window)

        pygame.quit()
        sys.exit()
