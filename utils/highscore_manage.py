"""
Contains various functions for managing the highscores data
"""

from nextcord.ext import commands
from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from utils import highscore_message  # pylint: disable=import-error
from utils import data_storage  # pylint: disable=import-error


async def submit_score_int(
    self, ctx: commands.Context, boss_name: str, category: str, user: str, score: int
):
    """
    Adds a score to the high scores and sorts. Removes a score if larger than size limit.
    @param boss: the boss to add score to
    @param category: the category to add score to
    @param user: user who submitted score
    @param score: score (int) to add
    """
    # TODO update user submission to not have dupe users
    scores = highscores_data[boss_name]["categories"][category]
    score_tuple = (user, score)
    scores.append(score_tuple)
    ascending = highscores_config["categories"][category]
    scores.sort(key=lambda x: x[1], reverse=not ascending)
    while len(scores) > highscores_config["highscore_size"]:
        scores.pop()
    highscores_data[boss_name]["categories"][category] = scores

    # edit message
    channel_id = highscores_data["channel_id"]
    print(f"Editting message {channel_id}")
    channel = self.bot.get_channel(channel_id)
    if channel is None:
        response = 'Registered Highscores channel does not exist or was never registered. \
            Register with "?register" command.'
        await ctx.send(response)
        return
    await highscore_message.send_highscore_message(channel, boss_name)

    # save data
    data_storage.save_highscores_data(highscores_data)


def submit_score_str(boss: str, category: str, user: str, score: str):
    """
    Adds a score to the high scores and sorts. Removes a score if larger than size limit.
    @param boss: the boss to add score to
    @param category: the category to add score to
    @param user: user who submitted score
    @param score: score (string) to add
    """
    # TODO update user submission to not have dupe users
    # TODO sort the strings properly, update this function for string usage
    scores = highscores_data[boss][category]
    score_tuple = (user, score)
    scores.append(score_tuple)
    ascending = highscores_config["categories"][category]
    scores.sort(key=lambda x: x[1], reverse=not ascending)
    while len(scores) > highscores_config["highscore_size"]:
        scores.pop()
    highscores_data[boss][category] = scores

    # save data
    data_storage.save_highscores_data(highscores_data)
