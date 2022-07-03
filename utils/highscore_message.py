"""
Contains various functions for sending/editing the highscore messages.
"""

import nextcord
from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error


def format_highscore_message(boss_name: str):
    """
    returns a formatted string for a boss's highscore
    @param boss: the dictionary object for the boss
    @return the formatted string
    """
    ret_string = f"**{boss_name}**\n```"
    boss_data = highscores_data[boss_name]

    # Gather all categories and add to string
    for key, value in boss_data["categories"].items():
        ret_string += f"{key}".ljust(30, " ")
    ret_string += "\n"

    highscore_size = highscores_config["highscore_size"]

    # list rankings in a single line. Start with first place for each category and then continue
    for i in range(highscore_size):
        for key, value in boss_data["categories"].items():
            if len(value) > i:
                score = value[i]
                ret_string += f"{i+1}: {score[0]} - {score[1]}".ljust(30, " ")
            else:
                ret_string += f"{i+1}: submit your score".ljust(30, " ")
        ret_string += "\n"

    return ret_string + "```"


async def send_highscore_message(channel, boss_name: str):
    """
    Function takes care of checking if a message exists for a boss, then
    creating and sending/editing the message
    @param channel: the channel to send the message in/search for message id
    @param boss: the boss to send the message about
    """
    highscore_string = format_highscore_message(boss_name)

    message_id = highscores_data[boss_name]["message_id"]
    try:
        message = await channel.fetch_message(message_id)
        await message.edit(content=highscore_string)
    except nextcord.NotFound:
        # message doesn't exist.
        message = await channel.send(highscore_string)
        message_id = message.id
        highscores_data[boss_name]["message_id"] = message_id
