import pygame as pygame
from pygame import Vector2

import math

from engine.map import Map
from input.commands import Command


class Player:
    def __init__(
            self,
            pos: Vector2,
            dir: Vector2,
            plane: Vector2,
            speed: float,
            rot_speed: float,
            map: Map):
        self.pos = pos
        self.dir = dir.normalize()
        self.plane = plane
        self.speed = speed
        self.rot_speed = rot_speed
        self.map = map

    def update(self, commands: list[Command], delta_time: float):
        self.movement(commands, delta_time)

    def movement(self, commands: list[Command], delta_time: float):
        speed = self.speed * delta_time
        move = Vector2()

        if Command.MOVE_FORWARD in commands:
            move += self.dir * speed
        if Command.MOVE_LEFT in commands:
            move += self.dir.rotate(-90) * speed
        if Command.MOVE_BACKWARD in commands:
            move += self.dir.rotate(180) * speed
        if Command.MOVE_RIGHT in commands:
            move += self.dir.rotate(90) * speed

        self.move_with_collision(move)

        if Command.ROTATE_LEFT in commands:
            self.rotate(-self.rot_speed)
        if Command.ROTATE_RIGHT in commands:
            self.rotate(self.rot_speed)

    def move_with_collision(self, move: Vector2):
        if self.check_wall(int(self.pos.x + move.x), int(self.pos.y)):
            self.pos.x += move.x
        if self.check_wall(int(self.pos.x), int(self.pos.y + move.y)):
            self.pos.y += move.y

    def check_wall(self, x, y):
        return (x, y) not in self.map.world_map

    def rotate(self, angle: float):
        self.dir = self.dir.rotate(angle).normalize()
        self.plane = self.plane.rotate(angle)
