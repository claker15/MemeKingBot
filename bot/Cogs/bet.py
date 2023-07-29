import os
import disnake
from disnake.ext import commands
from ..utils.query import *
from ..utils.points import *
from dotenv import load_dotenv
import logging


logger = logging.getLogger('bet')


def strip_char_from_target(string):
    stripped = string
    for char in '<>@':
        stripped = stripped.replace(char, '')
    return stripped


class bet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()

    @commands.slash_command(description="Make a bet on who will receive the next relax points")
    async def bet(self, inter: disnake.CommandInteraction, bet_amount: int, user: disnake.User):
        logger.info("starting bet command")
        logger.info("got user from arg: {}".format(user))
        if inter.channel.id != int(os.getenv("GAMBLE_CHANNEL")):
            logger.info("not the right channel response")
            await inter.response.send_message("Wrong channel")
            return

        logger.info("after stripping")
        if int(bet_amount) < 0:
            logger.info('negative number response')
            await inter.response.send_message("Bet cannot be negative")
            return
        if user_points(inter.guild.id, inter.author.id) < int(bet_amount):
            logger.info("No points response")
            await inter.response.send_message("Not enough points")
            return
        logger.info("bet has been validated. time to add it for user {}".format(inter.author))
        add_bet(inter.id, inter.author.id, user.id, inter.guild.id, bet_amount)
        bet_points(inter.id, inter.author.id, inter.guild.id, bet_amount)
        await inter.response.send_message("Bet taken. Good luck!")
        logger.info("bet successfully added")
        return

    async def gamble(self, user_picked, guild_id):
        logger.info('starting bet payouts for guild {}'.format(guild_id))
        embed = disnake.Embed()
        embed.title = "BETS WINNINGS"
        embed.colour = 0x0099ff
        embed_totals = {}
        logger.info('getting guild and channel objects')
        guild = self.bot.get_guild(int(guild_id))
        channel = guild.get_channel(int(os.getenv("GAMBLE_CHANNEL")))
        logger.info('getting outstanding bets for guild {}'.format(guild_id))
        bets = get_bets(guild_id)
        if len(bets) == 0:
            return
        logger.info('calculating payouts and listing users who won {}'.format(bets))
        for bet in bets:
            if bet[3] == user_picked:
                bet_win_points(bet[1], bet[2], bet[4], 3 * bet[5])
                if bet[2] not in embed_totals:
                    embed_totals[bet[2]] = 3 * bet[5]
                else:
                    embed_totals[bet[2]] = embed_totals[bet[2]] + (3 * bet[5])
        logger.info('adding totals for user who won bets {}'.format(embed_totals))
        for user in embed_totals:
            name = await guild.fetch_member(user)
            embed.add_field(name=name.nick, value=embed_totals[user], inline=False)
        await channel.send(embed=embed)
        logger.info('setting all bets to invalid')
        set_bets_invalid()
        return


def setup(bot):
    return bot.add_cog(bet(bot))
