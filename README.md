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

`cd` to the `client/SimpleChat` folder and `npm-install`, then `react-native run-ios`


### Push Notifications and running on Device
fastlane.tools `fastlane pem` was a life saver in terms of automating [provisioning APNs SSL Certificates](https://firebase.google.com/docs/cloud-messaging/ios/certs)


