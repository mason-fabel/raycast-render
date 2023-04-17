
from dataclasses import dataclass
from enum import Enum
import math

from pygame import Vector2

from engine.map import Map
from engine.player import Player


@dataclass
class Column:
    height: int
    color: int
    shadow: bool


class RayCaster:
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
        ray = Vector2(player.dir.x + player.plane.x * camera_x,
                      player.dir.y + player.plane.y * camera_x)

        # map coords
        map = Vector2(int(player.pos.x), int(player.pos.y))

        # length between intersects, not numerically correct but the ratio is correct
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

        intersect = 0
        side = -1
        while (intersect == 0):
            if (side_dist.x < side_dist.y):
                side_dist.x += delta_dist_x
                map.x += step.x
                side = 0
            else:
                side_dist.y += delta_dist_y
                map.y += step.y
                side = 1

            intersect = world_map.world_map[(map.x, map.y)] if (
                map.x, map.y) in world_map.world_map else 0

        dist = side_dist.x - delta_dist_x if side == 0 else side_dist.y - delta_dist_y
        height = int(self.height // dist)

        return Column(height, intersect, side == 0)
