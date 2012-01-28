# SyncPlay

Solution to synchronize video playback across many instances mplayer and media player classic

## Motivation

Watching videos with friends and commenting them live on IRC or Mumble

## Solution

One of the users sets up a server. It keeps track of clients's playback position and paused status.

Client connecting to the server identifies itself with some name (user nickname for example) so other peers will know who connected/started/paused playback.
After identifying server sends current state: is movie paused, on what position it currently is, and who was the last one to change playback state. Client also receives current state after sending his own state update, after global state change and after other client update (with predefined shortest time between messages).
Every some predefined period of time client sends its own state. If global state is paused, and his is playing (or other way around), and he was the last one to change the global state (or few seconds passed since then), state is changed and broadcasted to connected clients.

(tbc)

## Protocol

Protocol is line-based. First word is "command", the rest are the command arguments, space-separated.

### Client to server

    iam name

Client identifies itself with a name. After sending this line he receives from server `state` line, and can send other commands.

    state playback_state position

`playback_state` can be either `playing` or `paused`, positon is fixed point integer - playback position in seconds with two fraction digits. Value `1200` equals 12 seconds.

(tbc)

### Server to client

    state playback_state position [name]

Similar to client's `state` command, with exception of optional name at the end - clients may use it to display who paused/resumed playback.

(tbc)

## TODO

1. Implement seek
1. Implement "knowing" what filename is played
1. Implement client side
1. Implement mplayer master
1. Implement mpc client
