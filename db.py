import redis
from flask import json, abort
from typing import List
from settings import cfg_keys, hashset_name, default_value
Json = str


def initialize_db(
        redis_instance: redis.client.Redis,
        cfg_keys: List[str],
        default_value: int,
        hashset_name: str
) -> None:
    for key in cfg_keys:
        redis_instance.hset(hashset_name, key, default_value)


def get_db_keys(
        redis_instance: redis.client.Redis,
        hashset_name: str
) -> List[str]:
    return redis_instance.hgetall(hashset_name)


def get_whole_db(
        redis_instance: redis.client.Redis,
        hashset_name: str
) -> Json:
    db_set = dict()

    for key in get_db_keys(redis_instance, hashset_name):
        key = key.decode("utf-8")
        value = redis_instance.hget(hashset_name, key)
        value = value.decode("utf-8")
        db_set[key] = value

    return json.dumps(db_set)


def vote_for(
        voted_letter: str,
        redis_instance: redis.client.Redis,
        hashset_name: str
) -> Json:
    if redis_instance.hget(hashset_name, voted_letter) == None:
        abort(400, 'This value does not exist')

    for key in get_db_keys(redis_instance, hashset_name):
        key = key.decode("utf-8")

        if key == voted_letter:
            redis_instance.hincrby(hashset_name, voted_letter, 1)

            return get_whole_db(redis_instance, hashset_name)