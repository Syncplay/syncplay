#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author HarHar

import sys
import os
import socket
import threading
from syncplay import utils

class Bot(object):
	def __init__(self, server='irc.rizon.net', serverPassword='', port=6667, nick='SyncBot', nickservPass='', channel='', channelPassword='', functions=[]):
		#Arguments
		#	server 			- IRC Server to connect to
		#	serverPassword		- probably empty
		#	port			- usually between 6660 - 6669, 7000
		#	nick 			- duh
		#	nickservPass		- if not given, NickServ identification string won't be sent
		#	channel 		- channel to autojoin and interact with
		#	channelPassword		- if channel is +k
		#	functions		- list/tuple of functions that can be used from the bot:
		#		* pause(room, state=bool)
		#		* getRooms() -> list
		#		* getPosition(room) -> int
		#		* setPosition(room, seconds)
		#		* getUsers(room) -> list of {'nick': str, 'file': str, 'length': int}
		#		* isPaused(room) -> bool		

		self.functions = functions
		self.server = server
		self.serverPassword = serverPassword
		self.port = port
		self.nick = nick
		self.nickservPass = nickservPass
		self.channel = channel
		self.channelPassword = channelPassword

		#Connection/authentication routine
		self.sock = socket.socket()
		self.sock.connect((server, port))
		print self.sock.recv(4096)

		if serverPassword != '':
			self.sockSend('PASS ' + serverPassword)
		self.sockSend('NICK ' + nick)
		self.sockSend('USER ' + nick + ' ' + nick + ' ' + nick + ' :SyncPlay Bot') #Don't ask me

		print self.sock.recv(4096)

		if nickservPass != '':
			self.msg('NickServ', 'IDENTIFY ' + nickservPass)

		if channel != '':
			self.join(channel)

		self.active = True
		self.thread = threading.Thread(target=handlingThread, args=(self.sock, self))
		self.thread.setDaemon(True)
		self.thread.start()

	##Events that have to be binded##
	def sp_joined(self, who, room):
		self.msg(self.channel, chr(2) + '<' + who + '>'+ chr(15) +' has joined ' + room)
	def sp_left(self, who, room):
		self.msg(self.channel, chr(2) + '<' + who + '>'+ chr(15) +' has left ' + room)
	def sp_unpaused(self, who, room):
		self.msg(self.channel, chr(2) + '<' + who + '>'+ chr(15) +' has unpaused (room ' + room + ')')
	def sp_paused(self, who, room):
		self.msg(self.channel, chr(2) + '<' + who + '>'+ chr(15) +' has paused (room ' + room + ')')
	def sp_fileplaying(self, who, filename, room): #for when syncplay knows what filename is being played
		self.msg(self.channel, chr(2) + '<' + who + '>'+ chr(15) +' is playing "' + filename + '" (room ' + room + ')')
	##################################

	def sockSend(self, s):
		self.sock.send(s + '\r\n')
	def msg(self, who, message):
		self.sockSend('PRIVMSG ' + who + ' :' + message)
	def join(self, channel, passw=''):
		if passw != '': passw = ' ' + passw
		self.sockSend('JOIN ' + channel + passw)
	def part(self, channel, reason=''):
		self.sockSend('PART ' + channel + ' :' + reason)
	def quit(self, reason='Leaving'):
		self.active = False
		self.sockSend('QUIT :' + reason)
		self.sock.close()
	def nick(newnick):
		self.sockSend('NICK ' + newnick)
		self.nick = newnick
	def irc_onMsg(self, nickFrom, host, to, msg):
		if to[0] == '#': #channel
			split = msg.split(' ')

			if split[0].lower() == '!rooms':
				rooms = self.functions[1]()

				out = 'Currently the Syncplay server hosts viewing sessions as follows: '
				i = 0
				for room in rooms:
					if i == len(rooms)-1:
						out += chr(3) + '10' + room + chr(15) + '.'
					elif i == len(rooms)-2:
						out += chr(3) + '10' + room + chr(15) + ' and ultimately '
					else:
						out += chr(3) + '10' + room + chr(15) + ', '
					i += 1
				self.msg(to, out)
			elif split[0].lower() == '!roominfo':
				if len(split) >= 2:
					rooms = self.functions[1]()
					for room in split[1:]:
						if (room in rooms) == False:
							self.msg(to, chr(3) + '5Error!' + chr(15) + ' Room does not exists (' + room + ')')
						else:
							users = self.functions[4](room)
							paused = self.functions[5](room)
							out = chr(2) + '<Paused>' + chr(15) if paused else chr(2) + '<Playing>' + chr(15)
							out += ' [' + utils.formatTime(self.functions[2](room)) + '/' + utils.formatTime(users[0]['length']) + '] '
							out += users[0]['file']
							self.msg(to, out)
							out = 'Users: '
							i = 0
							for user in users:
								if i == len(users)-1:
									out += chr(3) + '2' + user['nick'] + chr(15) + '.'
								elif i == len(users)-2:
									out += chr(3) + '2' + user['nick'] + chr(15) + ' and '
								else:
									out += chr(3) + '2' + user['nick'] + chr(15) + ', '
								i += 1
							self.msg(to, out)
				else:
					self.msg(to, chr(2) + 'Usage:' + chr(15) + ' !roominfo [room]')
			elif split[0].lower() == '!pause':
				if len(split) >= 2:
					rooms = self.functions[1]()
					for room in split[1:]:
						if (room in rooms) == False:
							self.msg(to, chr(3) + '5Error!' + chr(15) + ' Room does not exists (' + room + ')')
						else:
							users = self.functions[4](room)
							for u in users:
								if u['nick'] == nickFrom:
									break
							else:
								self.msg(to, chr(3) + '5Error!' + chr(15) + ' Your nick is not in the specified room')
								continue

							self.functions[6](room, True)
				else:
					self.msg(to, chr(2) + 'Usage:' + chr(15) + ' !pause [room]')							
			elif split[0].lower() == '!play':
				if len(split) >= 2:
					rooms = self.functions[1]()
					for room in split[1:]:
						if (room in rooms) == False:
							self.msg(to, chr(3) + '5Error!' + chr(15) + ' Room does not exists (' + room + ')')
						else:
							users = self.functions[4](room)
							for u in users:
								if u['nick'] == nickFrom:
									break
							else:
								self.msg(to, chr(3) + '5Error!' + chr(15) + ' Your nick is not in the specified room')
								continue

							self.functions[6](room, False)							
				else:
					self.msg(to, chr(2) + 'Usage:' + chr(15) + ' !play [room]')
			elif split[0].lower() == '!help':
				self.msg(to, chr(2) + 'Available commands:' + chr(15) + ' !rooms / !roominfo [room] / !pause / !play')

def handlingThread(sock, bot):
	while bot.active:
		rcvd = sock.recv(4096).split('\n')
		for line in rcvd:
			print line
			line = line.replace('\r', '')

			if line.split(' ')[0] == 'PING':
				try:
					sock.send('\r\nPONG ' + line.split(' ')[1].replace(':', '') + '\r\n')
				except: #if we were fooled by the server :C
					sock.send('\r\nPONG\r\n')
				#\r\n on the beggining too because if we send two things too fast, the IRC server can discern

			lsplit = line.split(':')
			if len(lsplit) >= 2:
				if 'PRIVMSG' in lsplit[1] or 'NOTICE' in lsplit[1]:
					# ---BEGIN WTF BLOCK---
					lsplit = line.split(':')
					addrnfrom = ''
					if '~' in lsplit[1]:
						addrnfrom = lsplit[1].split('~')[1].split(' ')[0]
						nfrom = lsplit[1].split('!')[0]
					else:
						nfrom = lsplit[1].split('!')[0]

					if len(lsplit[1].split()) >= 3:
						to = lsplit[1].split()[2]
					msg = ''
					for brks in lsplit[2:]:
						msg += brks + ':'
					msg = msg[:-1].lstrip()
					# ---END WTF BLOCK- --
					bot.irc_onMsg(nfrom, addrnfrom, to, msg)
