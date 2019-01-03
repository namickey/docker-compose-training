import time
import redis
import uuid
import firebase_admin
from firebase_admin import credentials
from flask import Flask, session, render_template, request, redirect, url_for

# firebase auth
if not len(firebase_admin._apps):
    cred = credentials.Certificate('./firebase/accountkey.json')
    default_app = firebase_admin.initialize_app(cred)

# flask
app = Flask(__name__)
# redis
cache = redis.Redis(host='redis', port=6379)

@app.route('/', methods=['GET'])
def index():
    name = 'none'
    if 'user' in session:
        name = cache.hget(str(session['user']), 'name')
        if name:
            name = name.decode()
            app.logger.error('info:' + name)
            return render_template('index.html', username=name)
    return render_template('login.html')

@app.route('/login.html', methods=['GET'])
def loginhtml():
    if 'user' in session:
        name = cache.hget(str(session['user']), 'name')
        if name:
            return redirect(url_for('index'))
    return render_template('login.html')

# login and auth token validation.
@app.route('/login', methods=['POST'])
def login():
    genUuid(request.form['username'])
    return redirect(url_for('index'))

def genUuid(username=None):
    id = str(uuid.uuid4())
    session['user'] = id
    cache.hset(id, 'name', username)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

# session
app.secret_key = 'abcd'

if __name__ == "__main__":
    app.run()
