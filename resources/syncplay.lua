--[==========================================================================[
 syncplay.lua: Syncplay interface module
--[==========================================================================[

 Author: Etoh

--]==========================================================================]
require "common"
require "host"

local connectorversion = "0.0.2"

local port

local msgterminator = "\n"
local msgseperator = ": "
local argseperator = ", "

local responsemarker = "-response"
local errormarker = "-error"

local noinput = "no-input"
local notimplemented = "not-implemented"
local unknowncommand = "unknown-command"

function get_args (argument, argcount)
	local argarray = {}
	local index
	local i
	local argbuffer
	
	argbuffer = argument

	for i = 1, argcount,1 do
		if i == argcount  then
			if argbuffer == nil then
				argarray[i] = ""
			else
				argarray[i] = argbuffer
			end
		else
			if string.find(argbuffer, argseperator) then
				index = string.find(argbuffer, argseperator)
				argarray[i] = string.sub(argbuffer, 0, index - 1)
				argbuffer = string.sub(argbuffer, index + string.len(argseperator))
			else
				argarray[i] = ""
			end
		end
		
	end
	
	return argarray
	
end


port = tonumber(config["port"])
if (port == nil or port < 1) then port = 4123 end

vlc.msg.info("Hosting Syncplay interface on port: "..port)

h = host.host()

    -- Bypass any authentication
function on_password( client )
	client:switch_status( host.status.read )
end

function get_var( vartoget )
	local response
	local errormsg
	local input = vlc.object.input()
	
	if input then
		response = vlc.var.get(input,tostring(vartoget))
	else
		errormsg = noinput
	end
	
		vlc.msg.info("getvar `"..tostring(vartoget).."`: '"..tostring(response).."'")
	
	return response, errormsg
end

function set_var(vartoset, varvalue)
	local errormsg
	local input = vlc.object.input()
	
	if input then
		vlc.var.set(input,tostring(vartoset),tostring(varvalue))
	else
		errormsg = noinput
	end
		vlc.msg.info("setvar: '"..tostring(vartoset).."' = '"..tostring(varvalue).."'")
	return  errormsg
end

h:listen( "localhost:"..port)
    --h:listen( "*console" )
	
function get_play_state()
	local response
	local errormsg
	local input = vlc.object.input()
		
		if input then
			response = vlc.playlist.status()
		else
			errormsg = noinput
		end

	vlc.msg.info("get play state: '"..tostring(response).."'")
	
	return response, errormsg
		
end

function get_filepath ()
	local response
	local errormsg
	local item
	local input = vlc.object.input()
	
		if input then
			local item = vlc.input.item()
			if item then
				response = vlc.strings.decode_uri(item:uri())
			else
				errormsg = noinput
			end
		else
			errormsg = noinput
		end
		
	return response, errormsg
end

function display_osd ( argument )
	local errormsg
	local osdarray
	local input = vlc.object.input()
	if input then
		osdarray = get_args(argument,3)
		--position, duration, message -> message, , position, duration
		vlc.osd.message(osdarray[3],channel1,osdarray[1],tonumber(osdarray[2]))
	else
		errormsg = noinput
	end
	return errormsg
end

	
function do_command ( command, argument)

	local command = tostring(command)
	local argument = tostring(argument)
	local errormsg = ""
	local response = ""

	vlc.msg.info("Command: '"..command.."'")
	vlc.msg.info("Argument: '"..argument.."'")
		
	local input = vlc.object.input()

	if 	   command == "get-playstate" 	then response, errormsg = get_play_state()
	elseif command == "get-time" 		then response, errormsg = get_var("time")
	elseif command == "get-filename"	then response, errormsg = get_var("title")
	elseif command == "get-file-length" then response, errormsg = get_var("length")
	elseif command == "get-filepath"	then response, errormsg = get_filepath()
	elseif command == "get-vlc-version"	then response 		  	= vlc.misc.version()
	elseif command == "get-version" 	then response			= connectorversion
	elseif command == "play" 			then 		   errormsg = playfile()
	elseif command == "pause" 			then 		   errormsg = pausefile()
	elseif command == "playpause" 		then 		   errormsg = playpausefile()
	elseif command == "seek" 			then  		   errormsg = set_var("time", tonumber(argument))
	elseif command == "set-rate" 		then 		   errormsg = set_var("rate", tonumber(argument))
	elseif command == "display-osd" 	then 		   errormsg = display_osd(argument) 
	else									 		   errormsg = unknowncommand
	end
	
	if (tostring(errormsg) == "" or errormsg == nil) then
		if (tostring(response) == "") then
			response = command..responsemarker..msgterminator
		else
			response = command..responsemarker..msgseperator..tostring(response)..msgterminator
		end
	else
		response = command..errormarker..msgseperator..tostring(errormsg)..msgterminator
	end

	vlc.msg.info("Response: '"..tostring(response).."'")

	return response
	
end

function playfile()
	local errormsg
	local input = vlc.object.input()
	local playstate
	playstate, errormsg = get_play_state()
	
	if playstate == "paused" then
		vlc.playlist.pause()
	end
	
	return errormsg
end


function pausefile()
	local errormsg
	local input = vlc.object.input()
	local playstate
	playstate, errormsg = get_play_state()
	
	if playstate == "playing" then
		vlc.playlist.pause()
	end
	
	return errormsg
end

function playpausefile()
	local errormsg
	local input = vlc.object.input()

	if input then
		vlc.playlist.pause()
	else
		errormsg = noinput
	end
	
	return errormsg
end

    -- main loop
while not vlc.misc.should_die() do
        -- accept new connections and select active clients
	local write, read = h:accept_and_select()

        -- handle clients in write mode
	for _, client in pairs(write) do
		client:send()
		client.buffer = ""
		client:switch_status( host.status.read )
	end

        -- handle clients in read mode
		
	for _, client in pairs(read) do
		local str = client:recv(1000)
		local responsebuffer
		if not str then break end
		
		local safestr = string.gsub(tostring(str), "\r", "")
		
		if client.inputbuffer == nil then
			client.inputbuffer = ""
		end
		
		client.inputbuffer = client.inputbuffer .. safestr
						
		vlc.msg.info("Str: '" .. safestr.."'")
		vlc.msg.info("Input buffer: '" .. client.inputbuffer.."'")
			
		while string.find(client.inputbuffer, msgterminator) do
			local index = string.find(client.inputbuffer, msgterminator)
			local request = string.sub(client.inputbuffer, 0, index - 1)
			local command
			local argument
			client.inputbuffer = string.sub(client.inputbuffer, index + string.len(msgterminator))

			if (string.find(request, msgseperator)) then
				index = string.find(request, msgseperator)
				command = string.sub(request, 0, index - 1)
				argument = string.sub(request, index  + string.len(msgseperator))
				
			else
				command = request
			end
			
			if (responsebuffer) then
				responsebuffer = responsebuffer .. do_command(command,argument)
			else
				responsebuffer = do_command(command,argument)
			end

		end
		
		client.buffer = ""
		if (responsebuffer) then
			client:send(responsebuffer)
		end
		client.buffer = ""
        client:switch_status( host.status.write )
    end
	
end
	
