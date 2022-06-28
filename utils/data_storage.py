"""
Contains functions for saving and loading highscore data and configs.
"""

import json
import os

HIGHSCORES_CONFIG_FILE = "highscores_config.json"
HIGHSCORES_DATA_FILE = "highscores_data.json"


def open_highscores_data():
    """
    Opens a highscores_data.json file if one exists, otherwise creates a skeleton of the data.
    @return: dict of highscores data.
    """
    if (os.path.exists(HIGHSCORES_DATA_FILE)):
        with open(HIGHSCORES_DATA_FILE, encoding='utf-8', mode="r") as file:
            data = json.load(file)
    else:
        # create the json object
        data = {}

    return data


def open_highscores_config():
    """
    Opens the highscores config file and returns.
    @return: dict of highscores config.
    """
    # Load bot config
    with open(HIGHSCORES_CONFIG_FILE, encoding='utf-8', mode='r') as file:
        return json.load(file)


def save_highscores_data(data):
    """
    Saves the highscores data dict into a json file.
    @param data: dict of highscores data.
    """
    with open(HIGHSCORES_DATA_FILE, encoding='utf-8', mode='w') as file:
        file.write(json.dumps(data, indent=4))
