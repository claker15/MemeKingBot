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


def relax_points(guild_id, user_id_from, message_id, new_user):
    #transfered to another
    logger.debug("got relaxed. transferring points to random person")
    
    value = 1
    if str(new_user) == str(user_id_from):
        value = 2
    logger.debug("got new user for points: {0}".format(new_user))
    obj = {
        "user_id": str(new_user),
        "guild_id": str(guild_id),
        "user_id_from": str(user_id_from),
        "value": value,
        "type": "RELAX",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def cringe_points(user_id, guild_id, user_id_from, message_id):
    #points to whoever posted image first
    if user_id == user_id_from:
        return
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


def neg_points(user_id, guild_id, message_id):
    logger.debug("adding negative points for user: {0} on guild: {1}".format(user_id, guild_id))
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": -1,
        "type": "VETO",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def bet_points(message_id, user_id, guild_id, bet):
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": -1 * int(bet),
        "type": "BET",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def bet_win_points(message_id, user_id, guild_id, points):
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": points,
        "type": "BET_WIN",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def trivia_correct_answer(message_id, user_id, guild_id, points):
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": points,
        "type": "TRIVIA_CORRECT",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def sound_redemption(message_id, user_id, guild_id):
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": -5,
        "type": "SOUND_PLAY",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def sound_add(message_id, user_id, guild_id):
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": -10,
        "type": "SOUND_ADD",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def sound_remove(message_id, user_id, guild_id):
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": -10,
        "type": "SOUND_DEL",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def wand_points(message_id, user_id, guild_id, points):
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": points,
        "type": "WAND",
        "message_id": str(message_id)
    }
    query.add_points(obj)


def upgrade_points(message_id, user_id, guild_id):
    obj = {
        "user_id": str(user_id),
        "guild_id": str(guild_id),
        "user_id_from": None,
        "value": -50,
        "type": "WAND_UPGRADE",
        "message_id": str(message_id)
    }
    query.add_points(obj)
