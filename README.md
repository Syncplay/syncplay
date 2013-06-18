#  Syncplay

Solution to synchronize video playback across multiple instances of mplayer2, mpv, Media Player Classic (MPC-HC) and VLC over the Internet.

## Official website
http://syncplay.pl

## Downloads
http://sourceforge.net/projects/syncplay/

## What does it do

Syncplay synchronises the position and play state of multiple media players so that the viewers can watch the same thing at the same time.
This means that when one person pauses/unpauses playback or seeks (jumps position) within their media player then this will be replicated across all media players connected to the same server and in the same 'room' (viewing session).
When a new person joins they will also be synchronised.

## What it doesn't do

Syncplay does not use video streaming or file sharing so each user must have their own copy of the media to be played. Syncplay does not synchronise player configuration, audio or subtitle track choice, playback rate, volume or filters. Furthermore, users must manually choose what file to play as Syncplay does not synchronise which file is open. Finally, Syncplay does not provide a voice or text-based chat platform to allow for discussion during playback as Syncplay is intended to be used in conjunction with third-party communication solutions such as IRC and Mumble.

## Authors
* *Concept and principal Syncplay developer* - Uriziel.
* *Other Syncplay coders* - daniel-123, Et0h.
* *Original SyncPlay code* - Tomasz Kowalczyk (Fluxid), who developed SyncPlay at https://github.com/fluxid/syncplay.
