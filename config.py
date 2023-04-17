import yaml


class Config:
    def __init__(self, path):
        with open(path, 'r') as yml_file:
            self.config = yaml.safe_load(yml_file)

    def section(self, name):
        return self.config[name]
