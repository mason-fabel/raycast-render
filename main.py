import pygame as pygame
import sys

from pygame import Vector2

from config import Config
from engine.map import Map
from engine.player import Player
from engine.raycaster import RayCaster
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
        self.raycaster = RayCaster(
            self.config.section('graphics')['width'],
            self.config.section('graphics')['height'])

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    def update(self):
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.fps)
        pygame.display.set_caption(
            f'Raycast Rendering - {self.clock.get_fps() : .1f} fps')

        keys = pygame.key.get_pressed()
        commands = self.input_handler.handle_keys(keys)
        self.player.update(commands, self.delta_time)

    def draw(self):
        width = self.config.section('graphics')['width']
        height = self.config.section('graphics')['height']
        half_height = height / 2

        colors = {
            1: 'red',
            2: 'green',
            3: 'blue',
        }

        pygame.draw.rect(self.screen, 'black', (0, 0, width, height))

        columns = self.raycaster.cast_rays(self.player, self.map)
        for x, column in enumerate(columns):
            color_name = colors[column.color] if column.color in colors else 'gray'
            color_name = 'dark' + color_name if column.shadow else color_name
            pygame.draw.line(
                self.screen,
                color_name,
                (x, half_height - (column.height / 2)),
                (x, half_height + (column.height / 2)))

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
