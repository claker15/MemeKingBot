import disnake
import os
import logging
import time
import schedule
import threading
import message as king_message
import chussy as reaction_add
from dotenv import load_dotenv
from disnake.ext import commands
from logging.handlers import RotatingFileHandler


logging.basicConfig(filename="bot.log", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
handler = RotatingFileHandler(filename="bot.log", maxBytes=5*1024*1024, backupCount=1)
logger = logging.getLogger()
logger.addHandler(handler)

logger = logging.getLogger("bot")
load_dotenv()
intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)

bot.load_extension("Cogs.rankings")
bot.load_extension("Cogs.help")
bot.load_extension("Cogs.track")
bot.load_extension("Cogs.bet")
bot.load_extension("Cogs.trivia")
bot.load_extension("Cogs.equip")
bot.load_extension("Cogs.sounds")
bot.load_extension("Cogs.crown")
bot.load_extension("Cogs.musicsnob")
bot.load_extension("Cogs.login")


async def on_ready(self):
    print("Logged on as {0}!".format(self.user))


@bot.event
async def on_message(message):
    logger.info("Received message")
    if message.author == bot.user:
        logger.info("bot message. No process")
        return
    if not os.getenv("READ_CHANNELS").__contains__(message.channel.name):
        logger.info("Wrong channel")
        return
    logger.info("Parsing other contents of message")
    if message.content != "" and message.content[0] == "!":
        logger.info("running ! command")
        await bot.process_commands(message)
    else:
        logger.info("Parsing other contents of message")
        await king_message.parse_message(bot, message)
        # geodude = await message.guild.fetch_emoji("358102351287943178")
        # await message.add_reaction(geodude)


@bot.event
async def on_raw_reaction_add(payload):
    logger.info("Reaction added to message")
    if payload.emoji.name == os.getenv("EMOJI_NAME"):
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await reaction_add.check(message, payload.emoji)


@bot.event
async def on_gamble(user, guild_id):
    bet = bot.get_cog("bet")
    await bet.gamble(user, guild_id)


bot.run(os.getenv("DISCORD_SECRET"))
