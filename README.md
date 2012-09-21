# Syncplay

Solution to synchronize video playback across many instances of MPlayer and Media Player Classic (MPC-HC) over a network.

## What does it do

Syncplay synchronizes the position and playback state of multiple media players so that the viewers can watch the same thing at the same time.
When one person pauses playback, the media player is paused for all users who are connected to the same server and are in the same 'room'.
When one person seeks, all players seek to the same position. When a new person joins (or someone reconnects) they will be syncronised with their fellow viewers.

## What it doesn't do

Syncplay does not provide video streaming, nor does it syncronise player configuration, selected audio or subtitle track, playback rate, volume or filters. Furthermore, the user must manually choose what file to play as Syncplay does not syncrhonise which file is open.

## Requirements

On Windows: You need the Media Player Classic Home Cinema (MPC) media player.

On Linux: You need Python 2.7, Twisted and the MPlayer media player.

## Supported players
### MPlayer on Linux

On Linux `syncplayClient.exe` acts as a wrapper for MPlayer. First two arguments are host and nickname.
The rest are arguments to be given to mplayer (at least filename). It launches mplayer
which behaves just like normal (it reacts to keyboard shortcuts etc).

Default mplayer output is suppressed, but if mplayer quits with errors, those errors
will be printed (at most 50 last lines).

### Media Player Classic Home Cinema (MPC-HC) on Windows

On Windows simply running `syncplayClient.exe` opens a command-line window for communication and an instance of MPC-HC for synbcronised video playback.

### Opening a file with Syncplay

If you open a file with `syncplayClient.exe` then it will automatically load that file in Syncplay/MPC-HC.

## Command-line switches

You can run `syncplayClient.exe` with the following command-line arguments to alter the settings:

`--no-gui` - Do not display graphical user interface (GUI)

`--host [address]` - Specify address of server to connect to (can be address:port)

`--name [name]` / `-n [name]` - Specify username to use

`--debug` / `-d` - Enable debug mode

`--force-gui-prompt` / `-g` - Force the configuration prompt to appear when Syncplay starts

`--no-store` - Disable the storing of configuration data (in .syncplay file)

`--room [room]` / `-r [room]` - Specify default room to join upon connection

`--password [password]` / `-p [password]` - Specify server password

`[file]` - File to play upon start
        

## How to use the server

You need to run `rsyncplayServer.exe` somewhere. If you have public IP, you can try to launch server on your computer
and give your friends your IP number, so they can connect to it. It will listen at port 8999, you
might need to allow connections to it in your firewall/router.

Then you launch player synchronization. When it connects and doesn't print errors about player, you are ready.
When all interested people join, you can just unpause in and it will just start to play everywhere.

