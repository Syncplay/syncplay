--[==========================================================================[
 syncplay.lua: Syncplay interface module for VLC
--[==========================================================================[

 Principal author: Etoh
 Other contributors: DerGenaue, jb, Pilotat
 Project: https://syncplay.pl/
 Version: 0.3.7

 Note:
 * This interface module is intended to be used in conjunction with Syncplay.
 * Syncplay provides synchronized video playback across multiple media player instances over the net.
 * Syncplay allows group of people who all have the same videos to watch them together wherever they are.
 * Syncplay is available to download for free from https://syncplay.pl/

--[==========================================================================[

 === Installation instructions ===

Syncplay should install this automatically to your user folder.

 === Commands and responses ===
 = Note: ? denotes optional responses; * denotes mandatory response; uses \n terminator.

 .
    ? >> inputstate-change: [<input/no-input>]
    ? >> filepath-change-notification

    * >> playstate: [<playing/paused/no-input>]
    * >> position: [<decimal seconds/no-input>]

 get-interface-version
    * >> interface-version: [syncplay connector version]

 get-vlc-version
    * >> vlc-version: [VLC version]

 get-duration
    * >> duration: [<duration/no-input>]

 get-filepath
    * >> filepath: [<filepath/no-input>]

 get-filename
    * >> filepath: [<filename/no-input>]

 get-title
    * >> title: [<title/no-input>]

 set-position: [decimal seconds]
    ? >> play-error: no-input

 seek-within-title: [decimal seconds]
    ? >> seek-within-title-error: no-input

 set-playstate: [<playing/paused>]
    ? >> set-playstate-error: no-input

 set-rate: [decimal rate]
    ? >> set-rate-error: no-input

 set-title
    ? >> set-title-error: no-input

 display-osd: [placement on screen <center/left/right/top/bottom/top-left/top-right/bottom-left/bottom-right>], [duration in seconds], [message]
    ? >> display-osd-error: no-input

 display-secondary-osd: [placement on screen <center/left/right/top/bottom/top-left/top-right/bottom-left/bottom-right>], [duration in seconds], [message]
    ? >> display-secondary-osd-error: no-input

 load-file: [filepath]
    * >> load-file-attempted

 close-vlc

 [Unknown command]
    * >> [Unknown command]-error: unknown-command

--]==========================================================================]

local connectorversion = "0.3.7"
local vlcversion = vlc.misc.version()
local vlcmajorversion = tonumber(vlcversion:sub(1,1)) -- get the major version of VLC

if vlcmajorversion > 3 then
    vlc.misc.quit()
end

local durationdelay = 500000 -- Pause for get_duration command etc for increased reliability (uses microseconds)
local loopsleepduration = 2500 -- Pause for every event loop (uses microseconds)
local quitcheckfrequency = 20 -- Check whether VLC has closed every X loops

local host = "127.0.0.1"
local port

local titlemultiplier = 604800 -- One week

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
local oldtitle = 0
local newtitle = 0
local oldduration = 0
local newduration = 0

local channel1
local channel2
local l

local running = true


function radixsafe_tonumber(str)
    -- Version of tonumber that works with any radix character (but not thousand seperators)
    -- Based on the public domain VLC common.lua us_tonumber() function

    str = string.gsub(tostring(str), "[^0-9]", ".")
    local s, i, d = string.match(str, "^([+-]?)(%d*)%.?(%d*)$")
    if not s or not i or not d then
        return nil
    end

    if s == "-" then
        s = -1
    else
        s = 1
    end
    if i == "" then
        i = "0"
    end
    if d == nil or d == "" then
        d = "0"
    end
    return s * (tonumber(i) + tonumber(d)/(10^string.len(d)))
end

-- Start hosting Syncplay interface.

port = radixsafe_tonumber(config["port"])
if (port == nil or port < 1) then port = 4123 end

function quit_vlc()
    running = false
    vlc.misc.quit()
end

function detectchanges()
    -- Detects changes in VLC to report to Syncplay.
    -- [Used by the poll / "." command]

    local notificationbuffer = ""

        if vlc.object.input() then
            newinputstate = "input"
            newfilepath = get_filepath()

            if newfilepath ~= oldfilepath and get_filepath() ~= unknownstream then
                oldfilepath = newfilepath
                notificationbuffer = notificationbuffer .. "filepath-change"..notificationmarker..msgterminator
            end

            local titleerror
            newtitle, titleerror = get_var("title", 0)
            if newtitle ~= oldtitle and get_var("time", 0) > 1 then
                vlc.misc.mwait(vlc.misc.mdate() + durationdelay) -- Don't give new title with old time
            end
            oldtitle = newtitle
            notificationbuffer = notificationbuffer .. "playstate"..msgseperator..tostring(get_play_state())..msgterminator
            notificationbuffer = notificationbuffer .. "position"..msgseperator..tostring(get_time())..msgterminator
            notificationbuffer = notificationbuffer .. "rate"..msgseperator..tostring(get_var("rate", 0))..msgterminator
            newduration = get_duration()
            if oldduration ~= newduration then
                oldduration = newduration
                notificationbuffer = notificationbuffer .. "duration-change"..msgseperator..tostring(newduration)..msgterminator
            end
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


function get_var( vartoget, fallbackvar )
    -- [Used by the poll / '.' command to get time]

    local response
    local errormsg
    local input = vlc.object.input()

    if input then
        response = vlc.var.get(input,tostring(vartoget))
    else
        response = fallbackvar
        errormsg = noinput
    end

    if vlcmajorversion > 2 and vartoget == "time" then
        response = response / 1000000
    end

    return response, errormsg
end


function set_var(vartoset, varvalue)
    -- [Used by the set-time and set-rate commands]

    local errormsg
    local input = vlc.object.input()

    if vlcmajorversion > 2 and vartoset == "time" then
        varvalue = varvalue * 1000000
    end

    if input then
        vlc.var.set(input,tostring(vartoset),varvalue)
    else
        errormsg = noinput
    end

    -- Also set rate on playlist object so VLC's hotkey speed stepping
    -- uses the externally-set rate as its base (not a cached old value)
    if vartoset == "rate" then
        local playlist = vlc.object.playlist()
        if playlist then
            vlc.var.set(playlist, "rate", varvalue)
        end
    end

    return  errormsg
end

function get_time()
    local realtime, errormsg, longtime, title, titletime
    realtime, errormsg = get_var("time", 0) -- Seconds
    if errormsg ~= nil and errormsg ~= "" then
        return errormsg
    end

    title = get_var("title", 0)

    if errormsg ~= nil and errormsg ~= "" then
        return realtime
    end
    titletime = title * titlemultiplier -- weeks
    longtime = titletime + realtime
    return longtime
end

function set_time ( timetoset)
    local input = vlc.object.input()
    if input then
        local response, errormsg, realtime, titletrack
        realtime = timetoset % titlemultiplier
        oldtitle = radixsafe_tonumber(get_var("title", 0))
        newtitle = (timetoset - realtime) / titlemultiplier
        if oldtitle ~= newtitle and newtitle > -1 then
            set_var("title", radixsafe_tonumber(newtitle))
        end
        errormsg = set_var("time", radixsafe_tonumber(realtime))
        return errormsg
    else
        return noinput
    end
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
                elseif string.find(item:uri(),"dvd://") or string.find(item:uri(),"simpledvd://") then
                     response = ":::DVD:::"
                else
                     local metas = item:metas()
                     if metas and metas["url"] and string.len(metas["url"]) > 0 then
                          response = metas["url"]
                     elseif item:uri() and string.len(item:uri()) > 0 then
                          response = item:uri()
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
    if filename == unknownstream then
        return unknownstream
    end
    if filename == "" then
        local input = vlc.object.input()
        if input then
            local item = vlc.input.item()
            if item then
                if item.name then
                    response = ":::("..item.title..")"
                    return response
                end
            end
        end
    end

    if(filename ~= nil) and (filename ~= "") and (filename ~= noinput) then
        index = string.len(tostring(string.match(filename, ".*/")))
        if string.sub(filename,1,3) == ":::" then
            return filename
        elseif index then
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
            -- Try to get duration, which might not be available straight away
            local i = 0
            response = 0
            repeat
                -- vlc.misc.mwait(vlc.misc.mdate() + durationdelay)
                if item and item:duration() then
                    response = item:duration()
                    if response < 1 then
                        response = 0
                    elseif string.sub(vlcversion,1,5) == "3.0.0" and response > 2147 and math.abs(response-(vlc.var.get(input,"length")/1000000)) > 5 then
                        errormsg = "invalid-32-bit-value"
                    end
                end
                i = i + 1
            until response > 1 or i > 5
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
    if input and vlc.osd and vlc.object.vout() then
        if not channel1 then
            channel1 = vlc.osd.channel_register()
        end
        if not channel2 then
            channel2 = vlc.osd.channel_register()
        end
        osdarray = get_args(argument,3)
        --position, duration, message -> message, , position, duration (converted from seconds to microseconds)
        local osdduration = radixsafe_tonumber(osdarray[2]) * 1000 * 1000
        vlc.osd.message(osdarray[3],channel1,osdarray[1],osdduration)
    else
        errormsg = noinput
    end
    return errormsg
end

function display_secondary_osd ( argument )
    -- [Used by display-secondary-osd command]
    local errormsg
    local osdarray
    local input = vlc.object.input()
    if input and vlc.osd and vlc.object.vout() then
        if not channel1 then
            channel1 = vlc.osd.channel_register()
        end
        if not channel2 then
            channel2 = vlc.osd.channel_register()
        end
        osdarray = get_args(argument,3)
        --position, duration, message -> message, , position, duration (converted from seconds to microseconds)
        local osdduration = radixsafe_tonumber(osdarray[2]) * 1000 * 1000
        vlc.osd.message(osdarray[3],channel2,osdarray[1],osdduration)
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
    elseif command == "get-vlc-version"       then response           = "vlc-version"..msgseperator..vlcversion..msgterminator
    elseif command == "get-duration"          then
        newduration = errormerge(get_duration())
        response           = "duration"..msgseperator..newduration..msgterminator
        oldduration = newduration
    elseif command == "get-filepath"          then response           = "filepath"..msgseperator..errormerge(get_filepath())..msgterminator
    elseif command == "get-filename"          then response           = "filename"..msgseperator..errormerge(get_filename())..msgterminator
    elseif command == "get-title"             then response           = "title"..msgseperator..errormerge(get_var("title", 0))..msgterminator
    elseif command == "set-position"          then           errormsg = set_time(radixsafe_tonumber(argument))
    elseif command == "seek-within-title"     then           errormsg = set_var("time", radixsafe_tonumber(argument))
    elseif command == "set-playstate"         then           errormsg = set_playstate(argument)
    elseif command == "set-rate"              then           errormsg = set_var("rate", radixsafe_tonumber(argument))
    elseif command == "set-title"             then           errormsg = set_var("title", radixsafe_tonumber(argument))
    elseif command == "display-osd"           then           errormsg = display_osd(argument)
    elseif command == "display-secondary-osd" then           errormsg = display_secondary_osd(argument)
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

if string.sub(vlcversion,1,2) == "1." or string.sub(vlcversion,1,3) == "2.0" or string.sub(vlcversion,1,3) == "2.1" or string.sub(vlcversion,1,5) == "2.2.0" then
    vlc.msg.err("This version of VLC does not support Syncplay. Please use VLC 2.2.1+ or an alternative media player.")
    quit_vlc()
else
    l = vlc.net.listen_tcp(host, port)
    vlc.msg.info("Hosting Syncplay interface on port: "..port)
end

    -- main loop, which alternates between writing and reading

while running == true do
    --accept new connections and select active clients
    local quitcheckcounter = 0
    local fd = l:accept()
    local buffer, inputbuffer, responsebuffer = "", "", ""
    while fd >= 0 and running == true do

        -- handle read mode

        local str = vlc.net.recv ( fd, 1000)

        local responsebuffer
        if str == nil then str = "" end

        local safestr = string.gsub(tostring(str), "\r", "")
        if inputbuffer == nil then inputbuffer = "" end

        inputbuffer = inputbuffer .. safestr

        while string.find(inputbuffer, msgterminator) and running == true do
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

        if (running == false) then
            net.close(fd)
        end

        -- handle write mode

        if (responsebuffer and running == true) then
            vlc.net.send( fd, responsebuffer )
            responsebuffer = ""
        end
        vlc.misc.mwait(vlc.misc.mdate() + loopsleepduration) -- Don't waste processor time

        -- check if VLC has been closed

        quitcheckcounter = quitcheckcounter + 1

        if quitcheckcounter > quitcheckfrequency then
            if vlc.volume.get() == -256 then
                running = false
            end
            quitcheckcounter = 0
        end

    end

end
