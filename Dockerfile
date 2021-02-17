FROM ubuntu:18.04

ENV MOTD="Welcome to our Docker Syncplay server!"
ENV PORT=8999
ENV PASSWORD="changethis"
ENV SALT="changethis"

RUN apt update
RUN apt-get install -y make python3 python3-twisted python3-pyside

COPY . /syncplay
RUN cd syncplay && make install

EXPOSE $PORT

CMD echo $MOTD > motd.txt && syncplay-server --password $PASSWORD --port $PORT --salt $SALT --motd-file motd.txt
