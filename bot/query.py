import logging

import discord
import os
import logging
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import re
import requests
import datetime
from io import BytesIO
import imagehash
from PIL import Image
from urlextract import URLExtract
from hashlib import sha256
import query as query
import points as points

load_dotenv()
file_save_path = os.getenv("FILE_SAVE_PATH")
logger = logging.getLogger("message")


async def parse_message(bot, message):
    if "-play" in message.content:
        return
    urls = extract_urls(message.content)
    if len(urls) > 0:
        logger.debug("urls found in message")
        await process_urls(bot, message)
        return
    if len(message.attachments) > 0:
        logger.debug("attachments found in message")
        await process_attachments(bot, message)
        return


def extract_urls(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    return urls


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
    logger.debug("{0} has not waited for cooldown period".format(author.id))
    member = await channel.guild.fetch_member(new_user)
    await channel.send(content="{0}. {1}, enjoy the point".format(author.mention, member.mention),
                       file=discord.File(fp="/home/memes/Relax.png"))


async def send_cringe_message(author, channel, date, original_user_id):
    logger.debug("post exists. sending cringe message. date: " + date)
    orignal = await channel.guild.fetch_member(original_user_id)
    await channel.send(
        "{0} Cringe. Old meme, :b:ruh. Last posted at {1} by {2} https://newfastuff.com/wp-content/uploads/2019/07/DyPlSV9.png".format(
            author.mention, date, orignal.mention))


def save_attachments(image, filename):
    logger.debug("saving new image with filename: {0}".format(filename))
    with open(file_save_path + filename, 'wb') as outfile:
        for chunk in image:
            outfile.write(chunk)


def cool_down(author_id, guild_id):
    logging.debug("starting cooldown check for user: {0} in guild: {1}".format(author_id, guild_id))
    last_post_time = query.get_user_cooldown_date(author_id, guild_id)
    if last_post_time == None:
        return False
    now = datetime.datetime.now()
    diff_time = (now - last_post_time).seconds / 60.0
    logger.debug("{0} minutes since last post from user: {1}".format(diff_time, author_id))
    if diff_time < 5.0:
        return True
    else:
        return False


async def process_attachments(bot, message):
    logger.debug("starting attachment processing for message {0}".format(message.id))
    attach = message.attachments[0]
    logger.debug("processing message attachment: {0}".format(attach.url))
    res = requests.get(attach.url)
    new_hash = str(imagehash.dhash(Image.open(BytesIO(res.content))))
    logger.debug("image hashed to: {0}".format(new_hash))
    post = query.get_post_by_hash(new_hash, message.guild.id)
    print(post)
    cooldown = cool_down(message.author.id, message.guild.id)
    # save image if not there
    if post is None:
        obj = create_post_object(new_hash, file_save_path + attach.filename, message.author.id, message.guild.id,
                                 message.id)
        query.create_post(obj)
        if cooldown:
            new_user = query.get_random_user(message.guild.id)
            points.relax_points(message.guild.id, message.author.id, message.id, new_user)
            bot.dispatch("gamble", user=new_user, guild_id=message.guild.id)
            await send_relax_message(message.author, message.channel, new_user)
            return
        else:
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
    logger.debug("found urls {0}".format(urls))
    return urls


async def process_urls(bot, message):
    logger.debug("starting profcessing urls in message {0}".format(message.content))
    urls = get_urls(message.content)
    url = urls[0]
    logger.debug("start parsing url: {0}".format(urls[0]))
    res = query.url_check(urls[0], message.guild.id)
    if res != '1':
        return
    post = query.get_post_by_hash(url, message.guild.id)
    cooldown = cool_down(message.author.id, message.guild.id)
    # save image if not there
    if post is None:
        obj = create_post_object(url, url, message.author.id, message.guild.id, message.id)
        # add url
        query.create_post(obj)
        if cooldown:
            new_user = query.get_random_user(message.guild.id)
            points.relax_points(message.guild.id, message.author.id, message.id, new_user)
            bot.dispatch("gamble", new_user, message.guild.id)
            await send_relax_message(message.author, message.channel, new_user)
            return
        else:
            points.reg_points(message.author.id, message.guild.id, message.id)
            return
    # send cooldown message if 
    elif post is not None:
        points.cringe_points(post["user_id"], message.guild.id, message.author.id, message.id)
        await send_cringe_message(message.author, message.channel,
                                  post["created"].strftime(
                                      "%m/%d/%Y, %H:%M:%S"))
        return

