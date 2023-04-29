from typing import Any, Dict
import pygame
import yaml
from engine.LevelManager import LevelManager


def read_config(path: str) -> Dict[str, Any]:
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def init_pygame(config: Dict[str, Any]) -> pygame.Surface:
    pygame.init()
    pygame.display.set_caption('Raycast Rendering')
    return pygame.display.set_mode((config['graphics']['width'], config['graphics']['height']))


if __name__ == '__main__':
    config = read_config('doom-clone-reloaded.cfg')
    window = init_pygame(config)

    level_manager = LevelManager()
    level = level_manager.load('data/map01.json')

    level.run(window)
