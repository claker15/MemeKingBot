import discord
import os
import threading
import time
import schedule
from discord.ext import commands
import message as king_message
import crown as king_crown
from dotenv import load_dotenv

def emit_crown(bot):
    print("starting crowning")
    bot.dispatch('crown', ctx=bot)

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

load_dotenv()
bot = commands.Bot(command_prefix="!")
bot.load_extension("Cogs.rankings")
bot.load_extension("Cogs.help")
schedule.every(1).minute.do(emit_crown, bot)
stop_run_continuously = run_continuously()


@bot.event
async def on_crown(ctx):
    await king_crown.crown(ctx)

async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

@bot.event
async def on_message(message):
    print("got message")
    if message.author == bot.user:
        return
    await bot.process_commands(message)
    await king_message.parse_message(message)

bot.run(os.getenv("DISCORD_SECRET"))