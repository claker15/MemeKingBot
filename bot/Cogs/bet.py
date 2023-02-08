import os
import disnake
from disnake.ext import commands
import query as query
import points as points
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
    async def bet(self, inter: disnake.CommandInteraction, arg: int, arg1: disnake.User):
        logger.debug("starting bet command")
        if inter.channel.id != int(os.getenv("GAMBLE_CHANNEL")):
            logger.debug("not the right channel response")
            await inter.response.send_message("Wrong channel")
            return
        target = strip_char_from_target(arg1)
        if str(arg1[0]) != '<':
            logger.debug("invalid argument response")
            await inter.response.send_message('Invalid betting target')
            return
        if int(arg) < 0:
            logger.debug('negative number response')
            await inter.response.send_message("Bet cannot be negative")
            return
        if query.user_points(inter.guild.id, inter.author.id) < int(arg):
            logger.debug("No points response")
            await inter.response.send_message("Not enough points")
            return
        logger.debug("bet has been validated. time to add it for user {}".format(inter.author))
        query.add_bet(inter.target.id, inter.author.id, target, inter.guild.id, arg)
        points.bet_points(inter.target.id, inter.author.id, inter.guild.id, arg)
        await inter.response.send_message("Bet taken. Good luck!")
        logger.debug("bet successfully added")
        return

    async def gamble(self, user_picked, guild_id):
        logger.debug('starting bet payouts for guild {}'.format(guild_id))
        embed = disnake.Embed()
        embed.title = "BETS WINNINGS"
        embed.colour = 0x0099ff
        embed_totals = {}
        logger.debug('getting guild and channel objects')
        guild = self.bot.get_guild(int(guild_id))
        channel = guild.get_channel(int(os.getenv("GAMBLE_CHANNEL")))
        logger.debug('getting outstanding bets for guild {}'.format(guild_id))
        bets = query.get_bets(guild_id)
        if len(bets) == 0:
            return
        logger.debug('calculating payouts and listing users who won {}'.format(bets))
        for bet in bets:
            if bet[3] == user_picked:
                points.bet_win_points(bet[1], bet[2], bet[4], 3 * bet[5])
                if bet[2] not in embed_totals:
                    embed_totals[bet[2]] = 3 * bet[5]
                else:
                    embed_totals[bet[2]] = embed_totals[bet[2]] + (3 * bet[5])
        logger.debug('adding totals for user who won bets {}'.format(embed_totals))
        for user in embed_totals:
            name = await guild.fetch_member(user)
            embed.add_field(name=name.nick, value=embed_totals[user], inline=False)
        await channel.send(embed=embed)
        logger.debug('setting all bets to invalid')
        query.set_bets_invalid()
        return


def setup(bot):
    return bot.add_cog(bet(bot))
