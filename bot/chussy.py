from http import client
import query as query
import points as points
import logging
from discord.utils import get

logger = logging.getLogger("reaction")

async def check(message, geodude):
    reaction = get(message.reactions, emoji=geodude)
    logger.debug("message: {} has geodude count: {}".format(message.id, reaction.count))
    if reaction.count == 6:
        data = query.get_point_info(message.id)
        sub_from_user = ""
        if data[3] != "None":
            sub_from_user = data[3]
        else:
            sub_from_user = data[1]
    logger.debug("removing points from user: {}".format(sub_from_user))
    points.neg_points(sub_from_user, message.guild.id, message.id)
    await message.reply("This post has been vetoed. GG POGNUSSY")   
    