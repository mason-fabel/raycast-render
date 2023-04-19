import pygame as pygame
import yaml


class Map:
    def __init__(self, path):
        map_data = self.load_map(path)
        self.world_map = self.build_map(map_data)
        self.texture_map = self.load_texture_map()

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

    def load_texture_map(self) -> dict[int, str]:
        return {
            1: 'stone',
            2: 'brick',
            3: 'wood',
        }

    def get_texture_id(self, map_val: int) -> str:
        return self.texture_map[map_val] if map_val in self.texture_map else 'unknown'
