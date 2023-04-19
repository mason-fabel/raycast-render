import pygame as pygame
import sys
from pygame import Vector2
from TextureManager import TextureManager
from config import Config
from engine.Map import Map
from engine.Player import Player
from engine.Raycaster import Raycaster
from engine.Renderer import Renderer
from input.input_handler import InputHandler


class DoomCloneReloaded:
    def __init__(self):
        self.config = Config('doom-clone-reloaded.cfg')
        self.init_pygame()
        self.init_game()
        self.delta_time = 1
        self.running = True

    def init_pygame(self):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption('Raycast Rendering')

        self.screen = pygame.display.set_mode((
            self.config.section('graphics')['width'],
            self.config.section('graphics')['height']))
        self.clock = pygame.time.Clock()
        self.fps = self.config.section('graphics')['fps']

    def init_game(self):
        self.map = Map(self.config.section('map')['path'])
        self.input_handler = InputHandler()
        self.player = Player(
            Vector2(
                self.config.section('player')['pos_x'],
                self.config.section('player')['pos_y']
            ),
            Vector2(
                self.config.section('player')['dir_x'],
                self.config.section('player')['dir_y']
            ),
            Vector2(
                self.config.section('player')['plane_x'],
                self.config.section('player')['plane_y']
            ),
            self.config.section('player')['speed'],
            self.config.section('player')['rot_speed'],
            self.map)
        self.raycaster = Raycaster(
            self.config.section('graphics')['width'],
            self.config.section('graphics')['height'])
        self.texture_manager = TextureManager(
            self.config.section('textures')['path'],
            self.config.section('textures')['size'],
            self.config.section('texture_defs'))
        self.renderer = Renderer(
            self.config.section('graphics')['width'],
            self.config.section('graphics')['height'],
            self.config.section('renderer')['floor_color'],
            self.config.section('renderer')['sky_color'])

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

    def draw(self):
        columns = self.raycaster.cast_rays(self.player, self.map)
        self.renderer.render(self.screen, columns,
                             self.map, self.texture_manager)
        self.renderer.debug_overlay(self.screen, self.clock.get_fps())

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = DoomCloneReloaded()
    game.run()
