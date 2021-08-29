import discord
import requests
import logging
import json
from discord.ext import commands
from discord.ext.commands.core import guild_only
import query as query



url = "http://localhost:4000/graphql"
logger = logging.getLogger("rankings")

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranking(self, ctx: commands.Context):
        logger.debug("starting weekly ranking command")
        await ctx.send(embed=await create_rank_message(self, ctx.guild, "ranking"))

    @commands.command()
    async def crowns(self, ctx: commands.Context):
        logger.debug("starting king crowns command")
        await ctx.send(embed=await create_rank_message(self, ctx.guild, "crowns"))

    @commands.command()
    async def bigrelax(self, ctx: commands.Context):
        logger.debug("starting most relax command")
        await ctx.send(embed=await create_rank_message(self, ctx.guild, "relax"))

    @commands.command()
    async def bigcringe(self, ctx: commands.Context):
        logger.debug("starting most cringe command")
        await ctx.send(embed=await create_rank_message(self, ctx.guild, "cringe"))


def setup(bot):
    return bot.add_cog(Ranking(bot))


async def create_rank_message(self, guild, querytype):
        users = []
        embed = discord.Embed()
        if querytype == "ranking":
            users = query.rankings(guild.id)
            embed.title = "Current Meme King Rankings"
            embed.colour = 0x0099ff
        elif querytype == "crowns":
            users = query.crowns(guild.id)
            embed.title = "Coronation Leaderboard 👑"
            embed.colour = 0x0099ff
        elif querytype == "relax":
            users = query.relax_rank(guild.id)
            embed.title = "Bigest Pussy of the Week that Needs to Relax"
            embed.colour = 0x0099ff
        elif querytype == "cringe":
            users = query.cringe_rank(guild.id)
            embed.title = "Most Cringiest of the Week"
            embed.colour = 0x0099ff
        for user in users:
            logger.debug("Getting nickname for user {0} with count {1}".format(user["user_id"], user["count"]))
            member = await guild.fetch_member(user["user_id"])
            embed.add_field(name=member.nick, value=user["count"], inline=False)
        return embed