"""
Contains various utlity functions for highscores bot
"""

import nextcord
from nextcord.ext import commands
from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from utilities.data_storage import save_highscores_data  # pylint: disable=import-error


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


async def submit_score(self, ctx: commands.Context, boss_name: str, category: str, score: str):
    """
    Adds a score to the high scores and sorts. Removes a score if larger than size limit.
    @param boss: the boss to add score to
    @param category: the category to add score to
    @param user: user who submitted score
    @param score: score (int) to add
    """
    # TODO update user submission to not have dupe users

    # create score tuple for either time or int
    # define sort index
    if highscores_config["categories"][category]["is_time_record"]:
        score_list = score.split(":")
        minutes = score_list[0]
        seconds = score_list[1]
        score_seconds = int(minutes) * 60 + int(seconds)
        score_tuple = (ctx.author.display_name, score, score_seconds)
        sort_index = 2

    else:
        score_tuple = (ctx.author.display_name, int(score))
        sort_index = 1

    scores = highscores_data[boss_name]["categories"][category]
    scores.append(score_tuple)

    # sort scores.
    ascending = highscores_config["categories"][category]["ascending"]
    scores.sort(key=lambda x: x[sort_index], reverse=not ascending)

    # enforce highscore size
    while len(scores) > highscores_config["highscore_size"]:
        scores.pop()
    highscores_data[boss_name]["categories"][category] = scores

    # edit message
    highscore_channel_id = highscores_data["highscore_channel_id"]
    print(f"Editting message {highscore_channel_id}")
    channel = self.bot.get_channel(highscore_channel_id)
    if channel is None:
        response = 'Registered Highscores channel does not exist or was never registered. \
            Register with "?register" command.'
        await ctx.send(response)
        return
    await send_highscore_message(channel, boss_name)

    # save data
    save_highscores_data(highscores_data)
