import disnake
from disnake.ext import commands
from ..utils.query import *


class url_track(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Add url to track for points")
    async def track(self, inter: disnake.CommandInteraction, arg):
        #check if it exists in database
        data = url_check(arg, inter.guild.id)
        #if not, add
        if data != '1':
            add_url(arg, inter.guild.id)
            await inter.response.send_message("{} is now being tracked".format(arg))
        #otherwise send message
        else:
            await inter.response.send_message("{} is already being tracked".format(arg))


def setup(bot):
    return bot.add_cog(url_track(bot))
