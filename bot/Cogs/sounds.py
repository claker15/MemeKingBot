import time
import discord
from discord.ext import commands
import logging
import query as query
import points as points
import youtube_dl

logger = logging.getLogger("soundboard")


def build_sound_list_embed(sound_list):
    embed = discord.Embed()
    embed.title = "Available Sounds. Type # to play sound. Costs 5 points."
    for i in range(len(sound_list)):
        embed.add_field(name=str(i+1), value=sound_list[i][0], inline=False)
    return embed


async def play_sound(ctx, path):
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    source = discord.FFmpegPCMAudio(path)
    ctx.voice_client.play(source)
    while ctx.voice_client.is_playing():
        time.sleep(1)
    await ctx.voice_client.disconnect()


class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sounds(self, ctx: commands.Context):
        logger.debug("starting sound playing command")
        if ctx.author.voice is None:
            await ctx.reply("Must be connected to a voice channel")
            return

        if query.user_points(ctx.guild.id, ctx.author.id) < 5:
            await ctx.reply("Not enough points. Need 5.")
            return

        sounds = query.all_sounds(ctx.guild.id)
        await ctx.reply(embed=build_sound_list_embed(sounds))

        def check(user):
            return user.author.id == ctx.message.author.id

        try:
            reply = await self.bot.wait_for('message',  check=check, timeout=15.0)
        except:
            await ctx.reply("Too long to respond")
            return
        logger.debug("got sound choice from user: {}".format(reply))
        points.sound_redemption(ctx.message.id, ctx.author.id, ctx.guild.id)
        if reply.content != "" and reply.content.isdigit():
            index_to_play = int(reply.content) - 1
        else:
            return

        path = "./" + sounds[index_to_play][1]
        logger.debug("playing sound from path: {}".format(path))
        self.bot.loop.create_task(play_sound(ctx, path))

    @commands.command()
    async def addsound(self, ctx: commands.Context, sound_url):
        logger.debug("Starting addsound command")
        if sound_url == "":
            await ctx.reply("Need a video url")
            return
        if query.sound_count(ctx.guild.id) >= 10:
            await ctx.reply("Sound limit for server reached")
            return
        if query.user_points(ctx.guild.id, ctx.author.id) < 10:
            await ctx.reply("Not enough points. Need 10.")
            return
        logger.debug("checks passed. Getting video metadata")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './sounds/{}/%(title)s.%(ext)s'.format(ctx.guild.id),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {'key': 'FFmpegMetadata'},
            ],
        }
        ydl_info = youtube_dl.YoutubeDL(ydl_opts)
        with ydl_info:
            metadata = ydl_info.extract_info(sound_url, download=False)
        if 'entries' in metadata:
            metadata = metadata['entries'][0]
        logger.debug("Got video metadata: {}".format(metadata))
        if query.get_sound_by_path('./sounds/{}/{}.mp3'.format(ctx.guild.id, metadata['title']), ctx.guild.id):
            await ctx.reply("Video already exists")
            return
        if metadata['duration'] > 10:
            await ctx.reply("Video too long")
            return
        logger.debug("all checks passed. Downloading video and converting")
        with ydl_info:
            data = ydl_info.extract_info(sound_url, download=True)
        if 'entries' in data:
            data = data['entries'][0]
        logger.debug("Adding sound with information: {}".format(data))
        query.add_sound(data['title'], './sounds/{}/{}.mp3'.format(ctx.guild.id, data['title']), ctx.guild.id)
        points.sound_add(ctx.message.id, ctx.author.id, ctx.guild.id)
        await ctx.reply("Sound added successfully")

    @commands.command()
    async def delsound(self, ctx: commands.Context):
        logger.debug("starting delsound command")
        if query.sound_count(ctx.guild.id) >= 10:
            await ctx.reply("Sound limit for server reached")
            return
        logger.debug("checks passed. Listing sounds to user")
        sounds = query.all_sounds(ctx.guild.id)
        await ctx.reply(embed=build_sound_list_embed(sounds))

        def check(user):
            return user.author.id == ctx.message.author.id

        try:
            reply = await self.bot.wait_for('message', check=check, timeout=15.0)
        except:
            await ctx.reply("Too long to respond")
            return
        logger.debug("got user response: {}".format(reply))
        if reply.content != "" and reply.content.isdigit():
            index_to_del = int(reply.content) - 1
        else:
            return
        logger.debug("removing sound from list")
        points.sound_add(ctx.message.id, ctx.author.id, ctx.guild.id)
        sound = sounds[index_to_del]
        print(sound)
        query.delete_sound(sound[0], ctx.guild.id)
        await ctx.reply("Sound removed sucessfully")

def setup(bot):
    return bot.add_cog(Sounds(bot))
