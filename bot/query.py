import requests
import logging
import os
from dotenv import load_dotenv


logger = logging.getLogger('query')
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
                    }
                }"""
createPost = """mutation createPost($input: postInput) {
                    createPost(input: $input)
        }"""
addPoints = """mutation addPoints($input: pointInput) {
                    addPoints(input: $input)
        }"""
getRandId = """query getRandomUserId($guild_id: String) {
                getRandownUserId(guild_id: $guild_id) {
                    user_id
                }
        }"""

def get_user_cooldown_date(author_id, guild_id):
    logger.debug("Getting cooldown time for user: {0} in guild {1}".format(author_id, guild_id))
    res = requests.post(url, json={"query": coolDownQuery, "variables": {"user_id": str(author_id), "guild_id": str(guild_id)}})
    post = res.json()
    logger.debug("received post: {0} from database".format(post["data"]["getPreviousPost"]))
    return post["data"]["getPreviousPost"]["created"]

def get_post_by_hash(hash, guild_id):
    res = requests.post(url, json={"query": postByHashQuery, "variables": {"hash": hash, "guild_id": str(guild_id)}})
    post = res.json()["data"]["getPostByHash"]
    logger.debug("post returned from getPostByHash query: {0}".format(post))
    return post

def create_post(post):
    logger.debug("Sending new post object to database: {0}".format(post))
    res = requests.post(url, json={"query": createPost, "variables": {"input": post}})
    logger.debug("received as response from createPost query: {}".format(res.content))
    return True

def add_points(obj):
    logger.debug("Adding points entry into table: {0}".format(obj))
    res = requests.post(url, json={"query": addPoints, "variables": {"input": obj}})
    logger.debug("received as response from createPost query: {}".format(res.content))
    return True

def get_random_user(guild_id):
    logger.debug("Getting random userid from guild: {0}".format(guild_id))
    res = requests.post(url, json={"query": getRandId, "variables": {guild_id: str(guild_id)}})
    logger.debug("received as response from getRandomUserId query: {}".format(res.content))
    return res.json()["data"]["getRandomUserId"]["user_id"]