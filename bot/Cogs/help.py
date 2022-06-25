import discord
from discord.ext import commands


class king_help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def king_help(self, ctx: commands.Context):
        embed = discord.Embed(title="MemeKingBot", description="This is a bot that will crown a meme king every week. The king is the one who posts the most unique memes that week")
        embed.add_field(name='!rankings', value='Show rankings of king candidates.', inline=False)
        embed.add_field(name='The crowning', value='Automatically occurs at 12:00AM Monday', inline=False)
        embed.add_field(name='!help', value='Shows this message',inline=False)
        embed.add_field(name='!bet', value='Bet on who will receive the next point from a relax. Use form !bet BetValue @UserChoice',inline=False)
        embed.add_field(name='!trivia', value="Answer a question right and get some memekingpoints", inline=False)
        embed.add_field(name="!sounds", value="Play a fun sounds at the expense of some points")
        embed.add_field(name="!addsound", value="Add a new sound to the list of available sounds")
        embed.add_field(name="!delsound", value="Remove sound from list")
        await ctx.send(embed=embed)


def setup(bot):
    return bot.add_cog(king_help(bot))
