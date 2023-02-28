import time
import disnake
from disnake.ext import commands
import logging
import query as query
import points as points
import youtube_dl

logger = logging.getLogger("soundboard")
file_prefix_linux = "/home/code/MemeKingBot/bot/sounds/"
file_prefix_windows = "F:/sounds/"


def get_sound_as_options_array(guild_id):
    sounds = query.all_sounds(guild_id)
    options = []
    for i in range(len(sounds)):
        options.append(disnake.SelectOption(label=sounds[i][0], value=sounds[i][0]))
    return options


async def play_sound(inter: disnake.MessageInteraction, path):
    voice_channel = inter.author.voice.channel
    source = disnake.FFmpegPCMAudio(path)
    voice_client = await voice_channel.connect()
    voice_client.play(source)
    while voice_client.is_playing():
        time.sleep(1)
    await voice_client.disconnect()


class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Play a sound using points")
    async def sounds(self, inter: disnake.CommandInteraction):
        logger.debug("starting sound playing command")
        if inter.author.voice is None:
            await inter.response.send_message("Must be connected to a voice channel")
            return

        if query.user_points(inter.guild.id, inter.author.id) < 5:
            await inter.response.send_message("Not enough points. Need 5.")
            return

        view = DropdownView(get_sound_as_options_array(inter.guild.id), 'play')
        await inter.send(view=view)

    def sound_play(self, inter: disnake.MessageInteraction, file_path):
        logger.debug("got sound choice from user: {}".format(file_path))
        # points.sound_redemption(inter.id, inter.author.id, inter.guild.id)
        path = file_prefix_linux + str(inter.guild.id) + "/" + file_path + '.mp3'
        path = path.replace('\"', '\'')
        print(path)
        logger.debug("playing sound from path: {}".format(path))
        inter.bot.loop.create_task(play_sound(inter, path))

    # @commands.slash_command(description="Add a new sound. 10 second time limit.")
    # async def addsound(self, inter: disnake.CommandInteraction, sound_url):
    #     logger.debug("Starting addsound command")
    #     if sound_url == "":
    #         await inter.response.send_message("Need a video url")
    #         return
    #     if query.sound_count(inter.guild.id) >= 10:
    #         await inter.response.send_message("Sound limit for server reached")
    #         return
    #     if query.user_points(inter.guild.id, inter.author.id) < 10:
    #         await inter.response.send_message("Not enough points. Need 10.")
    #         return
    #     logger.debug("checks passed. Getting video metadata")
    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'outtmpl': './sounds/{}/%(title)s.%(ext)s'.format(inter.guild.id),
    #         'postprocessors': [
    #             {
    #                 'key': 'FFmpegExtractAudio',
    #                 'preferredcodec': 'mp3',
    #                 'preferredquality': '192',
    #             },
    #             {'key': 'FFmpegMetadata'},
    #         ],
    #     }
    #     ydl_info = youtube_dl.YoutubeDL(ydl_opts)
    #     with ydl_info:
    #         metadata = ydl_info.extract_info(sound_url, download=False)
    #     if 'entries' in metadata:
    #         metadata = metadata['entries'][0]
    #     logger.debug("Got video metadata: {}".format(metadata))
    #     if query.get_sound_by_path('./sounds/{}/{}.mp3'.format(inter.guild.id, metadata['title']), inter.guild.id):
    #         await inter.response.send_message("Video already exists")
    #         return
    #     if metadata['duration'] > 10:
    #         await inter.response.send_message("Video too long")
    #         return
    #     logger.debug("all checks passed. Downloading video and converting")
    #     with ydl_info:
    #         data = ydl_info.extract_info(sound_url, download=True)
    #     if 'entries' in data:
    #         data = data['entries'][0]
    #     logger.debug("Adding sound with information: {}".format(data))
    #     query.add_sound(data['title'], './sounds/{}/{}.mp3'.format(inter.guild.id, data['title']), inter.guild.id)
    #     points.sound_add(inter.id, inter.author.id, inter.guild.id)
    #     await inter.response.send_message("Sound added successfully")
    #
    # @commands.slash_command(description="Remove a sound from the list. Costs 10 points.")
    # async def delsound(self, inter: disnake.CommandInteraction):
    #     logger.debug("starting delsound command")
    #     if query.user_points(inter.guild.id, inter.author.id) < 10:
    #         await inter.response.send_message("Not enough points. Need 10.")
    #         return
    #     logger.debug("checks passed. Listing sounds to user")
    #     sounds = query.all_sounds(inter.guild.id)
    #     await inter.response.send_message(embed=build_sound_list_embed(sounds))
    #
    #     def check(user):
    #         return user.author.id == inter.author.id
    #
    #     try:
    #         reply = await self.bot.wait_for('message', check=check, timeout=15.0)
    #     except:
    #         await inter.response.send_message("Too long to respond")
    #         return
    #     logger.debug("got user response: {}".format(reply))
    #     if reply.content != "" and reply.content.isdigit():
    #         index_to_del = int(reply.content) - 1
    #     else:
    #         return
    #     logger.debug("removing sound from list")
    #     points.sound_add(inter.id, inter.author.id, inter.guild.id)
    #     sound = sounds[index_to_del]
    #     print(sound)
    #     query.delete_sound(sound[0], inter.guild.id)
    #     await inter.response.send_message("Sound removed sucessfully")


class DropdownView(disnake.ui.View):
    def __init__(self, options, operation):
        super().__init__()
        self.selection = ""
        self.add_item(Dropdown(options, operation))


class Dropdown(disnake.ui.StringSelect):
    def __init__(self, options, operation):
        super().__init__(
            placeholder="Choose a sound",
            min_values=1,
            max_values=1,
            options=options
        )
        self.operation = operation


    async def callback(self, inter: disnake.MessageInteraction):
        logger.debug("got into dropdown callback")
        if self.operation == 'play':
            Sounds.sound_play(self, inter, self.values[0])


def setup(bot):
    return bot.add_cog(Sounds(bot))
