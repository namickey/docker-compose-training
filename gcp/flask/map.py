# -*- coding: utf-8 -*-
import logging
from flask import Flask, jsonify, request
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route('/getmap', methods=['GET'])
def getmap():
    res = jsonify({"point":[\
        {"x":35.69, "y":139.7},\
        {"x":35.61, "y":139.6}\
        ]})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
