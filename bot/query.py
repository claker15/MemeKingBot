import requests
import logging
import os
from dotenv import load_dotenv


logger = logging.getLogger('query')
load_dotenv()
url = os.getenv("BOT_API_URL")

coolDownQuery = """query getPreviousPost($user_id: String, $guild_id: String){
                    getPreviousPost(user_id: $user_id, guild_id: $guild_id) {
                        created
                    }
                }"""

postByHashQuery = """query getPostByHash($hash: String, $guild_id: String){
                    getPostByHash(hash: $hash, guild_id: $guild_id) {
                        user_id
                        hash
                        path
                        created
                    }
                }"""
createPost = """mutation createPost($input: postInput) {
                    createPost(input: $input)
        }"""
addPoints = """mutation addPoints($input: pointInput) {
                    addPoints(input: $input)
        }"""
getRandId = """query getRandomUserId($guild_id: String) {
                getRandomUserId(guild_id: $guild_id) {
                    user_id
                }
        }"""
getCringeRank = """query getCringeRank($guild_id: String){
                        getCringeRank(guild_id: $guild_id) {
                            user_id,
                            count
                        }
                    }"""
getRelaxRank = """query getRelaxRank($guild_id: String){
                        getRelaxRank(guild_id: $guild_id) {
                            user_id,
                            count
                        }
                    }"""
rankQuery = """query getRanking($guild_id: String){
                        getRanking(guild_id: $guild_id) {
                            user_id,
                            count
                        }
                    }"""
crownsQuery = """query getCrowns($guild_id: String){
                        getCrowns(guild_id: $guild_id) {
                            user_id,
                            count
                        }
                    }"""

def get_user_cooldown_date(author_id, guild_id):
    logger.debug("Getting cooldown time for user: {0} in guild {1}".format(author_id, guild_id))
    res = requests.post(url, json={"query": coolDownQuery, "variables": {"user_id": str(author_id), "guild_id": str(guild_id)}})
    post = res.json()
    logger.debug("received post: {0} from database".format(post["data"]["getPreviousPost"]))
    return float(post["data"]["getPreviousPost"]["created"])

def get_post_by_hash(hash, guild_id):
    res = requests.post(url, json={"query": postByHashQuery, "variables": {"hash": hash, "guild_id": str(guild_id)}})
    post = res.json()["data"]["getPostByHash"]
    logger.debug("post returned from getPostByHash query: {0}".format(post))
    return post

def create_post(post):
    logger.debug("Sending new post object to database: {0}".format(post))
    res = requests.post(url, json={"query": createPost, "variables": {"input": post}})
    logger.debug("received as response from createPost query: {0}".format(res.content))
    return True

def add_points(obj):
    logger.debug("Adding points entry into table: {0}".format(obj))
    res = requests.post(url, json={"query": addPoints, "variables": {"input": obj}})
    logger.debug("received as response from createPost query: {0}".format(res.content))
    return True

def get_random_user(guild_id):
    logger.debug("Getting random userid from guild: {0}".format(guild_id))
    res = requests.post(url, json={"query": getRandId, "variables": {"guild_id": str(guild_id)}})
    logger.debug("received as response from getRandomUserId query: {0}".format(res.content))
    return res.json()["data"]["getRandomUserId"]["user_id"]

def relax_rank(guild_id):
    logger.debug("Getting relax list from guild: {0}".format(guild_id))
    res = requests.post(url, json={"query": getRelaxRank, "variables": {"guild_id": str(guild_id)}})
    logger.debug("received as response from getRelaxRank query: {0}".format(res.content))
    return res.json()["data"]["getRelaxRank"]

def cringe_rank(guild_id):
    logger.debug("Getting cringe list from guild: {0}".format(guild_id))
    res = requests.post(url, json={"query": getCringeRank, "variables": {"guild_id": str(guild_id)}})
    logger.debug("received as response from getCringeRank query: {0}".format(res.content))
    return res.json()["data"]["getCringeRank"]

def rankings(guild_id):
    logger.debug("Getting cringe list from guild: {0}".format(guild_id))
    res = requests.post(url, json={"query": rankQuery, "variables": {"guild_id": str(guild_id)}})
    logger.debug("received as response from getRankings query: {0}".format(res.content))
    return res.json()["data"]["getRanking"]

def crowns(guild_id):
    logger.debug("Getting cringe list from guild: {0}".format(guild_id))
    res = requests.post(url, json={"query": crownsQuery, "variables": {"guild_id": str(guild_id)}})
    logger.debug("received as response from getCrowns query: {0}".format(res.content))
    return res.json()["data"]["getCrowns"]