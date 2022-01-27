import requests
import logging
import os
import mysql.connector
import random
from dotenv import load_dotenv

logger = logging.getLogger('query')
load_dotenv()
url = os.getenv("BOT_API_URL")

coolDownQuery = "select created from post where user_id='{}' AND guild_id='{}' ORDER BY created DESC LIMIT 1"

postByHashQuery = "SELECT user_id, created from post where hash=\"{}\" and guild_id=\"{}\" LIMIT 1"

createPost = "INSERT INTO post(hash, path, user_id, guild_id, message_id, created) VALUES ('{}', '{}', '{}','{}', '{}', NOW())"

addPoints = "INSERT INTO points(user_id, guild_id, user_id_from, value, type, message_id) VALUES ('{}', '{}', '{}', {},'{}','{}')"

getRandId = "select DISTINCT user_id from post where guild_id = '{}' ORDER BY RAND()"

getCringeRank = "SELECT user_id_from as user_id, COUNT(*) as count FROM points WHERE guild_id = '{}' AND type = 'CRINGE' AND YEARWEEK(date) = YEARWEEK(NOW()) GROUP BY user_id_from ORDER BY COUNT(*) DESC LIMIT 5"

getRelaxRank = "SELECT user_id_from as user_id, COUNT(*) as count FROM points WHERE guild_id = '{}' AND type = 'RELAX' AND YEARWEEK(date) = YEARWEEK(NOW()) GROUP BY user_id_from ORDER BY COUNT(*) DESC LIMIT 5"

rankQuery = "SELECT user_id, SUM(value) as count FROM points WHERE guild_id = '{}' AND YEARWEEK(date) = YEARWEEK(NOW()) GROUP BY user_id ORDER BY SUM(value) DESC LIMIT 5"

crownsQuery = "select user_id, crowns as count from user where guild_id='{}' GROUP BY user_id ORDER BY count DESC limit 5"

urlCheck = "SELECT '1' FROM url where guild_id='{}' AND LOCATE(url, '{}') > 0"

addUrl = "INSERT INTO url(url, guild_id) VALUES('{}', '{}')"


def execute_query(query: str, args: list):
    try:
        conn = mysql.connector.connect(user="api", password="apipassword", host="localhost", database="MEMEKING")
        
    except mysql.connector.Error as err:
        print(err)
    cursor = conn.cursor()
    cursor.execute(query.format(*args))
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data


def get_user_cooldown_date(author_id, guild_id):
    logger.debug("Getting cooldown time for user: {0} in guild {1}".format(author_id, guild_id))
    data = execute_query(coolDownQuery, [author_id, guild_id])
    logger.debug("received post: {0} from database".format(data))
    return data[0][0]


def get_post_by_hash(hash, guild_id):
    data = execute_query(postByHashQuery, [hash, guild_id])
    logger.debug("post returned from getPostByHash query: {0}".format(data))
    if len(data) == 0:
        return None
    post = {
        "user_id": data[0][0],
        "created": data[0][1]
    }
    return post


def create_post(post):
    logger.debug("Sending new post object to database: {0}".format(post))
    data = execute_query(createPost, [post["hash"], post["path"], post["user_id"], post["guild_id"], post["message_id"]])
    logger.debug("received as response from createPost query: {0}".format(data))
    return True


def add_points(obj):
    logger.debug("Adding points entry into table: {0}".format(obj))
    data = execute_query(addPoints, [obj["user_id"], obj["guild_id"], obj["user_id_from"], obj["value"], obj["type"], obj["message_id"]])
    logger.debug("received as response from createPost query: {0}".format(data))
    return True


def get_random_user(guild_id):
    logger.debug("Getting random userid from guild: {0}".format(guild_id))
    data = execute_query(getRandId, [guild_id])
    logger.debug("received as response from getRandomUserId query: {0}".format(data))
    random.shuffle(data)
    return data[0][0]


def relax_rank(guild_id):
    logger.debug("Getting relax list from guild: {0}".format(guild_id))
    data = execute_query(getRelaxRank, [guild_id])
    logger.debug("received as response from getRelaxRank query: {0}".format(data))
    return data


def cringe_rank(guild_id):
    logger.debug("Getting cringe list from guild: {0}".format(guild_id))
    data = execute_query(getCringeRank, [guild_id])
    logger.debug("received as response from getCringeRank query: {0}".format(data))
    return data


def rankings(guild_id):
    logger.debug("Getting cringe list from guild: {0}".format(guild_id))
    data = execute_query(rankQuery, [guild_id])
    logger.debug("received as response from getRankings query: {0}".format(data))
    return data


def crowns(guild_id):
    logger.debug("Getting cringe list from guild: {0}".format(guild_id))
    data = execute_query(crownsQuery, [guild_id])
    logger.debug("received as response from getCrowns query: {0}".format(data))
    return data


def url_check(url, guild_id):
    logger.debug("Check if url exists in tracked list: {} for guild: {}".format(url, guild_id))
    data = execute_query(urlCheck, [guild_id, url])
    logger.debug("received as response from url_check query: {0}".format(data))
    if len(data) > 0: 
        return "1"
    else:
        return "0"


def add_url(url, guild_id):
    logger.debug("Check if url exists in tracked list: {} for guild: {}".format(url, guild_id))
    data = execute_query(addUrl, [url, guild_id])
    logger.debug("received as response from add_url query: {0}".format(data))
    return data
