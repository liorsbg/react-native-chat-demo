#!/bin/bash

PORT=5050

# run ngrok
./node_modules/ngrok/bin/ngrok http -log=stdout --bind-tls "true" --region eu ${PORT} > /dev/null &
sleep 3
# get and save the ngrok url
SERVER_URL=$(node -e "require('node-fetch')('http://localhost:4040/api/tunnels',{headers: {'Accept':'application/json','Content-Type': 'application/json'},}).then((resp)=> resp.json()).then((data)=>console.log(data.tunnels[0].public_url));")
echo "export const SERVER_URL = '${SERVER_URL}';" > constants.js