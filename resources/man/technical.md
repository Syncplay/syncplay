## Syncplay behaviour

The following information is sent from the client to the server:

*   Public IP address of client and other necessary routing information (as per TCP/IP standards).
*   Media position, play state, and any seek/pause/unpause commands (associated with the instance of the media player initiated by Syncplay).
*   Size, duration, and filename of currently open media (associated with the instance of the media player initiated by Syncplay).
*   Syncplay version, username, server password and current 'room' * Ping responses to assess latency.

Note: The current official build of the Syncplay server does not store any of this information. However, some of the information (not the IP address) is passed on to other users connected to the server (or just to those in the same room if 'isolation' mode is enabled).

The server has the ability to control the following aspects of the instance of the media player initiated by Syncplay:

*   Current position (seek commands).
*   Current play state (pause and unpause commands).

The following aspects of the media player are affected, but not controlled, by the server:

*   OSD / On-screen display (for the display of messages).
*   Playback rate (for slowdown due to time difference).

The client affects the following files: * Modifying .syncplay file in %APPDATA% (or $HOME on Linux version) folder to store configuration information.

Note: This behaviour can be disabled by using the `--no-store` command-line switch (see "Command-line switches", above)

## How to get involved.

Syncplay is developed using Python. You could help by reporting bugs, working on the code, or providing translations to other languages. The project is hosted at <https://github.com/Uriziel/syncplay/> and our IRC channel is #syncplay on irc.rizon.net.

## Authors

*   *Concept and principal Syncplay developer* - Uriziel.
*   *Other Syncplay coders* - daniel-123, Et0h.
*   *Translation* - Bosmanfrx (Polish).
*   *Original SyncPlay code* - Tomasz Kowalczyk (Fluxid), who developed SyncPlay at <https://github.com/fluxid/syncplay> - Fluxid's contributions to SyncPlay ended in February 2012, and it is understood that he passed away shortly after.