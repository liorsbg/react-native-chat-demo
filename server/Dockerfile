FROM python:2.7-slim

ENV PORT 5050

WORKDIR /root/server
COPY . .
RUN pip install --requirement requirements.txt

EXPOSE $PORT

CMD gunicorn -b :$PORT -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app:app
