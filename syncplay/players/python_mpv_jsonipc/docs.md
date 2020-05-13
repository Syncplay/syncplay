<a name=".python_mpv_jsonipc"></a>

## python\_mpv\_jsonipc

<a name=".python_mpv_jsonipc.MPVError"></a>

### MPVError

``` python
class MPVError(Exception):
 |  MPVError(**args, ****kwargs)
```

An error originating from MPV or due to a problem with MPV.

<a name=".python_mpv_jsonipc.WindowsSocket"></a>

### WindowsSocket

``` python
class WindowsSocket(threading.Thread)
```

Wraps a Windows named pipe in a high-level interface. (Internal)

Data is automatically encoded and decoded as JSON. The callback  
function will be called for each inbound message.

<a name=".python_mpv_jsonipc.WindowsSocket.__init__"></a>

#### \_\_init\_\_

``` python
 | __init__(ipc_socket, callback=None, quit_callback=None)
```

Create the wrapper.

**ipc\_socket** is the pipe name. (Not including \\\\.\\pipe\\)  
**callback(json\_data)** is the function for recieving events.

<a name=".python_mpv_jsonipc.WindowsSocket.stop"></a>

#### stop

``` python
 | stop()
```

Terminate the thread.

<a name=".python_mpv_jsonipc.WindowsSocket.send"></a>

#### send

``` python
 | send(data)
```

Send **data** to the pipe, encoded as JSON.

<a name=".python_mpv_jsonipc.WindowsSocket.run"></a>

#### run

``` python
 | run()
```

Process pipe events. Do not run this directly. Use **start**.

<a name=".python_mpv_jsonipc.UnixSocket"></a>

### UnixSocket

``` python
class UnixSocket(threading.Thread)
```

Wraps a Unix/Linux socket in a high-level interface. (Internal)

Data is automatically encoded and decoded as JSON. The callback  
function will be called for each inbound message.

<a name=".python_mpv_jsonipc.UnixSocket.__init__"></a>

#### \_\_init\_\_

``` python
 | __init__(ipc_socket, callback=None, quit_callback=None)
```

Create the wrapper.

**ipc\_socket** is the path to the socket.  
**callback(json\_data)** is the function for recieving events.

<a name=".python_mpv_jsonipc.UnixSocket.stop"></a>

#### stop

``` python
 | stop()
```

Terminate the thread.

<a name=".python_mpv_jsonipc.UnixSocket.send"></a>

#### send

``` python
 | send(data)
```

Send **data** to the socket, encoded as JSON.

<a name=".python_mpv_jsonipc.UnixSocket.run"></a>

#### run

``` python
 | run()
```

Process socket events. Do not run this directly. Use **start**.

<a name=".python_mpv_jsonipc.MPVProcess"></a>

### MPVProcess

``` python
class MPVProcess()
```

Manages an MPV process, ensuring the socket or pipe is available. (Internal)

<a name=".python_mpv_jsonipc.MPVProcess.__init__"></a>

#### \_\_init\_\_

``` python
 | __init__(ipc_socket, mpv_location=None, ****kwargs)
```

Create and start the MPV process. Will block until socket/pipe is available.

**ipc\_socket** is the path to the Unix/Linux socket or name of the Windows pipe.  
**mpv\_location** is the path to mpv. If left unset it tries the one in the PATH.

All other arguments are forwarded to MPV as command-line arguments.

<a name=".python_mpv_jsonipc.MPVProcess.stop"></a>

#### stop

``` python
 | stop()
```

Terminate the process.

<a name=".python_mpv_jsonipc.MPVInter"></a>

### MPVInter

``` python
class MPVInter()
```

Low-level interface to MPV. Does NOT manage an mpv process. (Internal)

<a name=".python_mpv_jsonipc.MPVInter.__init__"></a>

#### \_\_init\_\_

``` python
 | __init__(ipc_socket, callback=None, quit_callback=None)
```

Create the wrapper.

**ipc\_socket** is the path to the Unix/Linux socket or name of the Windows pipe.  
**callback(event\_name, data)** is the function for recieving events.

<a name=".python_mpv_jsonipc.MPVInter.stop"></a>

#### stop

``` python
 | stop()
```

Terminate the underlying connection.

<a name=".python_mpv_jsonipc.MPVInter.event_callback"></a>

#### event\_callback

``` python
 | event_callback(data)
```

Internal callback for recieving events from MPV.

<a name=".python_mpv_jsonipc.MPVInter.command"></a>

#### command

``` python
 | command(command, **args)
```

Issue a command to MPV. Will block until completed or timeout is reached.

**command** is the name of the MPV command

All further arguments are forwarded to the MPV command.  
Throws TimeoutError if timeout of 120 seconds is reached.

<a name=".python_mpv_jsonipc.EventHandler"></a>

### EventHandler

``` python
class EventHandler(threading.Thread)
```

Event handling thread. (Internal)

<a name=".python_mpv_jsonipc.EventHandler.__init__"></a>

#### \_\_init\_\_

``` python
 | __init__()
```

Create an instance of the thread.

<a name=".python_mpv_jsonipc.EventHandler.put_task"></a>

#### put\_task

``` python
 | put_task(func, **args)
```

Put a new task to the thread.

**func** is the function to call

All further arguments are forwarded to **func**.

<a name=".python_mpv_jsonipc.EventHandler.stop"></a>

#### stop

``` python
 | stop()
```

Terminate the thread.

<a name=".python_mpv_jsonipc.EventHandler.run"></a>

#### run

``` python
 | run()
```

Process socket events. Do not run this directly. Use **start**.

<a name=".python_mpv_jsonipc.MPV"></a>

### MPV

``` python
class MPV()
```

The main MPV interface class. Use this to control MPV.

This will expose all mpv commands as callable methods and all properties.  
You can set properties and call the commands directly.

Please note that if you are using a really old MPV version, a fallback command  
list is used. Not all commands may actually work when this fallback is used.

<a name=".python_mpv_jsonipc.MPV.__init__"></a>

#### \_\_init\_\_

``` python
 | __init__(start_mpv=True, ipc_socket=None, mpv_location=None, log_handler=None, loglevel=None, quit_callback=None, ****kwargs)
```

Create the interface to MPV and process instance.

**start\_mpv** will start an MPV process if true. (Default: True)  
**ipc\_socket** is the path to the Unix/Linux socket or name of Windows pipe. (Default: Random Temp File)  
**mpv\_location** is the location of MPV for **start\_mpv**. (Default: Use MPV in PATH)  
**log\_handler(level, prefix, text)** is an optional handler for log events. (Default: Disabled)  
**loglevel** is the level for log messages. Levels are fatal, error, warn, info, v, debug, trace. (Default: Disabled)

All other arguments are forwarded to MPV as command-line arguments if **start\_mpv** is used.

<a name=".python_mpv_jsonipc.MPV.bind_event"></a>

#### bind\_event

``` python
 | bind_event(name, callback)
```

Bind a callback to an MPV event.

**name** is the MPV event name.  
**callback(event\_data)** is the function to call.

<a name=".python_mpv_jsonipc.MPV.on_event"></a>

#### on\_event

``` python
 | on_event(name)
```

Decorator to bind a callback to an MPV event.

@on\_event(name)  
def my\_callback(event\_data):  
pass

<a name=".python_mpv_jsonipc.MPV.event_callback"></a>

#### event\_callback

``` python
 | event_callback(name)
```

An alias for on\_event to maintain compatibility with python-mpv.

<a name=".python_mpv_jsonipc.MPV.on_key_press"></a>

#### on\_key\_press

``` python
 | on_key_press(name)
```

Decorator to bind a callback to an MPV keypress event.

@on\_key\_press(key\_name)  
def my\_callback():  
pass

<a name=".python_mpv_jsonipc.MPV.bind_key_press"></a>

#### bind\_key\_press

``` python
 | bind_key_press(name, callback)
```

Bind a callback to an MPV keypress event.

**name** is the key symbol.  
**callback()** is the function to call.

<a name=".python_mpv_jsonipc.MPV.bind_property_observer"></a>

#### bind\_property\_observer

``` python
 | bind_property_observer(name, callback)
```

Bind a callback to an MPV property change.

**name** is the property name.  
**callback(name, data)** is the function to call.

Returns a unique observer ID needed to destroy the observer.

<a name=".python_mpv_jsonipc.MPV.unbind_property_observer"></a>

#### unbind\_property\_observer

``` python
 | unbind_property_observer(observer_id)
```

Remove callback to an MPV property change.

**observer\_id** is the id returned by bind\_property\_observer.

<a name=".python_mpv_jsonipc.MPV.property_observer"></a>

#### property\_observer

``` python
 | property_observer(name)
```

Decorator to bind a callback to an MPV property change.

@property\_observer(property\_name)  
def my\_callback(name, data):  
pass

<a name=".python_mpv_jsonipc.MPV.wait_for_property"></a>

#### wait\_for\_property

``` python
 | wait_for_property(name)
```

Waits for the value of a property to change.

**name** is the name of the property.

<a name=".python_mpv_jsonipc.MPV.play"></a>

#### play

``` python
 | play(url)
```

Play the specified URL. An alias to loadfile().

<a name=".python_mpv_jsonipc.MPV.terminate"></a>

#### terminate

``` python
 | terminate()
```

Terminate the connection to MPV and process (if **start\_mpv** is used).

<a name=".python_mpv_jsonipc.MPV.command"></a>

#### command

``` python
 | command(command, **args)
```

Send a command to MPV. All commands are bound to the class by default,  
except JSON IPC specific commands. This may also be useful to retain  
compatibility with python-mpv, as it does not bind all of the commands.

**command** is the command name.

All further arguments are forwarded to the MPV command.
