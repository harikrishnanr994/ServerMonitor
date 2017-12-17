import socketio
import eventlet
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid , environ)

@sio.on('send_details')
def message(sid, data):
    print ('message ', data)
    print 'host : ',data['host']
    print 'domain : ',data['domain']
    print 'email : ',data['email']
    print 'username : ',data['username']

    sio.emit('message_received', data)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
