import time
import redis
import uuid
import firebase_admin
from firebase_admin import credentials
from flask import Flask, session, render_template

cred = credentials.Certificate('./firebase/accountkey.json')
default_app = firebase_admin.initialize_app(cred)

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def index():
    return render_template('login.html')

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/c')
def hello():
    count = get_hit_count()
    name = 'none'
    if 'user' in session:
        name = cache.hget(str(session['user']), 'name')
        if name:
            name = name.decode()
        else:
            name = genUuid()
    else:
        name = genUuid()
    return str(session['user']) +'<br> Hello ' + name + '!!<br> I have been seen {} times.\n'.format(count)

def genUuid():
    id = str(uuid.uuid4())
    session['user'] = id
    name = 'hoge12345'
    cache.hset(id, 'name', name)
    return name

app.secret_key = 'abcd'

if __name__ == "__main__":
    app.run()
