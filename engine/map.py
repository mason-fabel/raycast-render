import pygame as pygame
import yaml


class Map:
    def __init__(self, path):
        map_data = self.load_map(path)
        self.world_map = self.build_map(map_data)

    def load_map(self, path):
        with open(path, 'r') as yml_file:
            data = yaml.safe_load(yml_file)

        return data

    def build_map(self, map_data):
        world_map = {}
        for j, row in enumerate(map_data):
            for i, value in enumerate(row):
                if value != 0:
                    world_map[(i, j)] = value
        return world_map

    def draw(self, screen):
        scale = 50
        [pygame.draw.rect(screen, 'darkgray',
                          (pos[0] * scale, pos[1] * scale, scale, scale), 2) for pos in self.world_map]
