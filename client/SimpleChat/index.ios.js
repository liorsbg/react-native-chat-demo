import React, { Component } from 'react';
import {
  AppRegistry,
  View,
  PushNotificationIOS,
  AlertIOS
} from 'react-native';
import SocketIOClient from 'socket.io-client';
import { GiftedChat } from 'react-native-gifted-chat';

export default class SimpleChat extends Component {
  constructor(props) {
    super(props);
    this.state = { messages: [] };
    this.onSend = this.onSend.bind(this);
    this.onChatReceived = this.onChatReceived.bind(this);
    this._onRegistered = this._onRegistered.bind(this);

    this.socket = SocketIOClient('https://9494294e.ngrok.io');
    this.socket.on('chat', (message) => {
      this.setState((previousState) => {
        return { messages: GiftedChat.append(previousState.messages, message) };
      });
    });
  }

  componentWillMount() {
    this.setState({
      user: { _id: "rn", name: "React Native" },
      messages: [
        {
          _id: 0, text: 'Welcome!',
          user: {
            _id: "aa",
            name: 'Admin Admin',
          },
        }],
    });

    PushNotificationIOS.addEventListener('register', this._onRegistered);
    PushNotificationIOS.addEventListener('registrationError', this._onRegistrationError);
    PushNotificationIOS.addEventListener('notification', this._onRemoteNotification);
    PushNotificationIOS.addEventListener('localNotification', this._onLocalNotification);
    PushNotificationIOS.requestPermissions();
  }

  componentWillUnmount() {
    PushNotificationIOS.removeEventListener('register', this._onRegistered);
    PushNotificationIOS.removeEventListener('registrationError', this._onRegistrationError);
    PushNotificationIOS.removeEventListener('notification', this._onRemoteNotification);
    PushNotificationIOS.removeEventListener('localNotification', this._onLocalNotification);
  }

  onChatReceived(message) {
    this.setState((previousState) => {
      return { messages: GiftedChat.append(previousState.messages, message) };
    });
  }

  onSend(messages) {
    for (message of messages) {
      this.socket.emit('chat', message);
    }
  }

  render() {
    return (
      <GiftedChat
        messages={this.state.messages}
        onSend={this.onSend}
        user={this.state.user}
      />
    );
  }


  _onRegistered(deviceToken) {
    console.log(deviceToken);
    this.onChatReceived({
      _id: 1,
      text: `Registered for Notifications with token: ${deviceToken}`,
      createdAt: new Date(),
      user: {
        _id: 'admin',
        name: 'Admin Admin',
        avatar: 'https://facebook.github.io/react/img/logo_og.png',
      },
    });
    AlertIOS.alert(
      'Registered For Remote Push',
      `Device Token: ${deviceToken}`,
      [{
        text: 'Dismiss',
        onPress: null,
      }]
    );
  }

  _onRegistrationError(error) {
    AlertIOS.alert(
      'Failed To Register For Remote Push',
      `Error (${error.code}): ${error.message}`,
      [{
        text: 'Dismiss',
        onPress: null,
      }]
    );
  }

  _onRemoteNotification(notification) {
    AlertIOS.alert(
      'Push Notification Received',
      'Alert message: ' + notification.getMessage(),
      [{
        text: 'Dismiss',
        onPress: null,
      }]
    );
  }

}

AppRegistry.registerComponent('SimpleChat', () => SimpleChat);
