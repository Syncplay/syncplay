#  Syncplay

Solution to synchronize video playback across multiple instances of mplayer2 and/or Media Player Classic (MPC-HC) over the Internet.

## Notice
No official builds of Syncplay have been released yet. If you want the current beta then compile it yourself from the official branch or check out the #syncplay IRC channel on irc.rizon.net.

## What does it do

Syncplay synchronises the position and play state of multiple media players so that the viewers can watch the same thing at the same time.
This means that when one person pauses/unpauses playback or seeks (jumps position) within their media player then this will be replicated across all media players connected to the same server and in the same 'room' (viewing session).
When a new person joins they will also be synchronised.

## What it doesn't do

Syncplay does not use video streaming or file sharing so each user must have their own copy of the media to be played. Syncplay does not synchronise player configuration, audio or subtitle track choice, playback rate, volume or filters. Furthermore, users must manually choose what file to play as Syncplay does not synchronise which file is open. Finally, Syncplay does not provide a voice or text-based chat platform to allow for discussion during playback as Syncplay is intended to be used in conjunction with third-party communication solutions such as IRC and Mumble.

## Requirements
Frozen Windows executables are available on the download page - https://github.com/Uriziel/syncplay/downloads

* On Windows: `Media Player Classic - Home Cinema (MPC-HC)` >= `1.6.4`.
* On Linux: `mplayer2`. `MPlayer` >= `1.1` should be compatible, but is not supported.

### Python scripts (for those not using the frozen executable package)

If you are not using the frozen executable package then you will need the following to run Python scripts:

* `pygtk` >= `2.0.0` (unless started with `--no-gui`)
* `argparse` >= `1.1`
* `pywin32` >= `r217` (MPC-HC, Windows only)
* `twisted` >= `12.1.0`

If you are using the frozen executable package available from the download page then you will not need to be able to run Python scripts.

## Supported players
### mplayer2 on Linux

On Linux `syncplay` acts as a front-end for mplayer2. 
To use it select "Open with..." in context menu and choose `Syncplay` or from command line: "syncplay video_filename". If you wish to pass more arguments to mplayer2 prepend them with -- argument, it's treated as the last argument for wrapper.

Default mplayer2 output is suppressed, but if mplayer2 quits with errors, those errors will be printed (at most 50 last lines).

### Media Player Classic - Home Cinema (MPC-HC) on Windows

On Windows simply running `syncplayClient.exe` opens a Syncplay command-line window for communication/control and a new instance of MPC-HC for synchronised video playback. This instance of MPC-HC is controlled by Syncplay through the associated command-line window, but other instances of MPC-HC will be unaffected.

## Using Syncplay

### Getting started with Syncplay on Windows

1. Ensure that you have the latest version of `Media Player Classic - Home Cinema (MPC-HC)` installed. The latest stable build is `1.6.4`.

2. Download Syncplay frozen executable package from https://github.com/Uriziel/syncplay/downloads and extract to a folder of your choosing.

3. If you are running your own server then open `syncplayServer.exe` (see "How to use the server", below).

4. Open `syncplayClient.exe` (or open the media file you wish to play with `syncplayClient.exe`, e.g. using "Open with").

5. Enter configuration settings (see "Configuration window", below). Ensure that you are on the same server and room as your fellow viewers.

6. If you don't have the file you want to play open then open it from within the MPC-HC instance initiated by Syncplay.

7. Playing, pausing and seeking from within the MPC-HC instance should now be synchronised with everyone else in the same 'room'.

### Getting started with Syncplay on Linux

1. Ensure that you have an up to date version of `mplayer2` and relevant python libraries (see "Python scripts", above) installed.

2. Download Syncplay tarball from https://github.com/Uriziel/syncplay/downloads and run `make install-client` (or `make install-all` if you also want server).

3. Open the media file you wish to play with `syncplay` (e.g. using "Open with...").

4. Enter configuration settings (see "Configuration window", below). Ensure that you are on the same server and room as your fellow viewers. This is done only once, configuration is kept in `~/.syncplay` file.

5. Playing, pausing and seeking from within the mplayer2 instance should now be synchronised with everyone else in the same 'room'.

### Opening a media file with Syncplay

Opening a file with `syncplayClient` (`Syncplay` on Linux) will automatically run Syncplay and load the file through MPC-HC on Windows or mplayer2 on Linux.

### Configuration window
The configuration window allows for various settings to be configured prior to Syncplay starting.

The window will appear if you:

1. Run `syncplayClient`  without settings being configured, e.g. on first boot,
2. Run `syncplayClient` with the `--force-gui-prompt` or `-g` commandline switches, or
3. Run `syncplayClientForceConfiguration`.

The settings to be configured are as follows:

* `Host` - Address (hostname / IP) of server to connect to (optionally with port), e.g. `localhost:2734` or `192.168.0.1`. Default port is `8999`.
* `Username` - Name that the server and other viewers know you by.
* `Default room (optional)` - Room to join upon connection. You will only be synchronised with others in the same room on the same server. Default room is `default`.
* `Server password (optional)` - Password for server. Servers that are not password protected have a blank password.
* `Path to mpc-hc.exe [Windows only]` - Location of the MPC-HC executable (mpc-hc.exe or mpc-hc64.exe). If this is in a common location then it will be filled in by default. Users are advised to check that it points to their desired installation.

Pressing "Save" will save the settings and continue Syncplay start-up.

### Syncplay Commands

Within the Syncplay command-line you can enter the following commands (and then press enter) to access features:

* `help` - Displays list of commands and other information.
* `room [room]` - Leaves current room and joins specified room. You are only synchronised with others in the same room on the same server. If no room is specified then this command will use the filename of the currently open file, or alternatively will join the room `default`.
* `[s][+-][time]` - Seek (jump) to specified time. Optional `+` or `-` denotes relative time forward and backward respectively. Time can be given in seconds or min:sec format.
* `r` - Revert last seek. Seeks to where you were before the most recent seek.
* `p` - Toggle play/pause.

### Command-line switches

You can run `syncplayClient` with the following command-line switches to alter Syncplay settings or behaviour:

* `--no-gui` - Do not display graphical user interface (GUI)
* `--host [address]` - Specify address of server to connect to (can be `address:port`)
* `--name [name]` / `-n [name]` - Specify username to use
* `--debug` / `-d` - Enable debug mode
* `--force-gui-prompt` / `-g` - Force the configuration window to appear when Syncplay starts
* `--no-store` - Disable the storing of configuration data (in .syncplay file)
* `--room [room]` / `-r [room]` - Specify default room to join upon connection.
* `--password [password]` / `-p [password]` - Specify server password
* `[file]` - File to play upon start
* `--` - used as a last argument for syncplayClient, used to prepend arguments that are meant to be passed to player

### Notification messages

* `Rewinded due to time difference  with [user]` - This means that your media player ended up too far in front of the specified user and has jumped back to keep you in sync. This is usually because someone's computer isn't powerful enough to play the file smoothly.
* `File you're playing is different from [user]'s` - This means that the filename, length and/or duration of the file that the user is playing is different from the file that you are playing. This is for information only and is not an error.
       
## How to use the server

Run `syncplayServer` to host a Syncplay server. If you have a public IP then you can try to launch the server on your computer
and give your friends your IP number so that they can connect to it. The server software will listen on port `8999` by default, but you can specify a different port. You might need to specifically allow connections to `syncplayServer` in your firewall/router. If that is the case then please consult your firewall/router instructions or contact your network administrator.

Pass the IP or hostname (and password / port if necessary) to people you want to watch with and you're ready to go. There are various online services that will tell you what your IP address is.

### Server command-line switches

* `--port [port]` - Use stated port instead of the default one.
* `--isolate-room` - If specified then 'room isolation' is enabled. This means that viewers will not be able to see information about users who are in rooms other than the one they are in. This feature is recommended for a public server, but not for a small private server.
* `--password [password]` - Restrict access to the Syncplay server to only those who use this password when they connect to the server. This feature is recommended for a private server but is not needed for a public server. By default the password is blank (i.e. there is no password restriction).

## Syncplay behaviour
The following information is sent from the client to the server:
* Public IP address of client and other necessary routing information (as per TCP/IP standards).
* Media position, play state, and any seek/pause/unpause commands (associated with the instance of the media player initiated by Syncplay).
* Size, length, and optionally filename of currently open media (associated with the instance of the media player initiated by Syncplay).
* Syncplay version, username, server password and current 'room'.
* Ping responses to assess latency.

Note: The current official build of the Syncplay server does not store any of this information. However, some of the information (not the IP address) is passed on to other users connected to the server (or just to those in the same room if 'isolation' mode is enabled).

The server has the ability to control the following aspects of the instance of the media player initiated by Syncplay:
* Current position (seek commands).
* Current play state (pause and unpause commands).

The client affects the following files:
* Modifying .syncplay file in %APPDATA% (or $HOME on Linux version) folder to store configuration information.

Note: This behaviour can be disabled by using the `--no-store` command-line switch (see "Command-line switches", above)

## How to report bugs

You can report bugs through https://github.com/Uriziel/syncplay/issues but first please check to see if your problem has already been reported.

You might also be able to discuss your problem through Internet Relay Chat (IRC). The #Syncplay channel is on the irc.rizon.net server.

### Known issues
1. Changing your system time while Syncplay is running confuses the sync. PROTIP: Don't do it.
2. Syncplay cannot properly handle a seek that is within 8 seconds of the current position. PROTIP: Don't do it.
