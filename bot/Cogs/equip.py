import disnake
from disnake.ext import commands
from wand.wand_factory import *
from points import *
import query as query
import logging

logger = logging.getLogger("Equipment")


class Equipment(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Upgrade your equipment. Will not reset at week's end")
    async def upgrade_wand(self, inter: disnake.CommandInteraction):
        logger.info("starting wand upgrade commmand")
        usr_current_points = query.user_points(inter.guild.id, inter.author.id)
        logger.info("user has {0} points".format(usr_current_points))
        if usr_current_points < 50:
            await inter.response.send_message("Not enough points")
        else:
            logger.info("user has enough points for upgrade")
            upgrade_points(inter.id, inter.author.id, inter.guild.id)
            current_wand = query.get_user_wand(inter.author.id, inter.guild.id)
            logger.info("user has {} wand".format(current_wand))
            new_wand = upgrade_wand(current_wand)
            logger.info("user is going to get {} wand".format(new_wand))
            query.change_user_wand(new_wand, inter.author.id, inter.guild.id)
            await inter.response.send_message("Wand has been upgraded to {0}".format(new_wand))

    @commands.slash_command(description="Shows which wand a user currently has")
    async def mywand(self, inter: disnake.CommandInteraction):
        logger.info("starting wand_check command")
        current_wand = query.get_user_wand(inter.author.id, inter.guild.id)
        await inter.response.send_message("You have a wand made out of {0}".format(current_wand))


def setup(bot):
    return bot.add_cog(Equipment(bot))
