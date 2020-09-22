import redis
from flask import Flask, request, abort
from settings import vote_key, hashset_name, default_value, cfg_keys
from db import vote_for, initialize_db
from typing import List

redis_instance = redis.Redis(db=1)


app = Flask(__name__)

@app.route('/votes', methods=['POST'])
def votes():
    request_body = request.json

    if not request_body or not vote_key in request_body:
        abort(400, 'This key does not exist')

    voted_letter = request_body[vote_key]

    return vote_for(
        voted_letter,
        redis_instance,
        hashset_name
    )

if __name__ == '__main__':

    initialize_db(redis_instance, cfg_keys, default_value, hashset_name)

    app.run()