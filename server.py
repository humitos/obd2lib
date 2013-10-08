# -*- coding: utf-8 -*-

import csv
import json
import glob

from flask import Flask
from flask import render_template
from flask import make_response

from obd2lib.elmdecoder import decode_answer


def get_data_from_log(ucommand):
    # 0105 - Temperature
    # 010C - RPM
    # 010D - Speed
    with open(glob.glob('*-obd-data.log')[-1], 'rb') as csvfile:
        flines = csvfile.readlines()
        flines.reverse()
        csvreader = csv.reader(flines)
        for row in csvreader:
            # command, answer, valid, timestamp
            command, answer, valid, timestamp = row
            if command == ucommand:
                value, unit = decode_answer(command, answer)
                # print value, unit
                return value, unit


app = Flask(__name__)


@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    return response


@app.route('/getdata')
def get_data():
    data = []
    for cmd in ['0105', '010C', '010D']:
        value, unit = get_data_from_log(cmd)
        data.append({'command': cmd, 'value': value, 'unit': unit})
    response = make_response(json.dumps(data))
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    app.debug = True
    app.run()
