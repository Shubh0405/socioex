import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(f'{BASE_DIR}/core/config.json') as file:
    CONFIG = json.load(file)