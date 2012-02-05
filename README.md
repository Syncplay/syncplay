# SyncPlay

Solution to synchronize video playback across many instances of mplayer and Media Player Classic (MPC-HC) over the network.

## Motivation

1. Watching videos with friends and commenting them live on IRC or Mumble
1. Do something for lulz and to learn new stuff

## What does it do

It synchronizes many media players, so many people can watch the same movie at the same moment.
When one person pauses playback, it gets paused in all players. When one person seeks,
all players seek to the same position. When new person joins to the watching session which
runs for a while, his player starts playback at the moment where other people are.

## Requirements

All you need is Python 2.7 and Twisted to run python scripts.

### Windows

Because setting up Python and installing requirements under Windows is a bit hard,
I'll provide download links to "ready to use" package when it gets stable.

If you still want to run it from sources, apart from Python and Twisted you'll
probably need to instal manually setuptools and zope.interface packages. Additionaly
you can install py2exe to make "all in one" redistributable package.

## Supported players

### Mplayer

`sync_mplayer` acts as a wrapper for mplayer. First two arguments are host and nickname.
The rest are arguments to be given to mplayer (at least filename). It launches mplayer
which behaves just like normal (it reacts to keyboard shortcuts etc).

Default mplayer output is suppressed, but if mplayer quits with errors, those errors
will be printed (at most 50 last lines).

### Media Player Classic Home Cinema (MPC-HC)

`sync_mpc` connects to MPC via its Web Interface. You need to enable it first in settings
(check "Listen on port" with default port which is 13579 and to be more secure check
"Allow access from localhost only"). You need to run MPC and open the file first, then launch syncplay.

You need to provide two argument to `sync_mpc`: hostname to conect to and nickname.
If hostname and nickname doesn not change, you can create shortcut to executable somewhere, edit it
and append those two arguments to command.

## How to use it

You need to run `run_sync_server` somewhere. If you have public IP, you can try to launch server on your computer
and give your friends your IP number, so they can connect to it. It will listen at port 8999, you
might need to allow connections to it in your firewall/router.

Then you launch player synchronization. When it connects and doesn't print errors about player, you are ready.
When all interested people join, you can just unpause in and it will just start to play everywhere.

