import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
bot.load_extension("Cogs.commands")

async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

async def on_message(self, message):
    print('Message from {0.author}: {0.content}'.format(message))

bot.run('ODMxMzQxMDM1NTI3NDcxMTE0.YHT0rA.rJl0R-HoZXccZOy89VRt8f-zMJo')