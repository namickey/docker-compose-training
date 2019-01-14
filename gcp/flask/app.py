# -*- coding: utf-8 -*-
import time
from google.appengine.api import memcache
import uuid
from datetime import datetime
import logging
from flask import Flask, session, render_template, request, redirect, url_for

r = memcache

#JST = timezone(timedelta(hours=+9), 'JST')
talkname = 'listsabcdezy'
cachetime = 3000
app = Flask(__name__)

@app.route('/talk', methods=['POST'])
def talk():
    if request.form['content']:
        #need timezone.
        t = datetime.now().strftime("%m/%d %H:%M")
        content = str(session['user']) + '|' + t + '|' + request.form['content']
        r.set(talkname, r.get(talkname) + '||' + content, cachetime)
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    name = 'none'
    if 'user' in session:
        name = r.get(str(session['user'])+'_name')
        if name:
            talks = []
            talkall = r.get(talkname)
            if talkall:
                for x in r.get(talkname).split('||'):
                    if '' == x:
                        continue
                    talkarray = x.split('|')
                    print talkarray
                    dic = {}
                    if r.get(talkarray[0].encode('utf-8')+'_name'):
                        dic['name'] = r.get(talkarray[0].encode('utf-8')+'_name')
                        dic['stamp'] = r.get(talkarray[0].encode('utf-8')+'_stamp')
                        dic['time'] = talkarray[1]
                        dic['talk'] = talkarray[2]
                        talks.append(dic)
            else:
                r.add(talkname, '', cachetime)
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
    r.add(id + '_name', username, cachetime)
    r.add(id + '_stamp', stamp, cachetime)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# session
app.secret_key = 'abcd'
