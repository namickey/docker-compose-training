import time
import redis
import uuid
from datetime import datetime, timedelta, timezone
import logging
import firebase_admin
from firebase_admin import credentials
from flask import Flask, session, render_template, request, redirect, url_for

# firebase auth
#if not len(firebase_admin._apps):
#    cred = credentials.Certificate('./firebase/accountkey.json')
#    default_app = firebase_admin.initialize_app(cred)
# redis
r = redis.Redis(host='redis', port=6379)

JST = timezone(timedelta(hours=+9), 'JST')
talkname = 'list'

# flask
logger = logging.getLogger()
logger.addHandler(logging.FileHandler("./log/app.log"))
app = Flask(__name__)

@app.route('/talk', methods=['POST'])
def talk():
    if request.form['content']:
        r.lpush(talkname, str(session['user']) + '|' + datetime.now(JST).strftime("%m/%d %H:%M") + '|' + request.form['content'])
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    name = 'none'
    if 'user' in session:
        name = r.hget(str(session['user']), 'name')
        if name:
            name = name.decode()
            talks = []
            for x in r.lrange(talkname, 0, r.llen(talkname)):
                talkarray = x.decode().split('|')
                dic = {}
                dic['name'] = r.hget(talkarray[0], 'name').decode()
                dic['stamp'] = r.hget(talkarray[0], 'stamp').decode()
                dic['time'] = talkarray[1]
                dic['talk'] = talkarray[2]
                talks.append(dic)
            talks.reverse()
            return render_template('index.html', username=name, talks=talks)
    return render_template('login.html')

@app.route('/login.html', methods=['GET'])
def loginhtml():
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

# login and auth token validation.
@app.route('/login', methods=['POST'])
def login():
    genUuid(request.form['username'], request.form['stamp'])
    return redirect(url_for('index'))

def genUuid(username=None, stamp=None):
    id = str(uuid.uuid4())
    session['user'] = id
    r.hset(id, 'name', username)
    r.hset(id, 'stamp', stamp)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

# session
app.secret_key = 'abcd'

if __name__ == "__main__":
    app.run()
