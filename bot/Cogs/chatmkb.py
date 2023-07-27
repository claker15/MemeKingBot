import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from bot.chat_gpt.chat_gpt import prompt_once, gpt_enabled
import logging
from bot.query import *

load_dotenv()
logger = logging.getLogger("gpt")
gpt_api_key = os.getenv("CHATGPT_API_KEY")
ai_model = os.getenv("CHATGPT_MODEL")


def new_embed(title: str) -> disnake.Embed:
    embed = disnake.Embed()
    embed.title = title
    embed.colour = 0x0099ff
    return embed


class ChatMkb(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(description="Send a prompt to ChatGPT")
    async def prompt(self, inter: disnake.CommandInteraction, prompt: str):
        if not gpt_enabled():
            inter.response.send_message("GPT Disabled")
            return
        if len(prompt) > 200:
            await inter.response.send_message("Prompt too long.")
            return
        res = prompt_once(prompt, str(inter.guild.id))
        await inter.response.send_message(res)

    @commands.slash_command(description="View current bot behavior rules")
    async def get_ai_rules(self, inter: disnake.CommandInteraction):
        if not gpt_enabled():
            inter.response.send_message("GPT Disabled")
            return
        rules = getBotBehaviors(inter.guild.id)
        embed = new_embed("Current AI Rules")
        for rule, i in rules:
            embed.add_field(name=i, value=rule['rule'], inline=False)
        await inter.send(embed=embed)

    @commands.slash_command(description="Add a new behavior rule for MemekingBot")
    async def add_ai_rules(self, inter: disnake.CommandInteraction, rule: str):
        if not gpt_enabled():
            inter.response.send_message("GPT Disabled")
            return
        suc = add_behavior(str(inter.guild.id), rule)
        await inter.response.send_message("Rule successfully added")

    @commands.slash_command(description="Remove a behavior rule for MemekingBot")
    async def rem_ai_rules(self, inter: disnake.CommandInteraction, index: int):
        if not gpt_enabled():
            inter.response.send_message("GPT Disabled")
            return
        suc = remove_bot_behavior(str(inter.guild.id), index)
        await inter.response.send_message("Rule successfully removed")


def setup(bot):
    return bot.add_cog(ChatMkb(bot))
