# -*- coding: utf-8 -*-
import logging
from flask import Flask, jsonify, render_template
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

app = Flask(__name__)

scopes = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('mapkey.json', scopes)

@app.route('/', methods=['GET'])
def index():
    return render_template('map_esri.html')

@app.route('/map', methods=['GET'])
def index():
    return render_template('map.html')

@app.route('/getmap', methods=['GET'])
def getmap():
    gc = gspread.authorize(credentials)
    wks = gc.open('iot').sheet1
    cell_dict = wks.get_all_records(empty2zero=False, head=1, default_blank='')
    list = []
    for cell in cell_dict:
        list.append({"x":float(cell["x"]), "y":float(cell["y"])})
    res = jsonify({"point":list})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
