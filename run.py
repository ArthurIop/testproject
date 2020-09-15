import redis
from flask import Flask, request, abort
import settings
import db
from typing import List

redis_instance = redis.Redis(db=1)

def initialize_db(
        redis_instance: redis.client.Redis,
        cfg_keys: List[str],
        default_value: int,
        hashset_name: str
) -> None:
    for key in settings.cfg_keys:
        redis_instance.hset(settings.hashset_name, key, settings.default_value)

initialize_db(redis_instance, settings.cfg_keys, settings.default_value, settings.hashset_name)

app = Flask(__name__)


@app.route('/votes', methods=['POST'])
def votes():
    request_body = request.json

    if not request_body or not settings.vote_key in request_body:
        abort(400, 'This key does not exist')

    voted_letter = request_body[settings.vote_key]

    return db.vote_for(
        voted_letter,
        redis_instance,
        settings.hashset_name
    )

if __name__ == '__main__':
    app.run()