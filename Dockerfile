FROM ubuntu:18.04

ENV VERSION="v1.6.7"
ENV PASSWORD="changethis"
ENV MOTD="Welcome to our Docker Syncplay server!"
ENV PORT=8999
ENV SALT="changethis"

RUN apt update
RUN apt-get install -y make git python3 python3-twisted python3-pyside
RUN git checkout $VERSION
RUN make install

EXPOSE $PORT

CMD echo $MOTD > motd.txt && syncplay-server --password $PASSWORD --port $PORT --salt $SALT --motd-file motd.txt
