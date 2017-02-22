-- syncplayintf.lua -- An interface for communication between mpv and Syncplay
-- Author: Etoh
-- Thanks: RiCON, James Ross-Gowan, Argon-, wm4

local CANVAS_WIDTH = 1000
local CANVAS_HEIGHT = 1000
local ROW_HEIGHT = 100
local PIXELS_PER_CHAR = 16
local CHAT_FORMAT = "{\\fs60}{\an1}{\\q2}"
local MAX_ROWS = 7
local MOVEMENT_PER_TICK = 6
local TICK_FREQUENCY = 0.03

local chat_log = {}

local assdraw = require "mp.assdraw"

function format_chat(xpos, ypos, text)
	chat_message = CHAT_FORMAT .. "{\\pos("..xpos..","..ypos..")}"..text.."\n"
    return string.format(chat_message)
end

function clear_chat()
	chat_log = {}
end

function add_chat(chat_message)
	local entry = #chat_log+1
	for i = 1, #chat_log do
		if chat_log[i].text == '' then
			entry = i
			break
		end
	end
	local row = ((entry-1) % MAX_ROWS)+1
	chat_log[entry] = { xpos=CANVAS_WIDTH, text=tostring(chat_message), row=row }
end

function chat_update()
    ass = assdraw.ass_new()
	local screenx, screeny, aspect = mp.get_osd_size()
	local chat_messages = #chat_log
	local chat_ass = ''
	if #chat_log > 0 then
		for i = 1, #chat_log do
			local xpos = chat_log[i].xpos
			local text = chat_log[i].text
			if text ~= '' then
				local roughlen = string.len(text) * PIXELS_PER_CHAR
				if xpos > (-1*roughlen) then
					local row = chat_log[i].row
					local ypos = row * ROW_HEIGHT
					chat_ass = chat_ass .. format_chat(xpos,ypos,text)
					chat_log[i].xpos = xpos-MOVEMENT_PER_TICK
				else
					chat_log[i].text = ''
				end
			end
		end
	end
	ass:append(chat_ass)
	mp.set_osd_ass(CANVAS_WIDTH,CANVAS_HEIGHT, ass.text)
end
chat_timer=mp.add_periodic_timer(TICK_FREQUENCY, chat_update)
--mp.register_event("tick", chat_update)

mp.register_script_message('chat', function(e)
	add_chat(e)
end)