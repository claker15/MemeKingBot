# import disnake
# from disnake.ext import commands
# import logging
# import spotipy
#
# logger = logging.getLogger("musicsnob")
#
#
# class MusicSnob(commands.Cog):
#
#     def __init__(self, bot):
#         self.bot = bot
#
#     @commands.Cog.listener()
#     async def on_presence_update(self, before, after):
#         if isinstance(after.activity, disnake.Spotify):
#             logger.debug("Spotify activity change. user: {} is listening to song: {}".format(after.id, after.activity.title))
#
#
# def setup(bot):
#     return bot.add_cog(MusicSnob(bot))
