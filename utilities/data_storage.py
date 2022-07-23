"""Functions for retreiving and storing highscores data and configurations."""

import os
import json

HIGHSCORES_CONFIG_FILE = "highscores_config.json"
HIGHSCORES_DATA_FILE = "highscores_data.json"


def open_highscores_config():
    """
    Opens the highscores config file and returns.
    @return: dict of highscores config.
    """
    # Load bot config
    with open(HIGHSCORES_CONFIG_FILE, encoding="utf-8", mode="r") as file:
        return json.load(file)


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
        data = {"highscore_channel_id": -1, "verification_channel_id": -1, "username_length": 12}
        config: dict = open_highscores_config()
        for boss, categories in config["highscore_table"].items():
            data["tables"][boss] = {"message_id": 0}
            boss_categories = {}
            for category in categories:  # pylint: disable=unused-variable
                rank_list = []
                boss_categories[category] = rank_list
            data["tables"][boss]["categories"] = boss_categories
    return data


def create_message_map(data: dict):
    """
    Creates a message map from input highscores data.

    @param data: highscores_data dict to create map from.
    @return: dict message_map of message to boss.
    """

    message_map = {}

    for boss, info in data["tables"].items():
        message_map[info["message_id"]] = boss

    return message_map


def save_highscores_data(data):
    """
    Saves the highscores data dict into a json file.
    @param data: dict of highscores data.
    """
    with open(HIGHSCORES_DATA_FILE, encoding="utf-8", mode="w") as file:
        file.write(json.dumps(data, indent=4))
