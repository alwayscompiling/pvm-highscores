"""
Contains various functions for sending/editing the highscore messages.
"""

import highscores  # pylint: disable=import-error


def format_highscore_message(boss):
    """
    returns a formattedd string for a boss's highscore
    @param the dictionary object for the boss
    @return the formatted string
    """
    boss_name = boss["boss"]
    ret_string = f"**{boss_name}**\n"

    # Gather all categories and add to string
    for category in highscores.highscores_config["categories"]:
        category_name = category["category"]
        ret_string += f"{category_name}".ljust(30, ' ')
    ret_string += "\n"

    highscore_size = highscores.highscores_config["highscore_size"]

    # list rankings
    for i in range(highscore_size):
        for category in highscores.highscores_config["categories"]:
            ret_string += f"{i+1}: (name here)".ljust(30, ' ')
        ret_string += "\n"

    # if boss is hardmode, repeat above for hardmode applicable categories
    if boss["hardmode"]:
        for category in highscores.highscores_config["categories"]:
            if category["hardmode"]:
                category_name = category["category"]
                ret_string += f"{category_name}".ljust(30, ' ')

        ret_string += "\n"

        for i in range(highscore_size):
            for category in highscores.highscores_config["categories"]:
                if category["hardmode"]:
                    ret_string += f"{i+1}: (name here)".ljust(30, ' ')
            ret_string += "\n"
    return ret_string
