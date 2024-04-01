import datetime
import os
import string

import disnake
from disnake import ModalInteraction, MessageInteraction
from disnake.ext import commands
from utils.query import *
from utils.points import *
from dotenv import load_dotenv
import logging

logger = logging.getLogger('bet')

new_bet_weights = {'2': float(1.30), '3': float(1.50), '4': float(1.70), '5': float(2.00), '6': float(3.00)}
list_length_subtractions = {'2': 0, '3': float(0.20), '4': float(0.12), '5': float(0.23), '6': float(0.30)}

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
    async def classic_bet(self, inter: disnake.CommandInteraction, bet_amount: int, user: disnake.User):
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
                bet_win_points(bet[1], bet[2], bet[4], float(bet[6]) * float(bet[5]))
                if bet[2] not in embed_totals:
                    embed_totals[bet[2]] = float(bet[6]) * float(bet[5])
                else:
                    embed_totals[bet[2]] = embed_totals[bet[2]] + (float(bet[6]) * float(bet[5]))
        logger.info('adding totals for user who won bets {}'.format(embed_totals))
        for user in embed_totals:
            name = await guild.fetch_member(user)
            embed.add_field(name=name.nick, value=embed_totals[user], inline=False)
        await channel.send(embed=embed)
        logger.info('setting all bets to invalid')
        set_bets_invalid()
        return

    @commands.slash_command(description="Make a bet on who will receive the next relax points.")
    async def bet(self, inter: disnake.CommandInteraction, bet_amount: int, user_number: str = commands.Param(name="numberofchoices", choices=['2', '3', '4', '5', '6'])):

        if (check_existing_bet(inter.guild.id, inter.author.id)):
            await inter.response.send_message("Bet already exists. You cannot bet again")
            return
        # if (user_points(inter.guild.id, inter.author.id) <= 0):
        #     await inter.response.send_message("Not enough points to bet")
        #     return

        #get list and make list of nicknames
        user_ids = get_betting_list(inter.guild.id, int(user_number) - 1)
        userNickNames = []
        userDict = {}
        for i in range(len(user_ids)):
            user = await inter.guild.fetch_member(user_ids[i].user_id)
            nickname = user.nick if user.nick is not None else user.name
            userNickNames.append(nickname)
            userDict.__setitem__(nickname, user_ids[i].user_id)

        #get user's choices
        choiceView = UserBetView()
        dropdown = UserDropdown(userNickNames, bet_amount)
        choiceView.add_item(dropdown)

        async def select_callback(select_interaction: MessageInteraction, /) -> None:
            dropdown.disabled = True
            await inter.edit_original_response(view=choiceView)
            # calculate bets
            # for each choice -- bet_amount / number of actual choices * new_bet_wieghts(number of overall choices) - (number of actual choices * list_length_subtractions(number of overall choices))
            user_choices = select_interaction.values
            bet_points(inter.id, inter.author.id, inter.guild.id, dropdown.bet_amount)
            amount_for_each = dropdown.bet_amount / len(user_choices)
            for i in range(len(user_choices)):
                split_bet_amount = float(amount_for_each)
                weight = new_bet_weights[str(len(userNickNames))] - (float(len(user_choices)) * list_length_subtractions[str(len(userNickNames))])
                logger.info("{} making bet record using amount: {:0.2f} and weight: {:0.2f}".format(inter.author.id, split_bet_amount, weight))
                target_user_id = userDict[user_choices[i]]
                add_bet_with_weight(inter.id, inter.author.id, target_user_id, inter.guild.id, split_bet_amount, weight)


            await select_interaction.response.send_message("Bet taken")


        dropdown.callback = select_callback

        await inter.response.send_message("Make your choices", view=choiceView, ephemeral=True)

        return

    # @commands.slash_command(description="See current running total on all bets this week.")
    # async def PotTotal(self, inter: disnake.CommandInteraction):
    #     await inter.response.send_message("Current betting totals is {}".format(get_split_pot_total(inter.guild.id)))
    #     return

class UserDropdown(disnake.ui.StringSelect):
    def __init__(self, displayList, bet_amount):

        self.bet_amount = bet_amount
        options = []
        for i in range(len(displayList)):
            options.append(disnake.SelectOption(label=displayList[i]))

        super().__init__(
            placeholder="Choose users to bet on",
            options=options,
            min_values=1,
            max_values=len(displayList) - 1 if len(displayList) > 1 else 1,
        )

class UserBetView(disnake.ui.View):

    user_choices = []

    def __init__(self):
        super().__init__()


def setup(bot):
    return bot.add_cog(bet(bot))
