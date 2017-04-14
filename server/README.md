Flask-SocketIO Demo Server
==========================

Image is on docker hub. To run:
`docker run -d -p 5050:5050 liorsbg/flask-socketio-chat-server:1`

Then go to `http://localhost:5050/chat` in your favorite browser (hopefully Chrome).
Open it in a few tabs for full effect.

Also try `curl http://localhost:5050/broadcast?message=Hello%20World!` for fun and profit.

Next, install and run the client (react native) application to have it connect and participate in the chat.

TODOs
* implement room system (user can join a specific chat room)
* user management
* history and syncronization
* docker-compose with ngnix and likely redis and mongodb
* Improve hacky chat.html and serve static files with nginx
