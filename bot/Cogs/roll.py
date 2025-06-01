import datetime
import random

import disnake
import pytz
from disnake import TextInputStyle
from disnake.ext import commands
import os
from utils.query import name_roll_current_value, increment_name_roll_value, add_roll_hist_row, last_name_roll_win, last_name_roll_win_user, reset_name_roll_value
from utils.points import name_roll_fail_points, name_roll_win_points


MAX_VALUE = int(os.getenv("ROLL_MAX_VALUE"))
GLOBAL_WIN_COOLDOWN = int(os.getenv("ROLL_GLOB_CD"))
USER_COOLDOWN = int(os.getenv("ROLL_USER_CD"))


class Roll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Check current roll value")
    async def name_roll_check(self, inter: disnake.CommandInteraction):
        current_value = name_roll_current_value(inter.guild_id)
        await inter.send(f"Current value is {current_value}")
        return

    @commands.slash_command(description="Roll the dice for a chance to win")
    async def roll(self, inter: disnake.CommandInteraction):
        # check for cooldowns
        global_win_cooldown = last_name_roll_win(inter.guild_id)
        timezone = pytz.timezone('America/New_York')
        if global_win_cooldown is not None:
            curr = datetime.datetime.now()
            diff = curr - timezone.localize(global_win_cooldown)
            if diff.seconds / 60 < GLOBAL_WIN_COOLDOWN:
                await inter.send("Global cooldown in effect. No attempts allowed.")
                return
        user_cooldown = last_name_roll_win_user(inter.author.id, inter.guild_id)
        if user_cooldown is not None:
            curr = datetime.datetime.now()
            diff = curr - timezone.localize(user_cooldown)
            if diff.seconds / 60 < USER_COOLDOWN:
                await inter.send("User cooldown in effect. No attempts allowed.")
                return

        # get current value
        current_server_value = name_roll_current_value(inter.guild_id)
        # roll random value between -1 and max
        rolled_value = random.randint(-1, MAX_VALUE + 1)
        roll_won = False
        max_value_win = False
        if rolled_value == MAX_VALUE:
            reset_name_roll_value(inter.guild_id)
            name_roll_win_points(inter.author.id, inter.guild_id, MAX_VALUE)
            max_value_win = True
            roll_won = True
        elif rolled_value > current_server_value and rolled_value != MAX_VALUE:
            increment_name_roll_value(inter.guild_id)
            points_won = min(50, rolled_value) / 50 * 20
            name_roll_win_points(inter.author.id, inter.guild_id, points_won)
            roll_won = True
            await inter.send(f"You rolled {rolled_value}, high enough for {points_won} points")
        elif rolled_value == -1:
            name_roll_fail_points(inter.author.id, inter.guild_id)
            await inter.send("You rolled -1 so 10 points are taken.")
        else:
            await inter.send(f"You rolled {rolled_value}, not good enough")

        # add history row
        add_roll_hist_row(inter.author.id, inter.guild_id, roll_won)
        if max_value_win:
            await inter.response.send_modal(modal=MyModal(str(inter.id)))
        return


class MyModal(disnake.ui.Modal):
    def __init__(self, custom_id: str):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Set a server name",
                custom_id="server_name",
                style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(title="Create Tag", components=components, custom_id=f"tag-{custom_id}")

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        server_name = inter.text_values.items().get('server_name')
        await inter.message.guild.edit(name=server_name)
