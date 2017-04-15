FROM python:2.7-slim

# For push notification, set variable and mount a volume containg the certificate
ENV CERT_PATH /root/cert

WORKDIR /root/server
COPY . .
RUN pip install --requirement requirements.txt

EXPOSE 5050

CMD gunicorn -b :5050 \
            -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
            -w 1 \
            --env CERT_PATH=$CERT_PATH \
            app:app