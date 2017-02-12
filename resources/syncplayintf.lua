-- repl.lua -- A graphical REPL for mpv input commands
--
-- © 2016, James Ross-Gowan
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

local utils = require 'mp.utils'
local options = require 'mp.options'
local assdraw = require 'mp.assdraw'

-- Default options
local opts = {
	-- All drawing is scaled by this value, including the text borders and the
	-- cursor. Change it if you have a high-DPI display.
	scale = 1,
	-- Set the font used for the REPL and the console. This probably doesn't
	-- have to be a monospaced font.
	font = 'monospace',
	-- Set the font size used for the REPL and the console. This will be
	-- multiplied by "scale."
	['font-size'] = 16,
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

-- Build a list of commands, properties and options for tab-completion
local option_info = {
	'name', 'type', 'set-from-commandline', 'set-locally', 'default-value',
	'min', 'max', 'choices',
}
local cmd_list = {
	'ignore', 'seek', 'revert-seek', 'quit', 'quit-watch-later', 'stop',
	'frame-step', 'frame-back-step', 'playlist-next', 'playlist-prev',
	'playlist-shuffle', 'sub-step', 'sub-seek', 'osd', 'print-text',
	'show-text', 'show-progress', 'sub-add', 'sub-remove', 'sub-reload',
	'tv-last-channel', 'screenshot', 'screenshot-to-file', 'screenshot-raw',
	'loadfile', 'loadlist', 'playlist-clear', 'playlist-remove',
	'playlist-move', 'run', 'set', 'add', 'cycle', 'multiply', 'cycle-values',
	'enable-section', 'disable-section', 'define-section', 'ab-loop',
	'drop-buffers', 'af', 'af-command', 'ao-reload', 'vf', 'vf-command',
	'script-binding', 'script-message', 'script-message-to', 'overlay-add',
	'overlay-remove', 'write-watch-later-config', 'hook-add', 'hook-ack',
	'mouse', 'keypress', 'keydown', 'keyup', 'audio-add', 'audio-remove',
	'audio-reload', 'rescan-external-file', 'apply-profile', 'load-script',
}
local prop_list = mp.get_property_native('property-list')
for _, opt in ipairs(mp.get_property_native('options')) do
	prop_list[#prop_list + 1] = 'options/' .. opt
	prop_list[#prop_list + 1] = 'file-local-options/' .. opt
	prop_list[#prop_list + 1] = 'option-info/' .. opt
	for _, p in ipairs(option_info) do
		prop_list[#prop_list + 1] = 'option-info/' .. opt .. '/' .. p
	end
end

local repl_active = false
local insert_mode = false
local line = ''
local cursor = 1
local history = {}
local history_pos = 1
local log_ring = {}

-- Add a line to the log buffer (which is limited to 100 lines)
function log_add(style, text)
	log_ring[#log_ring + 1] = { style = style, text = text }
	if #log_ring > 100 then
		table.remove(log_ring, 1)
	end
end

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
	str = str:gsub('\n', '\239\187\191\\N')
	return str
end

-- Render the REPL and console as an ASS OSD
function update()
	local screenx, screeny, aspect = mp.get_osd_size()
	screenx = screenx / opts.scale
	screeny = screeny / opts.scale

	-- Clear the OSD if the REPL is not active
	if not repl_active then
		mp.set_osd_ass(screenx, screeny, '')
		return
	end

	local ass = assdraw.ass_new()
	local style = '{\\r' ..
	               '\\1a&H00&\\3a&H00&\\4a&H99&' ..
	               '\\1c&Heeeeee&\\3c&H111111&\\4c&H000000&' ..
	               '\\fn' .. opts.font .. '\\fs' .. opts['font-size'] ..
	               '\\bord2\\xshad0\\yshad1\\fsp0\\q1}'
	-- Create the cursor glyph as an ASS drawing. ASS will draw the cursor
	-- inline with the surrounding text, but it sets the advance to the width
	-- of the drawing. So the cursor doesn't affect layout too much, make it as
	-- thin as possible and make it appear to be 1px wide by giving it 0.5px
	-- horizontal borders.
	local cheight = opts['font-size'] * 8
	local cglyph = '{\\r' ..
	                '\\1a&H44&\\3a&H44&\\4a&H99&' ..
	                '\\1c&Heeeeee&\\3c&Heeeeee&\\4c&H000000&' ..
	                '\\xbord0.5\\ybord0\\xshad0\\yshad1\\p4\\pbo24}' ..
	               'm 0 0 l 1 0 l 1 ' .. cheight .. ' l 0 ' .. cheight ..
	               '{\\p0}'
	local before_cur = ass_escape(line:sub(1, cursor - 1))
	local after_cur = ass_escape(line:sub(cursor))

	-- Render log messages as ASS. This will render at most screeny / font-size
	-- messages.
	local log_ass = ''
	local log_messages = #log_ring
	local log_max_lines = math.ceil(screeny / opts['font-size'])
	if log_max_lines < log_messages then
		log_messages = log_max_lines
	end
	for i = #log_ring - log_messages + 1, #log_ring do
		log_ass = log_ass .. style .. log_ring[i].style .. ass_escape(log_ring[i].text)
	end

	ass:new_event()
	ass:an(1)
	ass:pos(2, screeny - 2)
	ass:append(log_ass .. '\\N')
	ass:append(style .. '> ' .. before_cur)
	ass:append(cglyph)
	ass:append(style .. after_cur)

	-- Redraw the cursor with the REPL text invisible. This will make the
	-- cursor appear in front of the text.
	ass:new_event()
	ass:an(1)
	ass:pos(2, screeny - 2)
	ass:append(style .. '{\\alpha&HFF&}> ' .. before_cur)
	ass:append(cglyph)
	ass:append(style .. '{\\alpha&HFF&}' .. after_cur)

	mp.set_osd_ass(screenx, screeny, ass.text)
end

-- Set the REPL visibility (`, Esc)
function set_active(active)
	if active == repl_active then return end
	if active then
		repl_active = true
		insert_mode = false
		mp.enable_key_bindings('repl-input', 'allow-hide-cursor+allow-vo-dragging')
	else
		repl_active = false
		mp.disable_key_bindings('repl-input')
	end
	update()
end

-- Show the repl if hidden and replace its contents with 'text'
-- (script-message-to repl type)
function show_and_type(text)
	text = text or ''

	-- Save the line currently being edited, just in case
	if line ~= text and line ~= '' and history[#history] ~= line then
		history[#history + 1] = line
	end

	line = text
	cursor = line:len() + 1
	history_pos = #history + 1
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

-- As above, but finds the previous UTF-8 charcter in 'str' before 'pos'
function prev_utf8(str, pos)
	if pos <= 1 then return pos end
	repeat
		pos = pos - 1
	until pos <= 1 or str:byte(pos) < 0x80 or str:byte(pos) > 0xbf
	return pos
end

-- Insert a character at the current cursor position (' '-'~', Shift+Enter)
function handle_char_input(c)
	if insert_mode then
		line = line:sub(1, cursor - 1) .. c .. line:sub(next_utf8(line, cursor))
	else
		line = line:sub(1, cursor - 1) .. c .. line:sub(cursor)
	end
	cursor = cursor + 1
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
	history_pos = #history + 1
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
	if line == '' then
		return
	end
	mp.command('print-text "<chat>'..line..'</chat>"')
	clear()
end

-- Go to the specified position in the command history
function go_history(new_pos)
	local old_pos = history_pos
	history_pos = new_pos

	-- Restrict the position to a legal value
	if history_pos > #history + 1 then
		history_pos = #history + 1
	elseif history_pos < 1 then
		history_pos = 1
	end

	-- Do nothing if the history position didn't actually change
	if history_pos == old_pos then
		return
	end

	-- If the user was editing a non-history line, save it as the last history
	-- entry. This makes it much less frustrating to accidentally hit Up/Down
	-- while editing a line.
	if old_pos == #history + 1 and line ~= '' and history[#history] ~= line then
		history[#history + 1] = line
	end

	-- Now show the history line (or a blank line for #history + 1)
	if history_pos <= #history then
		line = history[history_pos]
	else
		line = ''
	end
	cursor = line:len() + 1
	insert_mode = false
	update()
end

-- Go to the specified relative position in the command history (Up, Down)
function move_history(amount)
	go_history(history_pos + amount)
end

-- Go to the first command in the command history (PgUp)
function handle_pgup()
	go_history(1)
end

-- Stop browsing history and start editing a blank line (PgDown)
function handle_pgdown()
	go_history(#history + 1)
end

-- Move to the start of the current word, or if already at the start, the start
-- of the previous word. (Ctrl+Left)
function prev_word()
	-- This is basically the same as next_word() but backwards, so reverse the
	-- string in order to do a "backwards" find. This wouldn't be as annoying
	-- to do if Lua didn't insist on 1-based indexing.
	cursor = line:len() - select(2, line:reverse():find('%s*[^%s]*', line:len() - cursor + 2)) + 1
	update()
end

-- Move to the end of the current word, or if already at the end, the end of
-- the next word. (Ctrl+Right)
function next_word()
	cursor = select(2, line:find('%s*[^%s]*', cursor)) + 1
	update()
end

-- List of tab-completions:
--   pattern: A Lua pattern used in string:find. Should return the start and
--            end positions of the word to be completed in the first and second
--            capture groups (using the empty parenthesis notation "()")
--   list: A list of candidate completion values.
--   append: An extra string to be appended to the end of a successful
--           completion. It is only appended if 'list' contains exactly one
--           match.
local completers = {
	{ pattern = '^%s*()[%w_-]+()$', list = cmd_list, append = ' ' },
	{ pattern = '^%s*set%s+()[%w_/-]+()$', list = prop_list, append = ' ' },
	{ pattern = '^%s*set%s+"()[%w_/-]+()$', list = prop_list, append = '" ' },
	{ pattern = '^%s*add%s+()[%w_/-]+()$', list = prop_list, append = ' ' },
	{ pattern = '^%s*add%s+"()[%w_/-]+()$', list = prop_list, append = '" ' },
	{ pattern = '^%s*cycle%s+()[%w_/-]+()$', list = prop_list, append = ' ' },
	{ pattern = '^%s*cycle%s+"()[%w_/-]+()$', list = prop_list, append = '" ' },
	{ pattern = '^%s*multiply%s+()[%w_/-]+()$', list = prop_list, append = ' ' },
	{ pattern = '^%s*multiply%s+"()[%w_/-]+()$', list = prop_list, append = '" ' },
	{ pattern = '${()[%w_/-]+()$', list = prop_list, append = '}' },
}

-- Use 'list' to find possible tab-completions for 'part.' Returns the longest
-- common prefix of all the matching list items and a flag that indicates
-- whether the match was unique or not.
function complete_match(part, list)
	local completion = nil
	local full_match = false

	for _, candidate in ipairs(list) do
		if candidate:sub(1, part:len()) == part then
			if completion and completion ~= candidate then
				local prefix_len = part:len()
				while completion:sub(1, prefix_len + 1)
				       == candidate:sub(1, prefix_len + 1) do
					prefix_len = prefix_len + 1
				end
				completion = candidate:sub(1, prefix_len)
				full_match = false
			else
				completion = candidate
				full_match = true
			end
		end
	end

	return completion, full_match
end

-- Complete the option or property at the cursor (TAB)
function complete()
	local before_cur = line:sub(1, cursor - 1)
	local after_cur = line:sub(cursor)

	-- Try the first completer that works
	for _, completer in ipairs(completers) do
		-- Completer patterns should return the start and end of the word to be
		-- completed as the first and second capture groups
		local _, _, s, e = before_cur:find(completer.pattern)
		if not s then
			-- Multiple input commands can be separated by semicolons, so all
			-- completions that are anchored at the start of the string with
			-- '^' can start from a semicolon as well. Replace ^ with ; and try
			-- to match again.
			_, _, s, e = before_cur:find(completer.pattern:gsub('^^', ';'))
		end
		if s then
			-- If the completer's pattern found a word, check the completer's
			-- list for possible completions
			local part = before_cur:sub(s, e)
			local c, full = complete_match(part, completer.list)
			if c then
				-- If there was only one full match from the list, add
				-- completer.append to the final string. This is normally a
				-- space or a quotation mark followed by a space.
				if full and completer.append then
					c = c .. completer.append
				end

				-- Insert the completion and update
				before_cur = before_cur:sub(1, s - 1) .. c
				cursor = before_cur:len() + 1
				line = before_cur .. after_cur
				update()
				return
			end
		end
	end
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

-- Delete from the cursor to the end of the word (Ctrl+W)
function del_word()
	local before_cur = line:sub(1, cursor - 1)
	local after_cur = line:sub(cursor)

	before_cur = before_cur:gsub('[^%s]+%s*$', '', 1)
	line = before_cur .. after_cur
	cursor = before_cur:len() + 1
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

-- Empty the log buffer of all messages (Ctrl+L)
function clear_log_buffer()
	log_ring = {}
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
		mp.add_key_binding(nil, name, fn, 'repeatable')
		cfg = cfg .. key .. ' script-binding ' .. mp.script_name .. '/' ..
		      name .. '\n'
	end
	mp.commandv('define-section', 'repl-input', cfg, 'force')
end

-- Mapping from characters to mpv key names
local binding_name_map = {
	[' '] = 'SPACE',
	['#'] = 'SHARP',
}

-- List of input bindings. This is a weird mashup between common GUI text-input
-- bindings and readline bindings.
local bindings = {
	{ 'esc',         function() set_active(false) end       },
	{ 'enter',       handle_enter                           },
	{ 'shift+enter', function() handle_char_input('\n') end },
	{ 'bs',          handle_backspace                       },
	{ 'shift+bs',    handle_backspace                       },
	{ 'del',         handle_del                             },
	{ 'shift+del',   handle_del                             },
	{ 'ins',         handle_ins                             },
	{ 'shift+ins',   function() paste(false) end            },
	{ 'mouse_btn1',  function() paste(false) end            },
	{ 'left',        function() prev_char() end             },
	{ 'right',       function() next_char() end             },
	{ 'up',          function() move_history(-1) end        },
	{ 'axis_up',     function() move_history(-1) end        },
	{ 'mouse_btn3',  function() move_history(-1) end        },
	{ 'down',        function() move_history(1) end         },
	{ 'axis_down',   function() move_history(1) end         },
	{ 'mouse_btn4',  function() move_history(1) end         },
	{ 'axis_left',   function() end                         },
	{ 'axis_right',  function() end                         },
	{ 'ctrl+left',   prev_word                              },
	{ 'ctrl+right',  next_word                              },
	{ 'tab',         complete                               },
	{ 'home',        go_home                                },
	{ 'end',         go_end                                 },
	{ 'pgup',        handle_pgup                            },
	{ 'pgdwn',       handle_pgdown                          },
	{ 'ctrl+c',      clear                                  },
	{ 'ctrl+d',      maybe_exit                             },
	{ 'ctrl+k',      del_to_eol                             },
	{ 'ctrl+l',      clear_log_buffer                       },
	{ 'ctrl+u',      del_to_start                           },
	{ 'ctrl+v',      function() paste(true) end             },
	{ 'meta+v',      function() paste(true) end             },
	{ 'ctrl+w',      del_word                               },
}
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
add_repl_bindings(bindings)

-- Add a global binding for enabling the REPL. While it's enabled, its bindings
-- will take over and it can be closed with ESC.
mp.add_key_binding('`', 'repl-enable', function()
	set_active(true)
end)

-- Add a script-message to show the REPL and fill it with the provided text
mp.register_script_message('type', function(text)
	show_and_type(text)
end)

-- Redraw the REPL when the OSD size changes. This is needed because the
-- PlayRes of the OSD will need to be adjusted.
mp.observe_property('osd-width', 'native', update)
mp.observe_property('osd-height', 'native', update)

-- Watch for log-messages and print them in the REPL console
--mp.enable_messages('info')

mp.register_script_message('chat', function(e)
	log_add('', e .. '\r\n')
	update()
end)