--[==========================================================================[
 syncplay.lua: Syncplay interface module for VLC
--[==========================================================================[

 Author: Etoh
 Project: http://syncplay.pl/
 Version: 0.1.6
 
 Note:
 * This interface module is intended to be used in conjunction with Syncplay.
 * Syncplay provides synchronized video playback across multiple media player instances over the net.
 * Syncplay allows group of people who all have the same videos to watch them together wherever they are.
 * Syncplay is available to download for free from http://syncplay.pl/
 
--[==========================================================================[

 === Installation instructions ===

Place the syncplay.lua file in the main (all user) VLC /lua/intf/ sub-directory. By default this should be:
* Window: %ProgramFiles%\VideoLAN\VLC\lua\intf\
* Linux: /usr/lib/vlc/lua/intf/
* Mac OS X: /Applications/VLC.app/Contents/MacOS/share/lua/intf/

If a directory does not exist then you may have to create it.

You may also need to re-copy the file when you update VLC.

 === Commands and responses ===
 = Note: ? denotes optional responses; * denotes mandatory response; uses \n terminator.

 [On connect]

 .
    ? >> inputstate-change: [<input/no-input>]
    ? >> filepath-change-notification
    
    * >> playstate: [<playing/paused/no-input>]
    * >> position: [<decimal seconds/no-input>]

 get-interface-version
    * >> interface-version: [syncplay connector version]
    
 get-duration
    * >> duration: [<duration/no-input>]
    
 get-filepath
    * >> filepath: [<filepath/no-input>]
    
 get-filename
    * >> filepath: [<filename/no-input>]
 
 set-position: [decimal seconds]
    ? >> play-error: no-input

 set-playstate: [<playing/paused>]
    ? >> set-playstate-error: no-input

 set-rate: [decimal rate]
    ? >> set-rate-error: no-input

 display-osd: [placement on screen <center/left/right/top/bottom/top-left/top-right/bottom-left/bottom-right>], [duration in seconds], [message]
    ? >> display-osd-error: no-input

 load-file: [filepath]
    * >> load-file-attempted

 close-vlc

 [Unknown command]
    * >> [Unknown command]-error: unknown-command

--]==========================================================================]

local modulepath = config["modulepath"]
if(modulepath ~= nil) and (modulepath ~= "") then
    -- Workaround for when the script is not being run from the usual VLC intf folder.
    package.path = modulepath
    pcall(require,"common")
else
    require "common"
end

local connectorversion = "0.1.6"
local durationdelay = 500000 -- Pause for get_duration command for increased reliability
local host = "localhost"
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
local unknownstream = "(Unknown Stream)"
    
local oldfilepath
local oldinputstate
local newfilepath
local newinputstate

local running = true

-- Start hosting Syncplay interface.

port = tonumber(config["port"])
if (port == nil or port < 1) then port = 4123 end

function quit_vlc()
    running = false
    vlc.misc.quit()
end

function detectchanges()
    -- Detects changes in VLC to report to Syncplay.
    -- [Used by the polll / "." command]

    local notificationbuffer = ""

        if vlc.object.input() then
            newinputstate = "input"
            newfilepath = get_filepath()
        
            if newfilepath ~= oldfilepath and get_filepath() ~= unknownstream then
                oldfilepath = newfilepath
                notificationbuffer = notificationbuffer .. "filepath-change"..notificationmarker..msgterminator
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
            notificationbuffer = notificationbuffer.."inputstate-change"..msgseperator..tostring(newinputstate)..msgterminator
        end
        
    return notificationbuffer
end

function get_args (argument, argcount)
    -- Converts comma-space-seperated values into array of a given size, with last item absorbing all remaining data if needed.
    -- [Used by the display-osd command]
    
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


function get_var( vartoget )
    -- [Used by the poll / '.' command to get time]
    
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
    -- [Used by the set-time and set-rate commands]
    
    local errormsg
    local input = vlc.object.input()
    
    if input then
        vlc.var.set(input,tostring(vartoset),tostring(varvalue))
    else
        errormsg = noinput
    end

    return  errormsg
end


function get_play_state()
    -- [Used by the get-playstate command]
    
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
    -- [Used by get-filepath command]
    
    local response
    local errormsg
    local item
    local input = vlc.object.input()
    
        if input then
            local item = vlc.input.item()
            if item then
                if string.find(item:uri(),"file://") then
                     response = vlc.strings.decode_uri(item:uri())
                else
                     local metas = item:metas()
                     if metas and metas["title"] and string.len(metas["title"]) > 0 then
                          response = ":::(Stream: "..metas["title"]..")"
                     else
                          response = unknownstream
                     end
                end
            else
                errormsg = noinput
            end
        else
            errormsg = noinput
        end
        
    return response, errormsg
end

function get_filename ()
    -- [Used by get-filename command]
    
    local response
    local index
    local filename
    filename = errormerge(get_filepath())
    
    if(filename ~= nil) and (filename ~= "") and (filename ~= noinput) then
        index = string.len(tostring(string.match(filename, ".*/")))
        if index then
            response = string.sub(tostring(filename), index+1)
        end
    else
          response = noinput
    end
    
    return response
end

function get_duration ()
    -- [Used by get-duration command]

    local response
    local errormsg
    local item
    local input = vlc.object.input()
    
        if input then
            local item = vlc.input.item()
            if (item and item:duration()) then
            -- Try to get duration, which might not be available straight away
                local i = 0            
                repeat
                    vlc.misc.mwait(vlc.misc.mdate() + durationdelay)
                    response = item:duration()
                    i = i + 1
                until response > 0 or i > 5
            else
                errormsg = noinput
            end
        else
            errormsg = noinput
        end
        
    return response, errormsg
end
    

function display_osd ( argument )
    -- [Used by display-osd command]
 
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

function load_file (filepath)
    -- [Used by load-file command]
    
    local uri = vlc.strings.make_uri(filepath)
    vlc.playlist.add({{path=uri}})
    return "load-file-attempted\n"
end

function do_command ( command, argument)
    -- Processes all commands sent by Syncplay (see protocol, above).
    
    if command == "." then
        do return detectchanges() end
    end
    local command = tostring(command)
    local argument = tostring(argument)
    local errormsg = ""
    local response = ""    

    if     command == "get-interface-version" then response           = "interface-version"..msgseperator..connectorversion..msgterminator
    elseif command == "get-duration"          then response           = "duration"..msgseperator..errormerge(get_duration())..msgterminator
    elseif command == "get-filepath"          then response           = "filepath"..msgseperator..errormerge(get_filepath())..msgterminator
    elseif command == "get-filename"          then response           = "filename"..msgseperator..errormerge(get_filename())..msgterminator
    elseif command == "set-position"          then           errormsg = set_var("time", tonumber(argument))
    elseif command == "set-playstate"         then           errormsg = set_playstate(argument)
    elseif command == "set-rate"              then           errormsg = set_var("rate", tonumber(argument))
    elseif command == "display-osd"           then           errormsg = display_osd(argument) 
    elseif command == "load-file"             then response           = load_file(argument)
    elseif command == "close-vlc"             then                      quit_vlc()
    else                                                     errormsg = unknowncommand
    end
    
    if (errormsg ~= nil) and (errormsg ~= "") then
        response = command..errormarker..msgseperator..tostring(errormsg)..msgterminator
    end

    return response
    
end

function errormerge(argument, errormsg)
    -- Used to integrate 'no-input' error messages into command responses.
    
    if (errormsg ~= nil) and (errormsg ~= "") then
        do return errormsg end
    end
    
    return argument
end

function set_playstate(argument)
    -- [Used by the set-playstate command]
    
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

if string.sub(vlc.misc.version(),1,2) ~= "2." then
    vlc.msg.err("This version of VLC is not known to support version " .. connectorversion .. " of the Syncplay interface module on Windows. Please use VLC 2.")
    quit_vlc()
else
    l = vlc.net.listen_tcp(host, port)
    vlc.msg.info("Hosting Syncplay interface on port: "..port)
end

    -- main loop, which alternates between writing and reading
    
while running do
    --accept new connections and select active clients
    local fd = l:accept()
    local buffer = ""
    while fd >= 0 do

        -- handle read mode
    
        local str = vlc.net.recv ( fd, 1000)
            
        local responsebuffer
        if str == nil then str = "" end
        
        local safestr = string.gsub(tostring(str), "\r", "")
        if inputbuffer == nil then inputbuffer = "" end
        
        inputbuffer = inputbuffer .. safestr

        while string.find(inputbuffer, msgterminator) do
            local index = string.find(inputbuffer, msgterminator)
            local request = string.sub(inputbuffer, 0, index - 1)
            local command
            local argument
            inputbuffer = string.sub(inputbuffer, index + string.len(msgterminator))

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
        
        -- handle write mode
        
        if (responsebuffer) then
            vlc.net.send( fd, responsebuffer )
            responsebuffer = ""
        end

    end

end
