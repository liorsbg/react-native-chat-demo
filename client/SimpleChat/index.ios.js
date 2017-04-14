import React, { Component } from 'react';
import {
  AppRegistry,
  View
} from 'react-native';
import SocketIOClient from 'socket.io-client';
import { GiftedChat } from 'react-native-gifted-chat';

export default class SimpleChat extends Component {
  constructor(props) {
    super(props);
    this.state = { messages: [] };
    this.onSend = this.onSend.bind(this);
    this.onChatReceived = this.onChatReceived.bind(this);

    this.socket = SocketIOClient('http://localhost:5050/');
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
}

AppRegistry.registerComponent('SimpleChat', () => SimpleChat);
