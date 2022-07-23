"""Functions for retreiving and storing highscores data and configurations."""

import os
import json

HIGHSCORES_CONFIG_FILE = "highscores_config.json"
HIGHSCORES_DATA_FILE = "highscores_data.json"


def create_highscore_skeleton() -> dict:
    """
    Creates a skeleton entry for new highscores data

    @return: dict skeleton entry
    """
    # create the dict
    skeleton = {"highscore_channel_id": -1, "verification_channel_id": -1, "username_length": 12}
    config: dict = open_highscores_config()
    skeleton["tables"] = {}
    for boss, categories in config["tables"].items():
        skeleton["tables"][boss] = {"message_id": 0}
        boss_categories = {}
        for category in categories:
            rank_list = []
            boss_categories[category] = rank_list
        skeleton["tables"][boss]["categories"] = boss_categories

    return skeleton


def create_message_map(data: dict):
    """
    Creates a message map from input highscores data.

    @param data: highscores_data dict to create map from.
    @return: dict message_map of message to boss.
    """

    message_map = {}

    for guild, guild_scores in data.items():
        message_map[guild] = {}
        for boss, info in guild_scores["tables"].items():
            message_map[guild][info["message_id"]] = boss

    return message_map


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
    Opens a highscores_data.json file if one exists, otherwise returns empty dict.
    @return: dict of highscores data.
    """
    if os.path.exists(HIGHSCORES_DATA_FILE):
        with open(HIGHSCORES_DATA_FILE, encoding="utf-8", mode="r") as file:
            data = json.load(file)
    else:
        data = {}
    return data


def save_highscores_data(data: dict):
    """
    Saves the highscores data dict into a json file.
    @param data: dict of highscores data.
    """
    with open(HIGHSCORES_DATA_FILE, encoding="utf-8", mode="w") as file:
        file.write(json.dumps(data, indent=4))
