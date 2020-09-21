import redis
from flask import Flask, request, abort
import settings
from db import vote_for, initialize_db
from typing import List

redis_instance = redis.Redis(db=1)


app = Flask(__name__)

@app.route('/votes', methods=['POST'])
def votes():
    request_body = request.json

    if not request_body or not settings.vote_key in request_body:
        abort(400, 'This key does not exist')

    voted_letter = request_body[settings.vote_key]

    return vote_for(
        voted_letter,
        redis_instance,
        settings.hashset_name
    )

if __name__ == '__main__':

    initialize_db(redis_instance, settings.cfg_keys, settings.default_value, settings.hashset_name)

    app.run()