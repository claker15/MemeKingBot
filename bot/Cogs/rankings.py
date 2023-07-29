import disnake
import requests
import logging
import json
from disnake.ext import commands
from discord.ext.commands.core import guild_only
from ..utils.query import *

logger = logging.getLogger("rankings")


class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Gives weekly rankings")
    async def ranking(self, inter: disnake.CommandInteraction):
        logger.info("starting weekly ranking command")
        await inter.send(embed=await create_rank_message(inter.guild, "ranking", ''))

    @commands.slash_command(description="Gives rankings of crowns")
    async def crowns(self, inter: disnake.CommandInteraction):
        logger.info("starting king crowns command")
        await inter.send(embed=await create_rank_message(inter.guild, "crowns", ''))

    @commands.slash_command(description="Gives current ranking of relaxes in the week")
    async def bigrelax(self, inter: disnake.CommandInteraction):
        logger.info("starting most relax command")
        await inter.send(embed=await create_rank_message(inter.guild, "relax", ''))

    @commands.slash_command(description="Gives current ranking of cringes in the week")
    async def bigcringe(self, inter: disnake.CommandInteraction):
        logger.info("starting most cringe command")
        await inter.send(embed=await create_rank_message(inter.guild, "cringe", ''))

    @commands.slash_command(description="Gives current bets that are outstanding")
    async def betboard(self, inter: disnake.CommandInteraction):
        logger.info("starting bet board command")
        await inter.send(embed=await create_rank_message(inter.guild, 'betboard', ''))

    @commands.slash_command(description="Gives user's bets that are outstanding")
    async def mybets(self, inter: disnake.CommandInteraction):
        logger.info("starting mybets command")
        await inter.send(embed=await create_rank_message(inter.guild, 'mybets', inter.author.id))

    @commands.slash_command(description="Gives a user's current point value")
    async def mypoints(self, inter: disnake.CommandInteraction):
        logger.info("starting mypoints command")
        await inter.send(embed=await create_rank_message(inter.guild, 'mypoints', inter.author.id))

def setup(bot):
    return bot.add_cog(Ranking(bot))


async def create_rank_message(guild, querytype, user_id):
        users = []
        embed = disnake.Embed()
        if querytype == "ranking":
            users = rankings(guild.id)
            embed.title = "Current Meme King Rankings"
            embed.colour = 0x0099ff
        elif querytype == "crowns":
            users = crowns(guild.id)
            embed.title = "Coronation Leaderboard 👑"
            embed.colour = 0x0099ff
        elif querytype == "relax":
            users = relax_rank(guild.id)
            embed.title = "Biggest Pussy of the Week that Needs to Relax"
            embed.colour = 0x0099ff
        elif querytype == "cringe":
            users = cringe_rank(guild.id)
            embed.title = "Most Cringiest of the Week"
            embed.colour = 0x0099ff
        elif querytype == "betboard":
            users = bet_total(guild.id)
            embed.title = "Current Bets on Who Will Be the Next Pussy That Needs to Relax"
            embed.colour = 0x0099ff
        elif querytype == 'mybets':
            users = my_bets(guild.id, user_id)
            user = await guild.fetch_member(users[0][2])
            embed.title = "Current targets of bets for you {}".format(user.nick)
            embed.colour = 0x0099ff
        elif querytype == 'mypoints':
            user = await guild.fetch_member(user_id)
            userPoints = user_points(guild.id, user_id)
            userObj = [user_id, userPoints]
            users = [userObj]
            embed.title = "Your current points"
            embed.colour = 0x0099ff
        for user in users:
            logger.info("Getting nickname for user {0} with count {1}".format(user[0], user[1]))
            member = await guild.fetch_member(user[0])
            embed.add_field(name=member.nick, value=user[1], inline=False)
        return embed