from email import message
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

getRandId = "select DISTINCT user_id from post where guild_id = '{}' AND YEARWEEK(created) = YEARWEEK(NOW() - INTERVAL 2 WEEK) ORDER BY RAND()"

getCringeRank = "SELECT user_id_from as user_id, COUNT(*) as count FROM points WHERE guild_id = '{}' AND type = 'CRINGE' AND YEARWEEK(date) = YEARWEEK(NOW()) GROUP BY user_id_from ORDER BY COUNT(*) DESC LIMIT 5"

getRelaxRank = "SELECT user_id_from as user_id, COUNT(*) as count FROM points WHERE guild_id = '{}' AND type = 'RELAX' AND YEARWEEK(date) = YEARWEEK(NOW()) GROUP BY user_id_from ORDER BY COUNT(*) DESC LIMIT 5"

rankQuery = "SELECT user_id, SUM(value) as count FROM points WHERE guild_id = '{}' AND YEARWEEK(date) = YEARWEEK(NOW()) GROUP BY user_id ORDER BY SUM(value) DESC LIMIT 5"

getAllUsersWhoPostedLastWeek = "SELECT user_id FROM points WHERE guild_id = '{}' AND YEARWEEK(date) = YEARWEEK(NOW())-1 GROUP BY user_id"

crownsQuery = "select user_id, crowns as count from user where guild_id='{}' GROUP BY user_id ORDER BY count DESC limit 5"

urlCheck = "SELECT '1' FROM url where guild_id='{}' AND LOCATE(url, '{}') > 0"

addUrl = "INSERT INTO url(url, guild_id) VALUES('{}', '{}')"

kingQuery = "select user_id, SUM(value) as count from points where guild_id='{}' AND  YEARWEEK(date) = YEARWEEK(NOW() - INTERVAL 1 WEEK) GROUP BY user_id ORDER BY SUM(value) DESC LIMIT 1"

changeCrownQuery = "INSERT INTO user(user_id, guild_id, created, crowns) VALUES ('{}', '{}', NOW(), 1) ON DUPLICATE KEY UPDATE crowns = crowns+1"

pointQuery = "SELECT * FROM points where message_id='{}'"

subQuery = "SELECT * FROM points WHERE message_id='{}' AND type='VETO'"

addBet = "INSERT INTO bets(message_id, user_id, target_id, guild_id, bet, valid) VALUES ('{}', '{}', '{}', '{}', {}, True)"

setBetsInvalid = "UPDATE bets SET valid=0"

getBets = "SELECT * FROM bets where guild_id='{}' and valid=1"

betTotals = "SELECT target_id, SUM(bet) FROM bets WHERE guild_id='{}' AND valid=1 GROUP BY target_id"

myBets = "SELECT target_id, SUM(bet), user_id FROM bets where guild_id='{}' AND user_id='{}' AND valid=1 GROUP BY target_id, user_id"

userPointsQuery = "SELECT SUM(value) as count FROM points WHERE guild_id = '{}' AND user_id='{}' AND YEARWEEK(date) = YEARWEEK(NOW()) GROUP BY user_id"

allSoundsQuery = "SELECT title, path from sounds where guild_id = '{}'"

soundCountQuery = "SELECT COUNT(*) from sounds where guild_id = '{}'"

addSoundQuery = "INSERT INTO sounds(title, path, guild_id) VALUES ('{}', '{}', '{}')"

getSoundByPathQuery = "SELECT path from sounds where path = '{}' AND guild_id = '{}'"

removeSoundQuery = "DELETE from sounds where title = '{}' AND guild_id = '{}'"

triviaCoolDownQuery = "select date from points where user_id='{}' AND guild_id='{}' AND type = 'TRIVIA_CORRECT' ORDER BY date DESC LIMIT 1"

userWandQuery = "SELECT wand from user where user_id='{}' AND guild_id='{}'"

userWandChangeQuery = "UPDATE user set wand='{}' where user_id='{}' AND guild_id='{}'"


def execute_query(query: str, args: list):
    try:
        conn = mysql.connector.connect(user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PASSWORD"), host=os.getenv("DATABASE_HOST"), database=os.getenv("DATABASE_DATABASE"))
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
    if len(data) == 0:
        return None
    else:
        return data[0][0]


def get_post_by_hash(hash, guild_id):
    data = execute_query(postByHashQuery, [hash, guild_id])
    logger.debug("post returned from getPostByHash query: {0}".format(data))
    if len(data) == 0:
        return None
    else:
        return data[0]


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


def get_king(guild_id):
    logger.debug("Getting king for guild: {}".format(guild_id))
    data = execute_query(kingQuery, [guild_id])
    logger.debug("received response from kingQuery: {}".format(data))
    return data[0][0]


def change_king_points(user_id, guild_id):
    logger.debug("changing point count for user: {} in guild: {}".format(user_id, guild_id))
    data = execute_query(changeCrownQuery, [user_id, guild_id])
    logger.debug("received as response when changeCrownQuery: {}".format(data))
    return data


def get_point_info(message_id):
    logger.debug("getting point information for message_id: {}".format(message_id))
    data = execute_query(pointQuery, [message_id])
    logger.debug("received response from pointQuery: {}".format(data))
    print(data[0])
    return data[0]


def get_sub_point(message_id):
    logger.debug("getting information if post has been vetoed with message id: {}".format(message_id))
    data = execute_query(subQuery, [message_id])
    logger.debug("receive response from subQuery: {}".format(data))
    if len(data) > 0:
        return True
    else:
        return False


def add_bet(message_id, user_id, target_id, guild_id, bet):
    data = execute_query(addBet, [message_id, user_id, target_id, guild_id, bet])
    logger.debug("receive response from addBet: {}".format(data))
    return data


def set_bets_invalid():
    data = execute_query(setBetsInvalid, [])
    return data


def get_bets(guild_id):
    data = execute_query(getBets, [guild_id])
    logger.debug("receive response from getBets: {}".format(data))
    return data


def bet_total(guild_id):
    data = execute_query(betTotals, [guild_id])
    logger.debug("receive response from betTotal: {}".format(data))
    return data


def my_bets(guild_id, user_id):
    data = execute_query(myBets, [guild_id, user_id])
    logger.debug("receive response from myBets: {}".format(data))
    return data


def user_points(guild_id, user_id):
    data = execute_query(userPointsQuery, [guild_id, user_id])
    logger.debug("receive response from userPointsQuery: {}".format(data))
    return data[0][0] if len(data) > 0 else 0


def all_sounds(guild_id):
    data = execute_query(allSoundsQuery, [guild_id])
    logger.debug('receive response from all_sounds: {}'.format(data))
    return data


def sound_count(guild_id):
    data = execute_query(soundCountQuery, [guild_id])
    logger.debug('receive response from sound_count: {}'.format(data))
    return int(data[0][0])


def add_sound(title, path, guild_id):
    data = execute_query(addSoundQuery, [title, path, guild_id])
    logger.debug('received response from addSoundQuery: {}'.format(data))
    return True


def get_sound_by_path(path, guild_id):
    data = execute_query(getSoundByPathQuery, [path, guild_id])
    logger.debug('received response from getSoundByPathQuery: {}'.format(data))
    return True if len(data) > 0 else False


def delete_sound(title, guild_id):
    data = execute_query(removeSoundQuery, [title, guild_id])
    logger.debug('received response from removeSoundQuery: {}'.format(data))
    return True


def trivia_cooldown(user_id, guild_id):
    data = execute_query(triviaCoolDownQuery, [user_id, guild_id])
    logger.debug('received response from triviaCoolDownQuery: {}'.format(data))
    return data[0][0] if len(data) > 0 else None


def get_user_wand(user_id, guild_id):
    data = execute_query(userWandQuery, [user_id, guild_id])
    logger.debug('received response from userWandQuery: {}'.format(data))
    return data[0][0]


def change_user_wand(wand, user_id, guild_id):
    data = execute_query(userWandChangeQuery, [wand, user_id, guild_id])
    logger.debug('received response from userWandChangeQuery: {}'.format(data))
    return data

def get_users_who_posted_last_week(guild_id):
    logger.debug("Getting list of users who posted last week from guild: {0}".format(guild_id))
    data = execute_query(getAllUsersWhoPostedLastWeek, [guild_id])
    logger.debug("received as response from getAllUsersWhoPostedLastWeek query: {0}".format(data))
    return data