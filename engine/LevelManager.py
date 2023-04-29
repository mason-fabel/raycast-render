import json

from engine.Level import Level


class LevelManager:
    def load(self, name: str) -> Level:
        with open(name, 'r') as level_file:
            file_str = level_file.read()
            level_json = json.loads(file_str)
            return Level(level_json)
