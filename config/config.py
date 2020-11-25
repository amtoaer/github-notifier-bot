import json


class Config(object):
    def __init__(self, path):
        self.path = path

    def get(self) -> dict:
        with open(self.path, "r") as f:
            config = json.loads(f.read())
        return config


config = Config('./config.json').get()
