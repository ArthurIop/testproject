import redis 
from flask import Flask
from flask import json

app = Flask(__name__)

r = redis.Redis(db=0)
keys = r.scan_iter('*')
dick = dict()

for key in keys:
    key = key.decode("utf-8")
    value = r.get(key)
    value = value.decode("utf-8")
    dick [key] = value
    
dick = json.dumps(dick)

@app.route('/all/')
def all():
    return json.loads(dick), 200

if __name__ == '__main__':
    app.run()
