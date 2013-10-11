# -*- coding: utf-8 -*-

import json
import logging
import threading
import Queue

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask
from flask import render_template
from flask import Response
from flask import request

from obd2lib.elmdb import ELMdb
from obd2lib.elmdecoder import decode_answer


SUPPORTED_PIDS = None
QUEUE = Queue.Queue()

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    supported_pids = []
    for sp in SUPPORTED_PIDS:
        if not (
            sp in ELMdb and
            'max_value' in ELMdb[sp] and
            'min_value' in ELMdb[sp]
            ):
            continue
        try:
            supported_pids.append(dict(ELMdb[sp], pid=sp))
        except KeyError:
            logging.debug('"%s" not in ELMdb')

    data = {
        'SUPPORTED_PIDS': supported_pids,
        }
    return render_template('index.html',
                           **data)


@app.route('/post', methods=['POST'])
def post():
    global QUEUE
    data = json.loads(request.data)
    logging.info('Data received: "%s"', data)
    data['value'], data['unit'] = decode_answer(
        data['command'], data['answer'])
    logging.info('Data translated: "%s"', data)

    del data['answer']
    QUEUE.put(data)

    return Response('OK\n')


def send_data():
    global QUEUE
    while True:
        try:
            data = json.dumps(QUEUE.get(True, 1))
            data = 'data: {0}\n\n'.format(data)
            logging.info('Returning data: "%s"', data)
            yield data
        except Queue.Empty:
            pass


@app.route('/stream')
def sse_request():
    logging.info('sse_request called')
    return Response(
        send_data(),
        mimetype='text/event-stream')


class ServerMode(threading.Thread):

    def __init__(self, supported_pids):
        global SUPPORTED_PIDS
        SUPPORTED_PIDS = supported_pids

        super(ServerMode, self).__init__()

    def run(self):
        logging.info('Launching server on 127.0.0.1:5000')
        http_server = WSGIServer(('127.0.0.1', 5000), app)
        http_server.serve_forever()
