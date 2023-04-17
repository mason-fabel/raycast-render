import pygame
from input.commands import Command


class InputHandler:
    def handle_keys(self, keys) -> list[Command]:
        commands = []

        if keys[pygame.K_w]:
            commands.append(Command.MOVE_FORWARD)
        if keys[pygame.K_a]:
            commands.append(Command.MOVE_LEFT)
        if keys[pygame.K_s]:
            commands.append(Command.MOVE_BACKWARD)
        if keys[pygame.K_d]:
            commands.append(Command.MOVE_RIGHT)
        if keys[pygame.K_LEFT]:
            commands.append(Command.ROTATE_LEFT)
        if keys[pygame.K_RIGHT]:
            commands.append(Command.ROTATE_RIGHT)

        return commands
