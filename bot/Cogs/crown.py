import disnake
from disnake.ext import tasks, commands
import logging
import os
from datetime import datetime
from datetime import time
import pytz
from dotenv import load_dotenv
import query as query
import points as points

load_dotenv()
logger = logging.getLogger("crown")
url = os.getenv("BOT_API_URL")
crown_guilds = os.getenv("CROWN_GUILDS").split(',')
crown_channels = os.getenv("CROWN_CHANNELS").split(',')
timezone = pytz.timezone('America/New_York')


class Crown(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.crown.start(bot)

    def cog_unload(self):
        self.crown.cancel()

    @tasks.loop(time=time(hour=0, minute=1, tzinfo=timezone))
    async def crown(self, ctx):
        if datetime.now(timezone).weekday() != 0:
            logger.info("Is not sunday. No crown today Got day: {}".format(datetime.now(timezone).day))
            pass
        logger.info("It is sunday. Time to crown")
        for index, guild_id in enumerate(crown_guilds):
            logger.info("finding user_id for king on server {0}".format(guild_id))
            guild = await ctx.fetch_guild(guild_id)
            res = query.get_king(str(guild_id))
            logger.info(res)
            logger.info("received user_id: {0} from getKing query for guild: {1}".format(res, guild_id))
            member = await guild.fetch_member(res)
            res = query.change_king_points(res, guild_id)
            logger.info("query to update king count of user: {0}".format(res))
            logger.info("getting channel {0} from guild {1}".format(crown_channels[index], guild_id))
            channel = disnake.utils.get(await guild.fetch_channels(), name=crown_channels[index])
            logger.info("found channel name {0} with id: {1} in guild: {2}".format(channel.name, channel.id, guild_id))
            await channel.send("👑{0} is Meme King of the Week 👑. Their wand has been confiscated".format(member.nick))
            logger.info("Successfully crowned {0} for server {1}".format(member.nick, guild_id))

            # add starting points for all people who posted last week
            users = query.get_users_who_posted_last_week(guild_id)
            for user in users:
                userid = user[0]
                logger.info("Giving starting points to user {0}".format(userid))
                points.starting_points(userid, guild_id)

            #fetch song and artists bests
            logger.info("Starting the music snob high awards")
            song_winner = query.get_weekly_track_pop_high(guild_id)
            member = await guild.fetch_member(song_winner.user_id)
            await channel.send("{} listened to the most popular song this week. {} by {} with a popularity score of {}".format(
                member.nick, song_winner.title, song_winner.artist_name, song_winner.track_pop))
            points.music_points(song_winner.user_id, song_winner.guild_id, 20, "TOP_SONG")
            query.track_winner_add(song_winner.guild_id, song_winner.title, song_winner.artist_name)
            artist_winner = query.get_weekly_artist_pop_high(guild_id)
            member = await guild.fetch_member(artist_winner.user_id)
            await channel.send("{} listened to the most popular artist this week. {} with a popularity score of {}".format(
                    member.nick, artist_winner.artist_name, artist_winner.artist_pop))
            points.music_points(artist_winner.user_id, artist_winner.guild_id, 20, "TOP_ARTIST")
            query.artist_winner_add(artist_winner.guild_id, artist_winner.artist_name)

            #fetch song and artist lows
            logger.info("Starting the music snob low awards")
            song_winner = query.get_weekly_track_pop_low(guild_id)
            member = await guild.fetch_member(song_winner.user_id)
            await channel.send(
                "{} listened to the least popular song this week. {} by {} with a popularity score of {}".format(
                    member.nick, song_winner.title, song_winner.artist_name, song_winner.track_pop))
            points.music_points(song_winner.user_id, song_winner.guild_id, 20, "LOW_SONG")
            query.track_winner_add(song_winner.guild_id, song_winner.title, song_winner.artist_name)
            artist_winner = query.get_weekly_artist_pop_low(guild_id)
            member = await guild.fetch_member(artist_winner.user_id)
            await channel.send(
                "{} listened to the least popular artist this week. {} with a popularity score of {}".format(
                    member.nick, artist_winner.artist_name, artist_winner.artist_pop))
            points.music_points(artist_winner.user_id, artist_winner.guild_id, 20, "LOW_ARTIST")
            query.artist_winner_add(artist_winner.guild_id, artist_winner.artist_name)


def setup(bot):
    return bot.add_cog(Crown(bot))
