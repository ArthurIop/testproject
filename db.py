import redis
from flask import json, abort
from typing import List
import settings

Json = str
redis_instance = redis.Redis(db=1)

def get_db_keys(
        redis_instance: redis.client.Redis,
        hashset_name: str
) -> List[str]:
    return redis_instance.hgetall(settings.hashset_name)


def get_whole_db(
        redis_instance: redis.client.Redis,
        hashset_name: str
) -> Json:
    db_set = dict()

    for key in get_db_keys(redis_instance, settings.hashset_name):
        key = key.decode("utf-8")
        value = redis_instance.hget(settings.hashset_name, key)
        value = value.decode("utf-8")
        db_set[key] = value

    return json.dumps(db_set)


def vote_for(
        voted_letter: str,
        redis_instance: redis.client.Redis,
        hashset_name: str
) -> Json:
    if redis_instance.hget(settings.hashset_name, voted_letter) == None:
        abort(400, 'This value does not exist')

    for key in get_db_keys(redis_instance, hashset_name):
        key = key.decode("utf-8")

        if key == voted_letter:
            redis_instance.hincrby(settings.hashset_name, voted_letter, 1)

            return get_whole_db(redis_instance, settings.hashset_name)