import discord
from discord.ext import commands
import query as query


class url_track(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def track(self, ctx: commands.Context, arg):
        #check if it exists in database
        data = query.url_check(arg, ctx.guild.id)
        #if not, add
        if data != '1':
            query.add_url(arg, ctx.guild.id)
            await ctx.send("{} is now being tracked".format(arg))
        #otherwise send message
        else:
            await ctx.send("{} is already being tracked".format(arg))



def setup(bot):
    return bot.add_cog(url_track(bot))