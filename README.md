# Syncplay

Solution to synchronize video playback across many instances of MPlayer and Media Player Classic (MPC-HC) over a network.

## What does it do

Syncplay synchronizes the position and playback state of multiple media players so that the viewers can watch the same thing at the same time.
When one person pauses playback, the media player is paused for all users who are connected to the same server and are in the same 'room'.
When one person seeks, all players seek to the same position. When a new person joins (or someone reconnects) they will be syncronised with their fellow viewers.

## What it doesn't do

Syncplay does not provide video streaming, nor does it syncronise player configuration, selected audio or subtitle track, playback rate, volume or filters. Furthermore, the user must manually choose what file to play as Syncplay does not syncrhonise which file is open.

## Requirements

On Windows: You need the Media Player Classic Home Cinema (MPC-HC) media player.

On Linux: You need Python 2.7, Twisted and the MPlayer media player.

## Supported players
### MPlayer on Linux

<TO UPDATE>

On Linux `syncplayClient.exe` acts as a wrapper for MPlayer. First two arguments are host and nickname.
The rest are arguments to be given to mplayer (at least filename). It launches mplayer
which behaves just like normal (it reacts to keyboard shortcuts etc).

Default mplayer output is suppressed, but if mplayer quits with errors, those errors
will be printed (at most 50 last lines).

### Media Player Classic Home Cinema (MPC-HC) on Windows

On Windows simply running `syncplayClient.exe` opens a command-line window for communication and an instance of MPC-HC for synbcronised video playback.

## Using Syncplay

### Opening a media file with Syncplay

If you open a file with `syncplayClient.exe` then it will automatically open Syncplay and load the file through MPC-HC on Windows and MPlayer on Linux.

### Command-line switches

You can run `syncplayClient.exe` with the following command-line arguments to alter the settings:

`--no-gui` - Do not display graphical user interface (GUI)

`--host [address]` - Specify address of server to connect to (can be address:port)

`--name [name]` / `-n [name]` - Specify username to use

`--debug` / `-d` - Enable debug mode

`--force-gui-prompt` / `-g` - Force the configuration window to appear when Syncplay starts

`--no-store` - Disable the storing of configuration data (in .syncplay file)

`--room [room]` / `-r [room]` - Specify default room to join upon connection. If no room is specified then it will use the filename of the currently playing file, or alternatively will join the default room if no file is playing.

`--password [password]` / `-p [password]` - Specify server password

`[file]` - File to play upon start

### Configuration window
The configuration window allows for various settings to be configured prior to Syncplsy starting.

The window will appear if you:

1. Run `syncplayClient.exe`  without settings being configured, e.g. on first boot,

2. run `syncplayClient.exe` with the `--force-gui-prompt` or `-g` commandline swtiches, or

3. Run `syncplayClientForceConfiguration.exe`.

The settings to be configured are as follows:

`Host` - Address (hostname / IP) of server to connect to (optionally with port), e.g. `localhost:2734` or `192.168.0.1`. Default port is `8999`.

`Username` - Name that the server and other viewers know you by

`Default room (optional)` - Room to join upon connection. You will only be syncronised with others on the same room on the same server. Default room is `default`.

`Server password (optional)` - Password for server. Servers that are not password protected have a blank password.

`Path to mpc-hc.exe [Windows only]` - Location of the MPC-HC executable (mpc-hc.exe or mpc-hc64.exe). If this is in a common location then it will be filled in by default.

Pressing "Save" will save the settings and continue Syncplay start-up.

### Syncplay Commands

Within the Syncplay commandline you can enter the following commaands (and then press enter) to access features:

`help` - Displays list of commands and other information.

`room [room]` - Leaves current room and joins specified room. You are only syncronised with others on the same room on the same server.

`s [time]` - Seek (jump) to specified time. Can be `seconds`, `minutes:seconds` or `hours:minutes:seconds`.

`s+ [time]` - Jumps [time] forward. Can be `seconds`, `minutes:seconds` or `hours:minutes:seconds`.

`r` - Revert last seek. Seeks to where you were before the most recent seek.

`p` - Toggle play/pause.

## Instructions on how to use Syncplay for the first time

1. Ensure you have the latest version of MPC-HC on Windows of MPlayer on Linux.

2. Download Syncplay from https://github.com/Uriziel/syncplay/downloads

3. Extract Syncplay to a folder of your choosing.

4. If you are using a private server then ensure the server is running `syncplayServer.exe` (see "How to use the server", below)

5. Open `syncplayClient.exe` (or open the media file you wish to play with `syncplayClient.exe`, e.g. using "Open with")

6. Enter configuration settings (see "Configuration window", above).

7. If your friends are not in the same room as you then use the room command (see "Syncplay Commands", above)

8. If you don't have the file you want to play open then open it from within your media player.
        
## How to use the server

<TO UPDATE>

You need to run `syncplayServer.exe`. If you have a public IP then you can try to launch server on your computer
and give your friends your IP number, so they can connect to it. It will listen at port `8999`, you
might need to allow connections to it in your firewall/router.

Then you launch player synchronization. When it connects and doesn't print errors about player, you are ready.
When all interested people join, you can just unpause in and it will just start to play everywhere.

## How to report bugs

<TO DO>
