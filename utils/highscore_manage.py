"""
Contains various functions for managing the highscores data
"""

from nextcord.ext import commands
from highscores import highscores_config  # pylint: disable=import-error
from highscores import highscores_data  # pylint: disable=import-error
from utils import highscore_message  # pylint: disable=import-error
from utils import data_storage  # pylint: disable=import-error


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
    await highscore_message.send_highscore_message(channel, boss_name)

    # save data
    data_storage.save_highscores_data(highscores_data)
