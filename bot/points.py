import query as query
import logging

logger = logging.getLogger("points")

def reg_points(user_id, guild_id, message_id):
    logger.debug("adding regular post points for user: {0} on guild: {1}".format(user_id, guild_id))
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": 1,
        "type": "REG_POST",
        "message_id": str(message_id)
    }
    #maybe some mathematical functions
    query.add_points(obj)

def relax_points(guild_id, user_id_from, message_id):
    #transfered to another
    logger.debug("got relaxed. transferring points to random person")
    new_user = query.get_random_user(guild_id)
    logger.debug("got new user for points: {0}".format(new_user))
    obj = {
        "user_id": str(new_user),
        "guild_id": str(guild_id),
        "user_id_from": str(user_id_from),
        "value": 1,
        "type": "RELAX",
        "message_id": str(message_id)
    }
    query.add_points(obj)

def cringe_points(user_id, guild_id, user_id_from, message_id):
    #points to whoever posted image first
    logger.debug("adding regular post points for user: {0} on guild: {1}".format(user_id, guild_id))
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": str(user_id_from),
        "value": 1,
        "type": "CRINGE",
        "message_id": str(message_id)
    }
    #maybe some mathematical functions
    query.add_points(obj)

