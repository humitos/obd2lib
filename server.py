# -*- coding: utf-8 -*-

import json
import logging
import Queue

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask
from flask import render_template
from flask import make_response
from flask import Response
from flask import request

from obd2lib.elmdecoder import decode_answer

QUEUE = Queue.Queue()

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    return response


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


if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',
        level=logging.DEBUG)

    logging.info('Launching server on 127.0.0.1:5000')
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
