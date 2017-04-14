from gevent import monkey
monkey.patch_all()

import uuid
import json
from datetime import datetime
from flask import Flask, render_template, request
from flask_socketio import SocketIO, rooms

app = Flask(__name__)
socketio = SocketIO(app)
clients = set()


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/chat/')
def web_chat():
    return render_template('chat.html')


@app.route('/broadcast', methods=['GET', 'POST'])
def broadcast():
    if request.method == 'GET':
        message = request.args.get('message')
    else:
        message = json.loads(request.data).get('message')
    socketio.emit('chat', new_message(message))
    return "Broadcast \"{0}\" to {1} devices.".format(message, len(clients))


@socketio.on('connect')
def on_connect():
    clients.add(request.sid)
    # Send only to user who just connected
    socketio.emit('get-id', str(request.sid), room=str(request.sid))


@socketio.on('disconnect')
def on_disconnect():
    clients.remove(request.sid)


@socketio.on('chat')
def on_chat(message):
    print "Received: {}".format(message)
    if "_id" not in message:
        message["_id"] = str(uuid.uuid1())

    socketio.emit('chat', message)


def new_message(text):
    msg = {
        "_id": str(uuid.uuid1()),
        "text": text,
        "createdAt": datetime.utcnow().isoformat(),
        "user": {
            "_id": "admin",
            "name": 'Admin Admin'
        }
    }
    return msg


if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5000)
