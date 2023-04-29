from typing import Dict, List
import pygame as pygame


class Map:
    def __init__(self, map_data: List[List[int]], tile_defs: Dict[str, str]):
        self.world_map = self.build_map(map_data)
        print(tile_defs)
        self.tile_defs = tile_defs

    def build_map(self, map_data):
        world_map = {}
        for j, row in enumerate(map_data):
            for i, value in enumerate(row):
                if value != 0:
                    world_map[(i, j)] = value
        return world_map

    def get_texture_id(self, map_val: int) -> str:
        key = str(map_val)
        return self.tile_defs[key] if key in self.tile_defs else 'unknown'
