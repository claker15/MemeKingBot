import discord
from discord.ext import commands
import bot.query as query


class url_track(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def track(self, ctx: commands.Context):
        url_to_add = ctx.args[0]
        #check if it exists in database
        data = query.execute_query(url_to_add, ctx.guild.id)
        #if not, add
        if data != '1':
            query.addUrl(url_to_add, ctx.guild.id)
            await ctx.send("url added")
        #otherwise send message
        else:
            await ctx.send("url already being tracked")



def setup(bot):
    return bot.add_cog(url_track(bot))