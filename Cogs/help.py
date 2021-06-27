import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(title="MemeKingBot", description="This is a bot that will crown a meme king every week. The king is the one who posts the most unique memes that week")
        embed.add_field(name='!rankings', value='Show rankings of king candidates.', inline=False)
        embed.add_field(name='The crowning', value='Automatically ccurs at 12:00AM Monday', inline=False)
        embed.add_field(name='!help', value='Shows this message',inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    return bot.add_cog(Help(bot))