# Syncplay

Solution to synchronize video playback across multiple instances of MPlayer and/or Media Player Classic (MPC-HC) over the Internet.

## What does it do

Syncplay synchronises the position and play state of multiple media players so that the viewers can watch the same thing at the same time.
When one person pauses playback, the media player is paused for all users who are connected to the same server and are in the same 'room' (viewing session).
When one person seeks, all players seek to the same position. When a new person joins they will be synchronised with their fellow viewers.

## What does it not do

Syncplay does not provide video streaming, nor does it synchronise player configuration, selected audio or subtitle track, playback rate, volume or filters. Furthermore, the user must manually choose what file to play as Syncplay does not synchronise which file is open. Finally, Syncplay does not provide a voice or text-based chat platform to allow for discussion during playback as Syncplay is intended to be used in conjunction with third-party communication software such as IRC, Mumble or Skype.

## Requirements
Frozen Windows executables are available on download page - https://github.com/Uriziel/syncplay/downloads

On Windows: You need Media Player Classic - Home Cinema (MPC-HC) >= `1.6.3`.

On Linux: mplayer >= `1.1`.

For running python script you need (not needed if using frozen executable package from download page):

`pygtk` >= `2.0.0` (unless started with `--no-gui`)

`argparse` >= `1.1`

`pywin32` >= `r217` (mpc-hc, Windows only)

`twisted` >= `12.1.0`

## Supported players
### MPlayer on Linux

<TO UPDATE>

On Linux `syncplayClient.exe` acts as a wrapper for MPlayer. First two arguments are host and nickname.
The rest are arguments to be given to mplayer (at least filename). It launches mplayer
which behaves just like normal (it reacts to keyboard shortcuts etc).

Default mplayer output is suppressed, but if mplayer quits with errors, those errors
will be printed (at most 50 last lines).

### Media Player Classic Home Cinema (MPC-HC) on Windows

On Windows simply running `syncplayClient.exe` opens a Syncplay command-line window for communication and an instance of MPC-HC for synchronised video playback. This instance of MPC-HC is controlled by Syncplay through the associated command-line window, but other instances of MPC-HC will be unaffected.

## Using Syncplay

### Opening a media file with Syncplay

If you open a file with `syncplayClient.exe` then it will automatically open Syncplay and load the file through MPC-HC on Windows and MPlayer on Linux.

### Configuration window
The configuration window allows for various settings to be configured prior to Syncplay starting.

The window will appear if you:

1. Run `syncplayClient.exe`  without settings being configured, e.g. on first boot,

2. Run `syncplayClient.exe` with the `--force-gui-prompt` or `-g` commandline switches, or

3. Run `syncplayClientForceConfiguration.exe`.

The settings to be configured are as follows:

`Host` - Address (hostname / IP) of server to connect to (optionally with port), e.g. `localhost:2734` or `192.168.0.1`. Default port is `8999`.

`Username` - Name that the server and other viewers know you by.

`Default room (optional)` - Room to join upon connection. You will only be synchronised with others in the same room on the same server. Default room is `default`.

`Server password (optional)` - Password for server. Servers that are not password protected have a blank password.

`Path to mpc-hc.exe [Windows only]` - Location of the MPC-HC executable (mpc-hc.exe or mpc-hc64.exe). If this is in a common location then it will be filled in by default.

Pressing "Save" will save the settings and continue Syncplay start-up.

### Syncplay Commands

Within the Syncplay command-line you can enter the following commands (and then press enter) to access features:

`help` - Displays list of commands and other information.

`room [room]` - Leaves current room and joins specified room. You are only synchronised with others in the same room on the same server. If no room is specified then it will use the filename of the currently playing file, or alternatively will join the default room if no file is playing.

`s [time]` - Seek (jump) to specified time. Can be `seconds`, `minutes:seconds` or `hours:minutes:seconds`.

`s+ [time]` - Jumps [time] forward. Can be `seconds`, `minutes:seconds` or `hours:minutes:seconds`.

`r` - Revert last seek. Seeks to where you were before the most recent seek.

`p` - Toggle play/pause.

### Instructions on how to use Syncplay for the first time

1. Ensure that you have the latest version of MPC-HC on Windows or MPlayer on Linux.

2. Download Syncplay from https://github.com/Uriziel/syncplay/downloads and extract to a folder of your choosing.

3. If you are running your own server then open `syncplayServer.exe` (see "How to use the server", below)

4. Open `syncplayClient.exe` (or open the media file you wish to play with `syncplayClient.exe`, e.g. using "Open with")

5. Enter configuration settings (see "Configuration window", above).

6. If your fellow viewers are not in the same 'room' as you then use the room command (see "Syncplay Commands", above)

7. If you don't have the file you want to play open in your media player then open it from within your media player.

### Command-line switches

You can run `syncplayClient.exe` with the following command-line switches to alter Syncplay settings or behaviour:

`--no-gui` - Do not display graphical user interface (GUI)

`--host [address]` - Specify address of server to connect to (can be address:port)

`--name [name]` / `-n [name]` - Specify username to use

`--debug` / `-d` - Enable debug mode

`--force-gui-prompt` / `-g` - Force the configuration window to appear when Syncplay starts

`--no-store` - Disable the storing of configuration data (in .syncplay file)

`--room [room]` / `-r [room]` - Specify default room to join upon connection.

`--password [password]` / `-p [password]` - Specify server password

`[file]` - File to play upon start

### Error messages and notifications

"Rewinded due to time difference" - This means that your media player ended up too far in front of at least one other viewer and has jumped back to keep you in sync. This is usually because someone's computer isn't powerful enough to play the file smoothly.
       
## How to use the server

<TO UPDATE>

You need to run `syncplayServer.exe`. If you have a public IP then you can try to launch server on your computer
and give your friends your IP number, so they can connect to it. It will listen at port `8999`, you
might need to allow connections to it in your firewall/router.

Then you launch player synchronization. When it connects and doesn't print errors about player, you are ready.
When all interested people join, you can just unpause in and it will just start to play everywhere.

## How to report bugs

You can report bugs through https://github.com/Uriziel/syncplay/issues but first please check to see if your problem has already been reported.

You might also be able to discuss your problem through Internet Relay Chat (IRC). The #Syncplay channel is on the irc.rizon.net server.
