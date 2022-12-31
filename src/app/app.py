from flask import Flask, render_template, request
from bluetooth.main import properties, buffer, modulator, demodulator, sender, receiver, encoder, decoder
from queue import Empty
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/bluetooth')
def bluetooth():
    return render_template('bluetooth.html')

@app.get('/distance')
def distance():
    return render_template('distance.html')


@app.post('/sender')
def send():
    data = request.json
    if data['action'] == 'play':
        print('Playing:', data['text'])
        encoder.encode(data['text'])
    elif data['action'] == 'stop':
        print('Stopping play')
        encoder.stop()
    return 'ok'

@app.post('/receiver')
def receive():
    data = request.json
    if data['action'] == 'receive':
        decoder.decode()
    elif data['action'] == 'stop':
        decoder.stop()
    elif data['action'] == 'read':
        return decoder.get(), 200 if decoder.running() else 400

    return 'ok'


@app.errorhandler(404)
def page_not_found(request, exception=None):
    return render_template('404.html')