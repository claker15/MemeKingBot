import disnake
import os
import logging
import time
import schedule
import threading
import message as king_message
import crown as king_crown
import chussy as reaction_add
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from disnake.ext import commands
from logging.handlers import RotatingFileHandler


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


async def emit_crown(bot):
    logger.debug("starting crowning")
    await king_crown.crown(bot)
    


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


schedule.every().sunday.at('00:01').do(emit_crown, bot)
stop_run_continuously = run_continuously()


async def on_ready(self):
    print("Logged on as {0}!".format(self.user))


@bot.event
async def on_message(message):
    logger.debug("Received message")
    if message.author == bot.user:
        logger.debug("bot message. No process")
        return
    if not os.getenv("READ_CHANNELS").__contains__(message.channel.name):
        logger.debug("Wrong channel")
        return
    logger.debug("Parsing other contents of message")
    if message.content != "" and message.content[0] == "!":
        logger.debug("running ! command")
        await bot.process_commands(message)
    else:
        logger.debug("Parsing other contents of message")
        await king_message.parse_message(bot, message)
        # geodude = await message.guild.fetch_emoji("358102351287943178")
        # await message.add_reaction(geodude)


@bot.event
async def on_raw_reaction_add(payload):
    logger.debug("Reaction added to message")
    if payload.emoji.name == os.getenv("EMOJI_NAME"):
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await reaction_add.check(message, payload.emoji)


@bot.event
async def on_gamble(user, guild_id):
    bet = bot.get_cog("bet")
    await bet.gamble(user, guild_id)


bot.run(os.getenv("DISCORD_SECRET"))
