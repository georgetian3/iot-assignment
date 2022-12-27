from flask import Flask, render_template, request
from bluetooth.main import properties, buffer, modulator, demodulator, sender, receiver, encoder, decoder
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
        sender.send(data['text'])
    elif data['action'] == 'stop':
        print('Stopping play')
        sender.stop()
    return 'ok'

@app.post('/receiver')
def receive():
    data = request.json
    if data['action'] == 'receive':
        receiver.receive(buffer)
    elif data['action'] == 'stop':
        receiver.stop()
    elif data['action'] == 'read':
        chars = []
        end = False
        try:
            while True:
                char = buffer.get_nowait()
                if char == 0:
                    end = True
                else:
                    chars.append(char)
        except Empty:
            pass
        return ''.join(chars), 400 if end else 200

    return 'ok'


@app.errorhandler(404)
def page_not_found(request, exception=None):
    return render_template('404.html')