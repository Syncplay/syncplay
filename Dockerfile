FROM ubuntu:18.04

ENV MOTD="Welcome to our Docker Syncplay server!"
ENV PORT=8999
ENV PASSWORD="changethis"
ENV SALT="changethis"

RUN apt update && apt-get install -y make python3 python3-twisted

COPY . /syncplay
WORKDIR syncplay

RUN make install

EXPOSE $PORT

RUN apt-get install -y net-tools 
HEALTHCHECK CMD netstat -tulpn | grep $PORT || exit 1

CMD echo $MOTD > motd.txt && syncplay-server --password $PASSWORD --port $PORT --salt $SALT --motd-file motd.txt
