import discord
import os
import logging
import message as king_message
import crown as king_crown
from dotenv import load_dotenv
from apscheduler.scheduler import Scheduler
from discord.ext import commands

sched = Scheduler()
sched.start

@sched.cron_schedule(day_of_week='sun', minute='1')
def emit_crown(bot):
    logger.debug("starting crowning")
    bot.dispatch('crown', ctx=bot)

logging.basicConfig(filename="bot.log", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logger = logging.getLogger("bot")
load_dotenv()
bot = commands.Bot(command_prefix="!")
bot.load_extension("Cogs.rankings")
bot.load_extension("Cogs.help")

@bot.event
async def on_crown(ctx):
    logger.debug("On_crown event called")
    await king_crown.crown(ctx)

async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

@bot.event
async def on_message(message):
    logger.debug("Received message")
    if message.author == bot.user:
        return
    logger.debug("Parsing commands from message")
    await bot.process_commands(message)
    logger.debug("Parsing other contents of message")
    await king_message.parse_message(message)

bot.run(os.getenv("DISCORD_SECRET"))