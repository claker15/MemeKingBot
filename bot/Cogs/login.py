import datetime
import os
import disnake
from disnake.ext import commands
import logging
from dotenv import load_dotenv
import pytz
import query as query
import points as points

load_dotenv()
logger = logging.getLogger("login")
tracked_channel = os.getenv("LOGIN_AWARD_CHANNEL")


class Login(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None and str(after.channel.id) == tracked_channel:
            timezone = pytz.timezone('America/New_York')
            date = datetime.datetime.now(timezone).date()
            if not query.login_check(member.id, after.channel.guild.id, date):
                logger.info("Adding user: {} to guild: {} for date: {}".format(member.id, after.channel.guild.id, date))
                query.login_add(member.id, after.channel.guild.id, date)
                points.login_points(member.id, after.channel.guild.id)
            else:
                logger.info("User: {} already logged in today".format(member.id))
        else:
            logger.info("presence change not into tracked channel")
            return


def setup(bot):
    return bot.add_cog(Login(bot))
