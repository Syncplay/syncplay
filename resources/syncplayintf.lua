-- syncplayintf.lua -- An interface for communication between mpv and Syncplay
-- Author: Etoh
-- Thanks: RiCON, James Ross-Gowan, Argon-, wm4, uau

local CANVAS_WIDTH = 1920
local CANVAS_HEIGHT = 1080
local ROW_HEIGHT = 100
local chat_format = "{\\fs50}{\an1}"
local max_scrolling_rows = 100
local MOVEMENT_PER_SECOND = 200
local TICK_INTERVAL = 0.01
local CHAT_MODE_CHATROOM = "Chatroom"
local CHAT_MODE_SUBTITLE = "Subtitle"
local CHAT_MODE_SCROLLING = "Scrolling"
local last_chat_time = 0
local use_alpha_rows_for_chat = true
local MOOD_NEUTRAL = 0
local MOOD_BAD = 1
local MOOD_GOOD = 2
local WORDWRAPIFY_MAGICWORD = "{\\\\fscx0}  {\\\\fscx100}"
local SCROLLING_ADDITIONAL_BOTTOM_MARGIN = 75
local default_oscvisibility_state = "never"

local ALPHA_WARNING_TEXT_COLOUR = "FF00FF" -- RBG
local HINT_TEXT_COLOUR = "AAAAAA" -- RBG
local NEUTRAL_ALERT_TEXT_COLOUR = "FFFFFF" -- RBG
local BAD_ALERT_TEXT_COLOUR = "0000FF"  -- RBG
local GOOD_ALERT_TEXT_COLOUR = "00FF00" -- RBG
local NOTIFICATION_TEXT_COLOUR = "FFFF00" -- RBG

local chat_log = {}

local assdraw = require "mp.assdraw"

local opt = require 'mp.options'

function format_scrolling(xpos, ypos, text)
	local chat_message = "\n"..chat_format .. "{\\pos("..xpos..","..ypos..")}"..text.."\\N\\n"
    return string.format(chat_message)
end

function format_chatroom(text)
    local chat_message = chat_format .. text .."\\N\\n"
    return string.format(chat_message)
end

function clear_chat()
	chat_log = {}
end

local alert_osd = ""
local last_alert_osd_time = nil
local alert_osd_mood = MOOD_NEUTRAL

local notification_osd = ""
local last_notification_osd_time = nil
local notification_osd_mood = MOOD_NEUTRAL

function set_alert_osd(osd_message, mood)
    alert_osd = osd_message
    last_alert_osd_time = mp.get_time()
    alert_osd_mood = mood
end

function set_notification_osd(osd_message, mood)
    notification_osd = osd_message
    last_notification_osd_time = mp.get_time()
    notification_osd_mood = mood
end

function add_chat(chat_message, mood)
    last_chat_time = mp.get_time()
	local entry = #chat_log+1
	for i = 1, #chat_log do
		if chat_log[i].text == '' then
			entry = i
			break
		end
    end
	local row = ((entry-1) % max_scrolling_rows)+1
    if opts['chatOutputMode'] == CHAT_MODE_CHATROOM then
		if entry > opts['chatMaxLines'] then
             table.remove(chat_log, 1)
             entry = entry - 1
        end
    end
	chat_log[entry] = { xpos=CANVAS_WIDTH, timecreated=mp.get_time(), text=tostring(chat_message), row=row }
end

function chat_update()
    ass = assdraw.ass_new()
	local chat_ass = ''
    local rowsAdded = 0
    local to_add = ''
    local incrementRow = 0
    if opts['chatOutputMode'] == CHAT_MODE_CHATROOM and chat_log ~= {} then
        local timedelta = mp.get_time() - last_chat_time
		if timedelta >= opts['chatTimeout'] then
            clear_chat()
        end
    end
    rowsAdded,to_add = process_alert_osd()
    if to_add ~= nil and to_add ~= "" then
        chat_ass = to_add
    end
    incrementRow,to_add = process_notification_osd(rowsAdded)
    rowsAdded = rowsAdded + incrementRow
    if to_add ~= nil and to_add ~= "" then
        chat_ass = chat_ass .. to_add
    end

	if #chat_log > 0 then
		for i = 1, #chat_log do
			local to_add = process_chat_item(i,rowsAdded)
			if to_add ~= nil and to_add ~= "" then
				chat_ass = chat_ass .. to_add
			end
		end
    end

    local xpos = opts['chatLeftMargin']
    local ypos = opts['chatTopMargin']
    chat_ass = "\n".."{\\pos("..xpos..","..ypos..")}".. chat_ass

    if use_alpha_rows_for_chat == false and opts['chatDirectInput'] == true then
        local alphawarning_ass = assdraw.ass_new()
        alphawarning_ass = "{\\a6}{\\1c&H"..ALPHA_WARNING_TEXT_COLOUR.."}"..opts['alphakey-mode-warning-first-line'].."\n{\\a6}{\\1c&H"..ALPHA_WARNING_TEXT_COLOUR.."}"..opts['alphakey-mode-warning-second-line']
        ass:append(alphawarning_ass)
    elseif opts['chatOutputMode'] == CHAT_MODE_CHATROOM and opts['chatInputPosition'] == "Top" then
        ass:append(chat_ass)
        ass:append(input_ass())
    else
        ass:append(input_ass())
        ass:append(chat_ass)
    end
	mp.set_osd_ass(CANVAS_WIDTH,CANVAS_HEIGHT, ass.text)
end

function process_alert_osd()
    local rowsCreated = 0
    local stringToAdd = ""
    if alert_osd ~= "" and mp.get_time() - last_alert_osd_time < opts['alertTimeout'] and last_alert_osd_time ~= nil then
        local messageColour
        if alert_osd_mood == MOOD_NEUTRAL then
            messageColour = "{\\1c&H"..NEUTRAL_ALERT_TEXT_COLOUR.."}"
        elseif alert_osd_mood == MOOD_BAD then
            messageColour = "{\\1c&H"..BAD_ALERT_TEXT_COLOUR.."}"
        elseif alert_osd_mood == MOOD_GOOD then
            messageColour = "{\\1c&H"..GOOD_ALERT_TEXT_COLOUR.."}"
        end
        local messageString = wordwrapify_string(alert_osd)
        local startRow = 0
        if messageString ~= '' and messageString ~= nil then
            local toDisplay
            rowsCreated = rowsCreated + 1
            messageString = messageColour..messageString
			if stringToAdd ~= "" then
            	stringToAdd = stringToAdd .. format_chatroom(messageString)
			else
				stringToAdd = format_chatroom(messageString)
			end
        end
    end
    return rowsCreated, stringToAdd
end

function process_notification_osd(startRow)
    local rowsCreated = 0
    local startRow = startRow
    local stringToAdd = ""
    if notification_osd ~= "" and mp.get_time() - last_notification_osd_time < opts['alertTimeout'] and last_notification_osd_time ~= nil then
        local messageColour
        messageColour = "{\\1c&H"..NOTIFICATION_TEXT_COLOUR.."}"
        local messageString
        messageString = wordwrapify_string(notification_osd)
        messageString = messageColour..messageString
        messageString = format_chatroom(messageString)
        stringToAdd = messageString
        rowsCreated = 1
	end
    return rowsCreated, stringToAdd
end


function process_chat_item(i, rowsAdded)
    if opts['chatOutputMode'] == CHAT_MODE_CHATROOM then
		return process_chat_item_chatroom(i, rowsAdded)
	elseif opts['chatOutputMode'] == CHAT_MODE_SCROLLING then
		return process_chat_item_scrolling(i)
	end
end

function process_chat_item_scrolling(i)
	local timecreated = chat_log[i].timecreated
	local timedelta = mp.get_time() - timecreated
	local xpos = CANVAS_WIDTH - (timedelta*MOVEMENT_PER_SECOND)
	local text = chat_log[i].text
	if text ~= '' then
		local roughlen = string.len(text) * opts['chatOutputFontSize'] * 1.5
		if xpos > (-1*roughlen) then
			local row = chat_log[i].row-1+opts['scrollingFirstRowOffset']
			local ypos = opts['chatTopMargin']+(row * opts['chatOutputFontSize'])
			return format_scrolling(xpos,ypos,text)
		else
			chat_log[i].text = ''
		end
	end
end

function process_chat_item_chatroom(i, startRow)
    local text = chat_log[i].text
	if text ~= '' then
        local text = wordwrapify_string(text)
        local rowNumber = i+startRow-1
        return(format_chatroom(text))
	end
end

function process_chat_item_subtitle(i)
    local timecreated = chat_log[i].timecreated
	local timedelta = mp.get_time() - timecreated
	local xpos = CANVAS_WIDTH - (timedelta*MOVEMENT_PER_SECOND)
	local text = chat_log[i].text
	if text ~= '' then
		local roughlen = string.len(text) * opts['chatOutputFontSize']
		if xpos > (-1*roughlen) then
			local row = chat_log[i].row
			local ypos = row * opts['chatOutputFontSize']
            return(format_scrolling(xpos,ypos,text))
		else
			chat_log[i].text = ''
		end
	end
end

chat_timer=mp.add_periodic_timer(TICK_INTERVAL, chat_update)

mp.register_script_message('chat', function(e)
	add_chat(e)
end)

-- Chat OSD

mp.register_script_message('chat-osd-neutral', function(e)
	add_chat(e,MOOD_NEUTRAL)
end)

mp.register_script_message('chat-osd-bad', function(e)
	add_chat(e,MOOD_BAD)
end)

mp.register_script_message('chat-osd-good', function(e)
	add_chat(e,MOOD_GOOD)
end)

-- Alert OSD

mp.register_script_message('alert-osd-neutral', function(e)
	set_alert_osd(e,MOOD_NEUTRAL)
end)

mp.register_script_message('alert-osd-bad', function(e)
	set_alert_osd(e,MOOD_BAD)
end)

mp.register_script_message('alert-osd-good', function(e)
	set_alert_osd(e,MOOD_GOOD)
end)

-- Notification OSD

mp.register_script_message('notification-osd-neutral', function(e)
	set_notification_osd(e,MOOD_NEUTRAL)
end)

mp.register_script_message('notification-osd-bad', function(e)
	set_notification_osd(e,MOOD_BAD)
end)

mp.register_script_message('notification-osd-good', function(e)
	set_notification_osd(e,MOOD_GOOD)
end)

--

mp.register_script_message('set_syncplayintf_options', function(e)
	set_syncplayintf_options(e)
end)

-- adapted from repl.lua -- A graphical REPL for mpv input commands
--
-- c 2016, James Ross-Gowan
--
-- Permission to use, copy, modify, and/or distribute this software for any
-- purpose with or without fee is hereby granted, provided that the above
-- copyright notice and this permission notice appear in all copies.
--
-- THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
-- WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
-- MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
-- SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
-- WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
-- OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
-- CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-- Default options
local utils = require 'mp.utils'
local options = require 'mp.options'
opts = {

	-- All drawing is scaled by this value, including the text borders and the
	-- cursor. Change it if you have a high-DPI display.
	scale = 1,
	-- Set the font used for the REPL and the console. This probably doesn't
	-- have to be a monospaced font.
	['chatInputFontFamily'] = 'monospace',
	-- Enable/Disable
	['chatInputEnabled'] = true,
	['chatOutputEnabled'] = true,
    ['OscVisibilityChangeCompatible'] = false,
	-- Set the font size used for the REPL and the console. This will be
	-- multiplied by "scale."
	['chatInputFontSize'] = 20,
	['chatInputFontWeight'] = 1,
	['chatInputFontUnderline'] = false,
	['chatInputFontColor'] = "#000000",
	['chatInputPosition'] = "Top",
	['MaxChatMessageLength'] = 50,
	['chatOutputFontFamily'] = "sans serif",
	['chatOutputFontSize'] = 50,
	['chatOutputFontWeight'] = 1,
	['chatOutputFontUnderline'] = false,
	['chatOutputFontColor'] = "#FFFFFF",
	['chatOutputMode'] = "Chatroom",
    ['scrollingFirstRowOffset'] = 2,
	-- Can be "Chatroom", "Subtitle" or "Scrolling" style
    ['chatMaxLines'] = 7,
    ['chatTopMargin'] = 25,
    ['chatLeftMargin'] = 20,
    ['chatDirectInput'] = true,
    --
    ['notificationTimeout'] = 3,
    ['alertTimeout'] = 5,
    ['chatTimeout'] = 7,
	--
	['inputPromptStartCharacter'] = ">",
    ['inputPromptEndCharacter'] = "<",
    ['backslashSubstituteCharacter'] = "|",
    --Lang:
    ['mpv-key-tab-hint'] = "[TAB] to toggle access to alphabet row key shortcuts.",
    ['mpv-key-hint'] = "[ENTER] to send message. [ESC] to escape chat mode.",
    ['alphakey-mode-warning-first-line'] = "You can temporarily use old mpv bindings with a-z keys.",
    ['alphakey-mode-warning-second-line'] = "Press [TAB] to return to Syncplay chat mode.",
}

function detect_platform()
	local o = {}
	-- Kind of a dumb way of detecting the platform but whatever
	if mp.get_property_native('options/vo-mmcss-profile', o) ~= o then
		return 'windows'
	elseif mp.get_property_native('options/input-app-events', o) ~= o then
		return 'macos'
	end
	return 'linux'
end

-- Pick a better default font for Windows and macOS
local platform = detect_platform()
if platform == 'windows' then
	opts.font = 'Consolas'
elseif platform == 'macos' then
	opts.font = 'Menlo'
end

-- Apply user-set options
options.read_options(opts)

-- Escape a string for verbatim display on the OSD
function ass_escape(str)
	-- There is no escape for '\' in ASS (I think?) but '\' is used verbatim if
	-- it isn't followed by a recognised character, so add a zero-width
	-- non-breaking space
	str = str:gsub('\\', '\\\239\187\191')
	str = str:gsub('{', '\\{')
	str = str:gsub('}', '\\}')
	-- Precede newlines with a ZWNBSP to prevent ASS's weird collapsing of
	-- consecutive newlines
	str = str:gsub('\n', '\239\187\191\n')
	return str
end

function update()
	return
end

local repl_active = false
local insert_mode = false
local line = ''
local cursor = 1
local key_hints_enabled = false

function input_ass()
	if not repl_active then
		return ""
	end
	local bold
	if opts['chatInputFontWeight'] < 75 then
		bold = 0
	else
		bold = 1
	end
	local underline = opts['chatInputFontUnderline'] and 1 or 0
	local red = string.sub(opts['chatInputFontColor'],2,3)
	local green = string.sub(opts['chatInputFontColor'],4,5)
	local blue = string.sub(opts['chatInputFontColor'],6,7)
	local fontColor = blue .. green .. red
	local style = '{\\r' ..
	               '\\1a&H00&\\3a&H00&\\4a&H99&' ..
	               '\\1c&H'..fontColor..'&\\3c&H111111&\\4c&H000000&' ..
	               '\\fn' .. opts['chatInputFontFamily'] .. '\\fs' .. opts['chatInputFontSize'] .. '\\b' .. bold ..
	               '\\bord2\\xshad0\\yshad1\\fsp0\\q1}'

	local after_style = '{\\u'  .. underline .. '}'
	local cheight = opts['chatInputFontSize'] * 8
	local cglyph = '_'
	local before_cur = ass_escape(line:sub(1, cursor - 1))
	local after_cur = ass_escape(line:sub(cursor))
    local secondary_pos = "10,"..tostring(10+opts['chatInputFontSize'])

	local alignment = 7
	local position = "5,5"
	local start_marker = opts['inputPromptStartCharacter']
	local end_marker = ""
	if opts['chatInputPosition'] == "Middle" then
		alignment = 5
		position = tostring(CANVAS_WIDTH/2)..","..tostring(CANVAS_HEIGHT/2)
        secondary_pos = tostring(CANVAS_WIDTH/2)..","..tostring((CANVAS_HEIGHT/2)+20+opts['chatInputFontSize'])
		end_marker = "{\\u0}"..opts['inputPromptEndCharacter']
	elseif opts['chatInputPosition'] == "Bottom" then
		alignment = 1
		position = tostring(5)..","..tostring(CANVAS_HEIGHT-5)
        secondary_pos = "10,"..tostring(CANVAS_HEIGHT-(20+opts['chatInputFontSize']))
    end

	local osd_help_message = opts['mpv-key-hint']
    if opts['chatDirectInput'] then
        osd_help_message = opts['mpv-key-tab-hint'] .. " " .. osd_help_message
    end
	local help_prompt = '\\N\\n{\\an'..alignment..'\\pos('..secondary_pos..')\\fn' .. opts['chatOutputFontFamily'] .. '\\fs' .. (opts['chatInputFontSize']/1.25) .. '\\1c&H'..HINT_TEXT_COLOUR..'}' .. osd_help_message

	local firststyle = "{\\an"..alignment.."}{\\pos("..position..")}"
	if opts['chatOutputEnabled'] and opts['chatOutputMode'] == CHAT_MODE_CHATROOM and opts['chatInputPosition'] == "Top" then
		firststyle = get_output_style().."{'\\1c&H'"..fontColor.."}"
        before_cur = before_cur .. firststyle
        after_cur =  after_cur .. firststyle
		help_prompt = '\\N\\n'..firststyle..'{\\1c&H'..HINT_TEXT_COLOUR..'}' .. osd_help_message .. '\\N\\n'
	end
	if key_hints_enabled == false then help_prompt = "" end

	return firststyle..style..start_marker.." "..after_style..before_cur..style..cglyph..style..after_style..after_cur..end_marker..help_prompt

end

function get_output_style()
	local bold
	if opts['chatOutputFontWeight'] < 75 then
		bold = 0
	else
		bold = 1
	end
	local underline = opts['chatOutputFontUnderline'] and 1 or 0
	local red = string.sub(opts['chatOutputFontColor'],2,3)
	local green = string.sub(opts['chatOutputFontColor'],4,5)
	local blue = string.sub(opts['chatOutputFontColor'],6,7)
	local fontColor = blue .. green .. red
	local style = '{\\r' ..
	               '\\1a&H00&\\3a&H00&\\4a&H99&' ..
	               '\\1c&H'..fontColor..'&\\3c&H111111&\\4c&H000000&' ..
	               '\\fn' .. opts['chatOutputFontFamily'] .. '\\fs' .. opts['chatOutputFontSize'] .. '\\b' .. bold ..
	               '\\u'  .. underline .. '\\a5\\MarginV=500' .. '}'

	--mp.osd_message("",0)
	return style

end

function escape()
	set_active(false)
	clear()
end

-- Set the REPL visibility (`, Esc)
function set_active(active)
    if use_alpha_rows_for_chat == false then active = false end
	if active == repl_active then return end
	if active then
		repl_active = true
		insert_mode = false
		mp.enable_key_bindings('repl-input', 'allow-hide-cursor+allow-vo-dragging')
	else
		repl_active = false
		mp.disable_key_bindings('repl-input')
    end
    if default_oscvisibility_state ~= "never" and opts['OscVisibilityChangeCompatible'] == true then
        if active then
            mp.commandv("script-message", "osc-visibility","never", "no-osd")
        else
            mp.commandv("script-message", "osc-visibility",default_oscvisibility_state, "no-osd")
        end
    end
end

-- Show the repl if hidden and replace its contents with 'text'
-- (script-message-to repl type)
function show_and_type(text)
	text = text or ''

	line = text
	cursor = line:len() + 1
	insert_mode = false
	if repl_active then
		update()
	else
		set_active(true)
	end
end

-- Naive helper function to find the next UTF-8 character in 'str' after 'pos'
-- by skipping continuation bytes. Assumes 'str' contains valid UTF-8.
function next_utf8(str, pos)
	if pos > str:len() then return pos end
	repeat
		pos = pos + 1
	until pos > str:len() or str:byte(pos) < 0x80 or str:byte(pos) > 0xbf
	return pos
end

-- Naive helper function to find the next UTF-8 character in 'str' after 'pos'
-- by skipping continuation bytes. Assumes 'str' contains valid UTF-8.


-- As above, but finds the previous UTF-8 charcter in 'str' before 'pos'
function prev_utf8(str, pos)
	if pos <= 1 then return pos end
	repeat
		pos = pos - 1
	until pos <= 1 or str:byte(pos) < 0x80 or str:byte(pos) > 0xbf
	return pos
end

function trim_string(line,maxCharacters)
-- Naive helper function to find the next UTF-8 character in 'str' after 'pos'
-- by skipping continuation bytes. Assumes 'str' contains valid UTF-8.

	local str = line
	if str == nil or str == "" or str:len() <= maxCharacters then
		return str, ""
	end
	local pos = 0
	local oldPos = -1
	local chars = 0

	repeat
		oldPos = pos
		pos = next_utf8(str, pos)
		chars = chars + 1
	until pos == oldPos or chars > maxCharacters
	return str:sub(1,pos-1), str:sub(pos)
end

function wordwrapify_string(line)
-- Naive helper function to find the next UTF-8 character in 'str' after 'pos'
-- by skipping continuation bytes. Assumes 'str' contains valid UTF-8.
	local str = line
	if str == nil or str == "" then
		return str, ""
    end
    local newstr = ""
	local currentChar = 0
	local nextChar = 0
	local chars = 0
    local maxChars = str:len()

	repeat
		nextChar = next_utf8(str, currentChar)
        if nextChar == currentChar then
            return newstr
		end
		charToTest = str:sub(currentChar,nextChar-1)
		if charToTest ~= "\\" and charToTest ~= "{"  and charToTest ~= "}" then
			newstr = newstr .. WORDWRAPIFY_MAGICWORD .. str:sub(currentChar,nextChar-1)
        else
			newstr = newstr .. str:sub(currentChar,nextChar-1)
		end
        currentChar = nextChar
	until currentChar > maxChars
    newstr = string.gsub(newstr,opts['backslashSubstituteCharacter'], '\\\239\187\191') -- Workaround for \ escape issues
	return newstr
end


function trim_input()
-- Naive helper function to find the next UTF-8 character in 'str' after 'pos'
-- by skipping continuation bytes. Assumes 'str' contains valid UTF-8.

	local str = line
	if str == nil or str == "" or str:len() <= opts['MaxChatMessageLength'] then
		return
	end
	local pos = 0
	local oldPos = -1
	local chars = 0

	repeat
		oldPos = pos
		pos = next_utf8(str, pos)
		chars = chars + 1
	until pos == oldPos or chars > opts['MaxChatMessageLength']
	line = line:sub(1,pos-1)
	if cursor > pos then
		cursor = pos
	end
	return
end

-- Insert a character at the current cursor position (' '-'~', Shift+Enter)
function handle_char_input(c)
	if key_hints_enabled and (string.len(line) > 0 or opts['chatDirectInput'] == false) then
        key_hints_enabled = false
    end
    set_active(true)
	if insert_mode then
		line = line:sub(1, cursor - 1) .. c .. line:sub(next_utf8(line, cursor))
	else
		line = line:sub(1, cursor - 1) .. c .. line:sub(cursor)
	end
	cursor = cursor + 1
    trim_input()
	update()
end

-- Remove the character behind the cursor (Backspace)
function handle_backspace()
	if cursor <= 1 then return end
	local prev = prev_utf8(line, cursor)
	line = line:sub(1, prev - 1) .. line:sub(cursor)
	cursor = prev
	update()
end

-- Remove the character in front of the cursor (Del)
function handle_del()
	if cursor > line:len() then return end
	line = line:sub(1, cursor - 1) .. line:sub(next_utf8(line, cursor))
	update()
end

-- Toggle insert mode (Ins)
function handle_ins()
	insert_mode = not insert_mode
end

--local was_active_before_tab = false

function handle_tab()
    use_alpha_rows_for_chat = not use_alpha_rows_for_chat
    if use_alpha_rows_for_chat then
        mp.enable_key_bindings('repl-alpha-input')
        --set_active(was_active_before_tab)
    else
        mp.disable_key_bindings('repl-alpha-input')
        --was_active_before_tab = repl_active
        --set_active(false)
        escape()
    end
end

-- Move the cursor to the next character (Right)
function next_char(amount)
	cursor = next_utf8(line, cursor)
	update()
end

-- Move the cursor to the previous character (Left)
function prev_char(amount)
	cursor = prev_utf8(line, cursor)
	update()
end

-- Clear the current line (Ctrl+C)
function clear()
	line = ''
	cursor = 1
	insert_mode = false
	update()
end

-- Close the REPL if the current line is empty, otherwise do nothing (Ctrl+D)
function maybe_exit()
	if line == '' then
		set_active(false)
	end
end

-- Run the current command and clear the line (Enter)
function handle_enter()
	if not repl_active then
		set_active(true)
		return
	end
	set_active(false)

	if line == '' then
		return
    end
    key_hints_enabled = false
	line = string.gsub(line,"\\", "\\\\")
	line = string.gsub(line,"\"", "\\\"")
	mp.command('print-text "<chat>'..line..'</chat>"')
	clear()
end

-- Move the cursor to the beginning of the line (HOME)
function go_home()
	cursor = 1
	update()
end

-- Move the cursor to the end of the line (END)
function go_end()
	cursor = line:len() + 1
	update()
end

-- Delete from the cursor to the end of the line (Ctrl+K)
function del_to_eol()
	line = line:sub(1, cursor - 1)
	update()
end

-- Delete from the cursor back to the start of the line (Ctrl+U)
function del_to_start()
	line = line:sub(cursor)
	cursor = 1
	update()
end

-- Returns a string of UTF-8 text from the clipboard (or the primary selection)
function get_clipboard(clip)
	if platform == 'linux' then
		local res = utils.subprocess({ args = {
			'xclip', '-selection', clip and 'clipboard' or 'primary', '-out'
		} })
		if not res.error then
			return res.stdout
		end
	elseif platform == 'windows' then
		local res = utils.subprocess({ args = {
			'powershell', '-NoProfile', '-Command', [[& {
				Trap {
					Write-Error -ErrorRecord $_
					Exit 1
				}

				$clip = ""
				if (Get-Command "Get-Clipboard" -errorAction SilentlyContinue) {
					$clip = Get-Clipboard -Raw -Format Text -TextFormatType UnicodeText
				} else {
					Add-Type -AssemblyName PresentationCore
					$clip = [Windows.Clipboard]::GetText()
				}

				$clip = $clip -Replace "`r",""
				$u8clip = [System.Text.Encoding]::UTF8.GetBytes($clip)
				[Console]::OpenStandardOutput().Write($u8clip, 0, $u8clip.Length)
			}]]
		} })
		if not res.error then
			return res.stdout
		end
	elseif platform == 'macos' then
		local res = utils.subprocess({ args = { 'pbpaste' } })
		if not res.error then
			return res.stdout
		end
	end
	return ''
end

-- Paste text from the window-system's clipboard. 'clip' determines whether the
-- clipboard or the primary selection buffer is used (on X11 only.)
function paste(clip)
	local text = get_clipboard(clip)
	local before_cur = line:sub(1, cursor - 1)
	local after_cur = line:sub(cursor)
	line = before_cur .. text .. after_cur
	cursor = cursor + text:len()
    trim_input()
	update()
end

-- The REPL has pretty specific requirements for key bindings that aren't
-- really satisified by any of mpv's helper methods, since they must be in
-- their own input section, but they must also raise events on key-repeat.
-- Hence, this function manually creates an input section and puts a list of
-- bindings in it.
function add_repl_bindings(bindings)
	local cfg = ''
	for i, binding in ipairs(bindings) do
		local key = binding[1]
		local fn = binding[2]
		local name = '__repl_binding_' .. i
		mp.add_forced_key_binding(nil, name, fn, 'repeatable')
		cfg = cfg .. key .. ' script-binding ' .. mp.script_name .. '/' ..
		      name .. '\n'
	end
	mp.commandv('define-section', 'repl-input', cfg, 'force')
end

function add_repl_alpharow_bindings(bindings)
	local cfg = ''
	for i, binding in ipairs(bindings) do
		local key = binding[1]
		local fn = binding[2]
		local name = '__repl_alpha_binding_' .. i
		mp.add_forced_key_binding(nil, name, fn, 'repeatable')
		cfg = cfg .. key .. ' script-binding ' .. mp.script_name .. '/' ..
		      name .. '\n'
	end
	mp.commandv('define-section', 'repl-alpha-input', cfg, 'force')
    mp.enable_key_bindings('repl-alpha-input')
end

-- Mapping from characters to mpv key names
local binding_name_map = {
	[' '] = 'SPACE',
	['#'] = 'SHARP',
}

-- List of input bindings. This is a weird mashup between common GUI text-input
-- bindings and readline bindings.
local bindings = {
	{ 'esc',         function() escape() end       },
	{ 'bs',          handle_backspace                       },
	{ 'shift+bs',    handle_backspace                       },
	{ 'del',         handle_del                             },
	{ 'shift+del',   handle_del                             },
	{ 'ins',         handle_ins                             },
	{ 'left',        function() prev_char() end             },
	{ 'right',       function() next_char() end             },
	{ 'up',          function() clear() end        },
	{ 'home',        go_home                                },
	{ 'end',         go_end                                 },
	{ 'ctrl+c',      clear                                  },
	{ 'ctrl+d',      maybe_exit                             },
	{ 'ctrl+k',      del_to_eol                             },
	{ 'ctrl+l',      clear_log_buffer                       },
	{ 'ctrl+u',      del_to_start                           },
	{ 'ctrl+v',      function() paste(true) end             },
	{ 'meta+v',      function() paste(true) end             },
}
local alpharowbindings = {}
-- Add bindings for all the printable US-ASCII characters from ' ' to '~'
-- inclusive. Note, this is a pretty hacky way to do text input. mpv's input
-- system was designed for single-key key bindings rather than text input, so
-- things like dead-keys and non-ASCII input won't work. This is probably okay
-- though, since all mpv's commands and properties can be represented in ASCII.
for b = (' '):byte(), ('~'):byte() do
	local c = string.char(b)
	local binding = binding_name_map[c] or c
	bindings[#bindings + 1] = {binding, function() handle_char_input(c) end}
end

function add_alpharowbinding(firstchar,lastchar)
    for b = (firstchar):byte(), (lastchar):byte() do
	    local c = string.char(b)
	    local alphabinding = binding_name_map[c] or c
	    alpharowbindings[#alpharowbindings + 1] = {alphabinding, function() handle_char_input(c) end}
    end
end

add_alpharowbinding('a','z')
add_alpharowbinding('A','Z')
add_alpharowbinding('/','/')
add_alpharowbinding(':',':')
add_alpharowbinding('(',')')
add_alpharowbinding('{','}')
add_alpharowbinding(':',';')
add_alpharowbinding('<','>')
add_alpharowbinding(',','.')
add_alpharowbinding('|','|')
add_alpharowbinding('\\','\\')
add_alpharowbinding('?','?')
add_alpharowbinding('[',']')
add_alpharowbinding('#','#')
add_alpharowbinding('~','~')
add_alpharowbinding('\'','\'')
add_alpharowbinding('@','@')

add_repl_bindings(bindings)

-- Add a script-message to show the REPL and fill it with the provided text
mp.register_script_message('type', function(text)
	show_and_type(text)
end)

mp.command('print-text "<get_syncplayintf_options>"')

function set_syncplayintf_options(input)
	--mp.command('print-text "<chat>...'..input..'</chat>"')
	for option, value in string.gmatch(input, "([^ ,=]+)=([^,]+)") do
		local valueType = type(opts[option])
		if valueType == "number" then
			value = tonumber(value)
		elseif valueType == "boolean" then
			if value == "True" then
				value = true
			else
				value = false
			end
		end
		opts[option] = value
		--mp.command('print-text "<chat>'..option.."="..tostring(value).." - "..valueType..'</chat>"')
    end
    chat_format = get_output_style()
    local vertical_output_area = CANVAS_HEIGHT-(opts['chatTopMargin']+opts['chatBottomMargin']+(opts['chatOutputFontSize']*opts['scrollingFirstRowOffset'])+SCROLLING_ADDITIONAL_BOTTOM_MARGIN)
    max_scrolling_rows = math.floor(vertical_output_area/opts['chatOutputFontSize'])
    local user_opts = { visibility = "auto", }
    opt.read_options(user_opts, "osc")
    default_oscvisibility_state = user_opts.visibility
	if opts['chatInputEnabled'] == true then
        key_hints_enabled = true
		mp.add_forced_key_binding('enter', handle_enter)
		mp.add_forced_key_binding('kp_enter', handle_enter)
        if opts['chatDirectInput'] == true then
        	add_repl_alpharow_bindings(alpharowbindings)
        	mp.add_forced_key_binding('tab', handle_tab)
		end
    end
end