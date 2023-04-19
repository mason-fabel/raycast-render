
from dataclasses import dataclass
from enum import Enum
import math

from pygame import Vector2

from engine.Map import Map
from engine.Player import Player


@dataclass
class Column:
    height: int
    color: int
    texture_index: int
    texture_coord: float
    shadow: bool


class Raycaster:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def cast_rays(self, player: Player, world_map: Map) -> list[Column]:
        columns = []

        for column in range(self.width):
            columns.append(self.cast_ray(column, player, world_map))

        return columns

    def cast_ray(self, column: int, player: Player, world_map: Map) -> Column:
        # where are we in the fov, from -1 to 1
        camera_x = (2 / self.width) * column - 1

        # ray to cast
        ray = camera_x * player.plane + player.dir

        # map coords
        map = Vector2(int(player.pos.x), int(player.pos.y))

        # length between intersects, not numerically correct but the ratio is correct
        # use 1e30 to prevent divide by zero exceptions
        delta_dist_x = math.fabs(1 / ray.x) if ray.x != 0 else 1e30
        delta_dist_y = math.fabs(1 / ray.y) if ray.y != 0 else 1e30

        # step and initial distance
        step = Vector2()
        side_dist = Vector2()
        if (ray.x < 0):
            step.x = -1
            side_dist.x = (player.pos.x - map.x) * delta_dist_x
        else:
            step.x = 1
            side_dist.x = (map.x + 1 - player.pos.x) * delta_dist_x

        if (ray.y < 0):
            step.y = -1
            side_dist.y = (player.pos.y - map.y) * delta_dist_y
        else:
            step.y = 1
            side_dist.y = (map.y + 1 - player.pos.y) * delta_dist_y

        # run the DDA algorithm
        intersect = 0
        side = -1
        while (intersect == 0):
            # increment the smaller of x and y
            if (side_dist.x < side_dist.y):
                side_dist.x += delta_dist_x
                map.x += step.x
                side = 0
            else:
                side_dist.y += delta_dist_y
                map.y += step.y
                side = 1

            # check for intersection
            intersect = world_map.world_map[(map.x, map.y)] if (
                map.x, map.y) in world_map.world_map else 0

        # get dist based on side. we've overcounted delta_dist once, so subtract
        dist = side_dist.x - delta_dist_x if side == 0 else side_dist.y - delta_dist_y

        # column height is inversely proportional to distance
        height = int(self.height // dist)

        texture_index = world_map.world_map[(map.x, map.y)]

        # get texture coord, from 0 to 1, based on where the intersection happened
        texture_coord = 0.0
        if side == 0:
            texture_coord = player.pos.y + dist * ray.y
        else:
            texture_coord = player.pos.x + dist * ray.x
        texture_coord -= math.floor(texture_coord)

        return Column(height, intersect, texture_index, texture_coord, side == 0)
