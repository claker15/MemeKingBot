from utils.query import *
from utils.points import *
import logging
from discord.utils import get

logger = logging.getLogger("reaction")

async def check(message, geodude):
    reaction = get(message.reactions, emoji=geodude)
    print(reaction)
    if reaction.count == 4:
        data = get_point_info(message.id)
        sub_from_user = ""
        if data[3] != "None":
            sub_from_user = data[3]
        else:
            sub_from_user = data[1]
    logger.info("removing points from user: {}".format(sub_from_user))
    if get_sub_point(message.id):
        return
    else:
        neg_points(sub_from_user, message.guild.id, message.id)
        await message.reply("This post has been vetoed. GG POGNUSSY")   
    