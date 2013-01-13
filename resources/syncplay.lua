--[==========================================================================[
 syncplay.lua: Syncplay interface module
--[==========================================================================[

 Author: Etoh
 Project: http://syncplay.pl
 
--[==========================================================================[

 === Commands and response ===
 = Note: ? is optional response, * is mandatory response; uses \n terminator

 [On connect]
    >> VLC version

 .
    ? >> inputstate-change: [<input/no-input>]
    ? >> filepath-change: [filepath URI]
    ? >> file-length: [decimal seconds]
    
    * >> playstate: [<playing/paused/no-input>]
    * >> position: [<decimal seconds/no-input>]

 get-interface-version
    * >> interface-version: [sncplay connector version]

 set-position: [decimal seconds]
    ? >> play-error: no-input

 set-playstate: [<playing/paused>]
    ? >> set-playstate-error: no-input

 set-rate: [decimal rate]
    ? >> set-rate-error: no-input

 display-osd: [placement on screen <center/left/right/top/bottom/top-left/top-right/bottom-left/bottom-right>], [duration in seconds], [message]
    ? >> display-osd-error: no-input

 close-vlc

 [Unknown command]
    * >> [Unknown command]-error: unknown-command

--]==========================================================================]
require "common"
require "host"

local connectorversion = "0.0.3"

local port

local msgterminator = "\n"
local msgseperator = ": "
local argseperator = ", "

local responsemarker = "-response"
local errormarker = "-error"
local notificationmarker = "-notification"

local noinput = "no-input"
local notimplemented = "not-implemented"
local unknowncommand = "unknown-command"
    
local oldfilepath
local oldinputstate
local newfilepath
local newinputstate

function detectchanges()

    local notificationbuffer = ""

        if vlc.object.input() then
            newinputstate = "input"
            newfilepath = get_filepath()
        
            if newfilepath ~= oldfilepath then
                oldfilepath = newfilepath
                notificationbuffer = notificationbuffer .. "filepath-change"..msgseperator..tostring(newfilepath)..msgterminator
                notificationbuffer = notificationbuffer .. "file-length-change"..msgseperator..get_var("length")..msgterminator
            end
            
            notificationbuffer = notificationbuffer .. "playstate"..msgseperator..tostring(get_play_state())..msgterminator
            notificationbuffer = notificationbuffer .. "position"..msgseperator..tostring(get_var("time"))..msgterminator                        
        else
            notificationbuffer = notificationbuffer .. "playstate"..msgseperator..noinput..msgterminator
            notificationbuffer = notificationbuffer .. "position"..msgseperator..noinput..msgterminator
            newinputstate = noinput
        end
        
        if newinputstate ~= oldinputstate then
            oldinputstate = newinputstate
            notificationbuffer = "inputstate-change"..msgseperator..tostring(newinputstate)..msgterminator..notificationbuffer
        end
        
    return notificationbuffer
end

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

    return  errormsg
end

h:listen( "localhost:"..port)
--    h:listen( "*console" )
    
function get_play_state()
    local response
    local errormsg
    local input = vlc.object.input()
        
        if input then
            response = vlc.playlist.status()
        else
            errormsg = noinput
        end
        
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

function get_filename ()
    local response
    local errormsg
    local input = vlc.object.input()
    
        if input then
            local item = vlc.input.item()
            if item then
                response = item:name()
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
        --position, duration, message -> message, , position, duration (converted from seconds to microseconds)
        local osdduration = tonumber(osdarray[2]) * 1000 * 1000
        vlc.osd.message(osdarray[3],channel1,osdarray[1],osdduration)
    else
        errormsg = noinput
    end
    return errormsg
end

    
function do_command ( command, argument)
    if command == "." then
        do return detectchanges() end
    end
    local command = tostring(command)
    local argument = tostring(argument)
    local errormsg = ""
    local response = ""

    local input = vlc.object.input()
    
     

    if     command == "get-interface-version" then response           = "interface-version"..msgseperator..connectorversion..msgterminator
    elseif command == "set-position"          then           errormsg = set_var("time", tonumber(argument))
    elseif command == "set-playstate"         then           errormsg = set_playstate(argument)
    elseif command == "set-rate"              then           errormsg = set_var("rate", tonumber(argument))
    elseif command == "display-osd"           then           errormsg = display_osd(argument) 
    elseif command == "close-vlc"             then                      misc.quit()
    else                                                     errormsg = unknowncommand
    end
    
    if (tostring(errormsg) ~= nil) and (errormsg ~= "") then
        response = command..errormarker..msgseperator..tostring(errormsg)..msgterminator
    end

    return response
    
end

function set_playstate(argument)
    local errormsg
    local input = vlc.object.input()
    local playstate
    playstate, errormsg = get_play_state()
    
    if playstate ~= "playing" then playstate =    "paused" end
    if ((errormsg ~= noinput) and (playstate ~= argument)) then
        vlc.playlist.pause()
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
        
        if client.inputbuffer == nil then client.inputbuffer = "" end
        
        client.inputbuffer = client.inputbuffer .. safestr
            
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
