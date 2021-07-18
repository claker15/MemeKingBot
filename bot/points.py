import query as query
import logging

logger = logging.getLogger("points")

def reg_points(user_id, guild_id):
    logger.debug("adding regular post points for user: {0} on guild: {1}".format(user_id, guild_id))
    obj = {
        "user_id": user_id,
        "guild_id": guild_id,
        "value": 1,
        "type": "REG_POST"
    }
    #maybe some mathematical functions
    query.add_points(obj)

def relax_points(guild_id):
    #transfered to another
    logger.debug("got relaxed. transferring points to random person")
    new_user = query.get_random_user(guild_id)
    logger.debug("got new user for points: {0}".format(new_user))
    obj = {
        "user_id": new_user,
        "guild_id": guild_id,
        "value": 1,
        "type": "RELAX"
    }
    query.add_points(obj)

def cringe_points(user_id, guild_id):
    #points to whoever posted image first
    logger.debug("adding regular post points for user: {0} on guild: {1}".format(user_id, guild_id))
    obj = {
        "user_id": user_id,
        "guild_id": guild_id,
        "value": 1,
        "type": "CRINGE"
    }
    #maybe some mathematical functions
    query.add_points(obj)

