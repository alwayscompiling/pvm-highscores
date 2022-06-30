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
    if os.path.exists(HIGHSCORES_DATA_FILE):
        with open(HIGHSCORES_DATA_FILE, encoding="utf-8", mode="r") as file:
            data = json.load(file)
    else:
        # create the json object
        data = {"channel_id": -1}
        config = open_highscores_config()
        for boss in config["bosses"]:
            data[boss["boss"]] = {"message_id": 0}
            boss_categories = {}
            for key, value in config["categories"].items():
                rank_list = []
                boss_categories[key] = rank_list
                if boss["hardmode"] and value["hardmode"]:
                    rank_list = []
                    boss_categories["Hardmode " + key] = rank_list
            data[boss["boss"]]["categories"] = boss_categories
    return data


def open_highscores_config():
    """
    Opens the highscores config file and returns.
    @return: dict of highscores config.
    """
    # Load bot config
    with open(HIGHSCORES_CONFIG_FILE, encoding="utf-8", mode="r") as file:
        return json.load(file)


def save_highscores_data(data):
    """
    Saves the highscores data dict into a json file.
    @param data: dict of highscores data.
    """
    with open(HIGHSCORES_DATA_FILE, encoding="utf-8", mode="w") as file:
        file.write(json.dumps(data, indent=4))
