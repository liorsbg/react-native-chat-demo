Server
=======

Image is on docker hub. To run:
```
docker run -d \
    -v $PUSH_NOTIFICATION_CERTS_FOLDER:/root/cert \
    -e CERT_PATH=/root/cert/$CERT_FILE_NAME_PEM \
    -p 5050:5050 \
    liorsbg/flask-socketio-chat-server:latest
```

Then go to `http://localhost:5050/chat` in your favorite browser.
Open it in a few tabs for full effect.

Also try `curl http://localhost:5050/broadcast?message=Hello%20World!` from the command line for fun and profit.

Next, install and run the client (react native) application to have it connect and participate in the chat.

TODOs
* improve and break out notifier; run as a seperate component.
* implement room system (user can join a specific chat room)
* user management
* history and syncronization
* docker-compose with ngnix and likely redis and mongodb
* Improve hacky chat.html and serve static files with nginx


Client
======

Assuming you have React Native installed like so: https://facebook.github.io/react-native/docs/getting-started.html

1. `cd client/SimpleChat` 
2. `npm-install`
3. `npm run ngrok` (creates an web accessible tunnel to localhost:5050 for on device testing)
4. `react-native run-ios`
5. When you're done don't forget to `pkill ngrok`.

### Push Notifications and running on Device
fastlane.tools `fastlane pem` was a life saver in terms of automating [provisioning APNs SSL Certificates](https://firebase.google.com/docs/cloud-messaging/ios/certs)


