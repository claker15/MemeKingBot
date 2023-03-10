import disnake
from disnake.ext import commands
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import query as query
from dotenv import load_dotenv
import pylast

logger = logging.getLogger("musicsnob")
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
secret = os.getenv("SPOTIFY_CLIENT_SECRET")
music_role = os.getenv("MUSIC_SNOB_ROLE_ID")
last_fm_key = os.getenv("LAST_FM_API_KEY")
last_fm_secret = os.getenv("LAST_FM_API_SECRET")



def build_embed_field(music_entry, index, nick, embed):
    logger.info("Got in the embed field method")
    logger.info("music_entry is {}".format(music_entry))
    logger.info("nickname is {}".format(nick))
    if index <= 1:
        adjective = "Most"
    else:
        adjective = "Least"
    if index % 2 == 0:
        search_type = "Song"
        pop = music_entry.track_pop
    else:
        search_type = "Artist"
        pop = music_entry.artist_pop

    name = "{} Popular {} of the Week".format(adjective, search_type)
    value = "{}: {} by {} with popularity of {:,}".format(nick, music_entry.title, music_entry.artist_name, pop)
    embed.add_field(name=name, value=value, inline=False)


class MusicSnob(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        auth_manager = SpotifyClientCredentials(client_id, secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=auth_manager)
        self.network = pylast.LastFMNetwork(
            api_key=last_fm_key,
            api_secret=last_fm_secret
        )


    @commands.slash_command(description="Look at the current music snob running entries")
    async def snob_board(self, inter: disnake.CommandInteraction):
        embed = disnake.Embed()
        embed.title = "Current Music Snob Rankings"
        embed.colour = 0x0099ff
        entry_list = query.music_snob_combo_query(inter.guild.id)
        index = 0
        for entry in entry_list:
            member = await inter.guild.fetch_member(entry.user_id)
            build_embed_field(entry, index, member.nick, embed)
            index += 1
        await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if not isinstance(after.activity, disnake.Spotify):
            return
        if after.get_role(int(music_role)) is None:
            logger.info("user: {} does not have role. Returning".format(after.id))
            return
        logger.info("Spotify activity change. user: {} is listening to song: {}".format(after.id, after.activity.title))
        track_name = after.activity.title
        artist_name = after.activity.artists[0]
        if query.track_exists(after.id, after.guild.id, track_name, artist_name):
            logger.info("track already exists in database for user: {}".format(after.id))
            return
        track = self.network.get_track(artist_name, track_name)
        track_pop = track.get_playcount()
        artist = self.network.get_artist(artist_name)
        artist_pop = artist.get_playcount()
        logger.info("From lastfm, got track plays: {} and artist plays: {}".format(track_pop, artist_pop))

        query.track_add(after.id, after.guild.id, track_name, artist_name, track_pop, artist_pop)
        logger.info("Added track: {} successfully for user: {}".format(track_name, after.id))


def setup(bot):
    return bot.add_cog(MusicSnob(bot))
