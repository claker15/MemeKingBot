import disnake
import os
import logging
from dotenv import load_dotenv
import requests
import datetime
from io import BytesIO
import imagehash
from PIL import Image
from urlextract import URLExtract
from utils.query import *
from utils import points as points
import pytz
from utils.chat_gpt import prompt_once, gpt_enabled
from wand.wand_factory import *


load_dotenv()
file_save_path = os.getenv("FILE_SAVE_PATH")
logger = logging.getLogger("message")


async def parse_message(bot, message):
    if "-play" in message.content:
        return
    urls = get_urls(message.content)
    if len(urls) > 0:
        logger.info("urls found in message")
        await process_urls(bot, message)
        return
    if len(message.attachments) > 0:
        logger.info("attachments found in message")
        await process_attachments(bot, message)
        return

def get_chosen_bet_target(guild_id: str):
    return get_next_bet_target(guild_id)



def create_post_object(hash, path, user_id, guild_id, message_id):
    obj = {
        "hash": hash,
        "path": path,
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "message_id": str(message_id)
    }
    return obj


async def send_relax_message(author, channel, new_user):
    logger.info("{0} has not waited for cooldown period".format(author.id))
    author = await channel.guild.fetch_member(author.id)
    member = await channel.guild.fetch_member(new_user)
    if gpt_enabled():
        res = prompt_once("Make a passive aggressive comment to {} that they are losing their meme points to {} and that they deserve it and need to relax".format(author.nick, member.nick), str(channel.guild.id))
        await channel.send(content="{0}. {1}, {2}".format(author.mention, member.mention, res))
        return
    else:
        await channel.send(content="{0}. {1}, enjoy the point".format(author.mention, member.mention),
                           file=disnake.File(fp="/home/memes/Relax.png"))
        return


async def send_cringe_message(author, channel, date, original_user_id):
    logger.info("post exists. sending cringe message. date: " + date)
    author = await channel.guild.fetch_member(author.id)
    orignal = await channel.guild.fetch_member(original_user_id)
    if gpt_enabled():
        res = prompt_once("Make a passive aggressive comment to {} about how their taste in memes is cringe and that {} had a better taste on {}".format(author.nick, orignal.nick, str(date)), str(channel.guild.id))
        await channel.send(
            "{0} {3}. Last posted at {1} by {2}".format(
                author.mention, date, orignal.mention, res))
        return
    else:
        await channel.send(
            "{0} Cringe. Old meme, :b:ruh. Last posted at {1} by {2} https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".format(
                author.mention, date, orignal.mention))
        return


async def send_equip_message(message, points):
    logger.info("Equipment rolled. Sending message")
    if gpt_enabled():
        res = prompt_once("Make a short comment about a user casting a spell and shortly describe its effect.")
        await message.reply("{0} Your spell had the added effect of {1} points".format(res, points))
        return
    else:
        await message.reply("You're lucky. Your spell had the added effect of {0} points".format(points))
        return


def save_attachments(image, filename):
    logger.info("saving new image with filename: {0}".format(filename))
    with open(file_save_path + filename, 'wb') as outfile:
        for chunk in image:
            outfile.write(chunk)


def cool_down(author_id, guild_id):
    logging.debug("starting cooldown check for user: {0} in guild: {1}".format(author_id, guild_id))
    timezone = pytz.timezone('America/New_York')
    last_post_time = get_user_cooldown_date(author_id, guild_id)
    logger.info("got last_post_time: {0}".format(last_post_time))
    if last_post_time is None:
        return False
    now = datetime.datetime.now(timezone)
    logger.info("now: {}".format(now))
    diff_time = now - timezone.localize(last_post_time)
    logger.info("{0} minutes since last post from user: {1}".format(diff_time, author_id))
    if diff_time.seconds / 60 < 5.0:
        return True
    else:
        return False


async def process_attachments(bot, message):
    logger.info("starting attachment processing for message {0}".format(message.id))
    attach = message.attachments[0]
    logger.info("processing message attachment: {0}".format(attach.url))
    res = requests.get(attach.url)
    new_hash = str(imagehash.dhash(Image.open(BytesIO(res.content))))
    logger.info("image hashed to: {0}".format(new_hash))
    post = get_post_by_hash(new_hash, message.guild.id)
    print(post)
    cooldown = cool_down(message.author.id, message.guild.id)
    # save image if not there
    if post is None:
        obj = create_post_object(new_hash, file_save_path + attach.filename, message.author.id, message.guild.id,message.id)
        create_post(obj)
        if cooldown:
            # new_user = get_random_user(message.guild.id)
            new_user = get_next_bet_target(message.guild.id)
            wand = create_wand(get_user_wand(message.author.id, message.guild.id))
            if wand.roll():
                logger.info("adding wand points")
                rolled_points = wand.get_points()
                await send_equip_message(message, rolled_points)
                points.wand_points(message.id, new_user, message.guild.id, rolled_points)
            points.relax_points(message.guild.id, message.author.id, message.id, new_user)
            bot.dispatch("gamble", user=new_user, guild_id=message.guild.id)
            change_bet_target(message.guild.id)
            await send_relax_message(message.author, message.channel, new_user)
            return
        else:
            wand = create_wand(get_user_wand(message.author.id, message.guild.id))
            if wand.roll():
                logger.info("adding wand points")
                rolled_points = wand.get_points()
                await send_equip_message(message, rolled_points)
                points.wand_points(message.id, message.author.id, message.guild.id, rolled_points)
            points.reg_points(message.author.id, message.guild.id, message.id)
            return
    # send cooldown message if
    elif post is not None:
        print(post[0])
        print(post[1])
        points.cringe_points(post[0], message.guild.id, message.author.id, message.id)
        await send_cringe_message(message.author, message.channel,
                                  post[1].strftime(
                                      "%m/%d/%Y, %H:%M:%S"), post[0])
        return


def get_urls(string):
    extractor = URLExtract()
    urls = extractor.find_urls(string)
    logger.info("found urls {0}".format(urls))
    return urls


async def process_urls(bot, message):
    logger.info("starting processing urls in message {0}".format(message.content))
    urls = get_urls(message.content)
    url = urls[0]
    logger.info("start parsing url: {0}".format(urls[0]))
    res = url_check(urls[0], message.guild.id)
    if res != '1':
        return
    post = get_post_by_hash(url, message.guild.id)
    cooldown = cool_down(message.author.id, message.guild.id)
    # save image if not there
    if post is None:
        obj = create_post_object(url, url, message.author.id, message.guild.id, message.id)
        # add url
        create_post(obj)
        if cooldown:
            new_user = get_random_user(message.guild.id)
            wand = create_wand(get_user_wand(message.author.id, message.guild.id))
            if wand.roll():
                logger.info("adding wand points")
                rolled_points = wand.get_points()
                await send_equip_message(message, rolled_points)
                points.wand_points(message.id, new_user, message.guild.id, rolled_points)
            points.relax_points(message.guild.id, message.author.id, message.id, new_user)
            bot.dispatch("gamble", new_user, message.guild.id)
            await send_relax_message(message.author, message.channel, new_user)
            return
        else:
            wand = create_wand(get_user_wand(message.author.id, message.guild.id))
            if wand.roll():
                logger.info("adding wand points")
                rolled_points = wand.get_points()
                await send_equip_message(message, rolled_points)
                points.wand_points(message.id, message.author.id, message.guild.id, rolled_points)
            points.reg_points(message.author.id, message.guild.id, message.id)
            return
    # send cooldown message if
    elif post is not None:
        points.cringe_points(post[0], message.guild.id, message.author.id, message.id)
        await send_cringe_message(message.author, message.channel,
                                  post[1].strftime(
                                      "%m/%d/%Y, %H:%M:%S"))
        return

