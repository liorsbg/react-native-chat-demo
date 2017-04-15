from gevent import monkey
monkey.patch_all()

import uuid
import json
from datetime import datetime
from collections import defaultdict
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import notifier

app = Flask(__name__)
socketio = SocketIO(app)

connected_clients = set()

# Keep track of token/session relationships for push notifications.
# If a token has no connected sessions it should be sent a push notification.
registered_token_sessions = defaultdict(set)
session_tokens = {}


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/chat/')
def web_chat():
    return render_template('chat.html')


@app.route('/broadcast', methods=['GET', 'POST'])
def broadcast():
    """
    Allows triggering from other processes/servers, e.g.:
    http://localhost:5050/broadcast?message=Hello%20World!
    """
    if request.method == 'GET':
        text = request.args.get('message')
    else:
        text = json.loads(request.data).get('message')
    message = new_message(text)
    socketio.emit('chat', message)
    notify_disconnected(message)
    return "Broadcast \"{0}\" to {1} devices.".format(message, len(connected_clients))


@socketio.on('connect')
def on_connect():
    connected_clients.add(request.sid)
    print "{} connected".format(request.sid)
    # Use `room` arg to send only to user who just connected
    socketio.emit('get-id', str(request.sid), room=str(request.sid))


@socketio.on('register')
def on_register(token):
    registered_token_sessions[token].add(request.sid)
    session_tokens[request.sid] = token
    print registered_token_sessions


@socketio.on('disconnect')
def on_disconnect():
    connected_clients.remove(request.sid)
    token = session_tokens.pop(request.sid, None)
    if token:
        registered_token_sessions[token].remove(request.sid)
    print "{} disconnected".format(request.sid)


@socketio.on('chat')
def on_chat(message):
    print "Received: {}".format(message)
    if "_id" not in message:
        message["_id"] = str(uuid.uuid1())

    # This is giving an error. TODO: find alternative to offload notification as it can hang
    # notify_thread = socketio.server.start_background_task(notify_disconnected, message)
    socketio.emit('chat', message)
    notify_disconnected(message)


def notify_disconnected(message):
    """
    Figure out which devices are not currently connected and notify them of the new message.
    This is not strictly necessary (we could just notify everyone all the time), but greatly
    reduces the number of notifications. Also, notification timing is not deterministic, so
    this can prevent situations where users receive delayed notification for messages they've
    already seen after they leave the app.
    """
    for token, sid_list in registered_token_sessions.iteritems():
        all_disconnected = all(not socketio.server.manager.is_connected(sid, request.namespace)
                               for sid in sid_list)
        if all_disconnected:
            notifier.send_message(token, message)


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
