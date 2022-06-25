import discord
import logging
import os
from dotenv import load_dotenv
import query as query

load_dotenv()
logger = logging.getLogger("crown")
url = os.getenv("BOT_API_URL")
crown_guilds = os.getenv("CROWN_GUILDS").split(',')
crown_channels = os.getenv("CROWN_CHANNELS").split(',')


async def crown(ctx):
    for index, guild_id in enumerate(crown_guilds):
        logger.debug("finding user_id for king on server {0}".format(guild_id))
        guild = await ctx.fetch_guild(guild_id)
        res = query.get_king(str(guild_id))        
        logger.debug(res)
        logger.debug("received user_id: {0} from getKing query for guild: {1}".format(res, guild_id))
        member = await guild.fetch_member(res)
        res = query.change_king_points(res, guild_id)
        logger.debug("query to update king count of user: {0}".format(res))
        logger.debug("getting channel {0} from guild {1}".format(crown_channels[index], guild_id))
        channel = discord.utils.get(await guild.fetch_channels(), name=crown_channels[index])
        logger.debug("found channel name {0} with id: {1} in guild: {2}".format(channel.name, channel.id, guild_id))
        await channel.send("👑{0} is Meme King of the Week 👑".format(member.nick))
        logger.debug("succesfully crowned {0} for server {1}".format(member.nick, guild_id))

