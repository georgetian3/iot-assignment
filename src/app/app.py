from flask import Flask, render_template, request, redirect
from bluetooth.main import encoder, decoder
from queue import Empty
from distance.sender import Sender
from distance.receiver import Receiver
from threading import Thread
import logging
class ThreadWithReturnValue(Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
 
    def join(self):
        super(ThreadWithReturnValue,self).join()
        return self._return
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.get('/')
def home():
    return redirect('/bluetooth')

@app.get('/index')
def index():
    return render_template('index.html')

@app.get('/bluetooth')
def bluetooth():
    return render_template('bluetooth.html')

@app.get('/distance')
def distance():
    return render_template('distance.html')


@app.post('/bt-sender')
def bt_sender():
    data = request.json
    if data['action'] == 'play':
        encoder.encode(data['text'])
    elif data['action'] == 'stop':
        encoder.stop()
    return 'ok'

@app.post('/bt-receiver')
def bt_receiver():
    data = request.json
    if data['action'] == 'receive':
        decoder.decode()
    elif data['action'] == 'stop':
        decoder.stop()
    elif data['action'] == 'read':
        return decoder.get(), 200 if decoder.running() else 400
    return 'ok'

""" @app.post('/dist-sender')
def dist_sender():
    data = request.json
    print(data)
    if data['action'] == 'send':
        sender = Sender(data['port'],data['aa'],data['bb'])
        thread = ThreadWithReturnValue(target=sender.main())
        thread.start()
        #result = thread.join()
        result = '1'
        print(f'result is {result}')
        return result,200
    print('dist sender')
    return 'ok'

@app.post('/dist-receiver')
def dist_receiver():
    data = request.json
    if data['action'] == 'receive':
        receiver = Receiver(data['ip'],data['port'])
        thread = Thread(target=receiver.main())
        thread.start()
        print('started receiver thread')
        #thread.join()
    print('dist receiver')
    return 'ok'

 """