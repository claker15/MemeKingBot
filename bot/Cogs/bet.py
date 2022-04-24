import discord
import os
from discord.ext import commands
import query as query
import points as points
from dotenv import load_dotenv
import logging
logger = logging.getLogger('bet')


class bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()

    def strip_char_from_target(self, string):
        stripped = string
        for char in '<>@':
            stripped = stripped.replace(char, '')
        return stripped

    @commands.command()
    async def bet(self, ctx: commands.Context, arg, arg1):
        logger.debug("starting bet command")
        if ctx.channel.id != int(os.getenv("GAMBLE_CHANNEL")):
            logger.debug("not the right channel response")
            await ctx.message.reply("Wrong channel, dummy")
            return
        target = self.strip_char_from_target(arg1)
        if str(arg1[0]) != '<':
            logger.debug("invalid argument response")
            await ctx.message.reply('Invalid betting target, bud.')
            return
        if int(arg) < 0:
            logger.debug('negative number response')
            await ctx.message.reply("Bet cannot be negative, relax buddy.")
            return
        if query.user_points(ctx.guild.id, ctx.message.author.id) < int(arg):
            logger.debug("No points response")
            await ctx.message.reply("Not enough points, pussy.")
            return
        logger.debug("bet has been valided. time to add it")
        query.add_bet(ctx.message.id, ctx.message.author.id, target, ctx.guild.id, arg)
        points.bet_points(ctx.message.id, ctx.message.author.id, ctx.guild.id, arg)
        await ctx.message.reply("Bet taken. Good luck!")
        logger.debug("bet sucessfully added")
        return


    async def gamble(self, user_picked, guild_id):
        embed = discord.Embed()
        embed.title = "BETS WINNINGS"
        embed.colour = 0x0099ff
        embed_totals = {}
        guild = self.bot.get_guild(int(guild_id))
        channel = guild.get_channel(int(os.getenv("GAMBLE_CHANNEL")))
        bets = query.get_bets(guild_id)
        if len(bets) == 0:
            return
        for bet in bets:
            if bet[3] == user_picked:
                points.bet_win_points(bet[1], bet[2], bet[4], 2 * bet[5])
                if bet[2] not in embed_totals:
                    embed_totals[bet[2]] = 2 * bet[5]
                else:
                    embed_totals[bet[2]] = embed_totals[bet[2]] + (2 * bet[5])
        for user in embed_totals:
            name = await guild.fetch_member(user)
            embed.add_field(name=name.nick, value=embed_totals[user], inline=False)
        await channel.send(embed=embed)
        query.set_bets_invalid()
        return





def setup(bot):
    return bot.add_cog(bet(bot))
