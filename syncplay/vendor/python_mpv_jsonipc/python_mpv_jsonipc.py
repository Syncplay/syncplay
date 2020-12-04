import threading
import socket
import json
import os
import time
import subprocess
import random
import queue
import logging

log = logging.getLogger('mpv-jsonipc')

if os.name == "nt":
    import _winapi
    from multiprocessing.connection import PipeConnection

TIMEOUT = 120

# Older MPV versions do not allow us to dynamically retrieve the command list.
FALLBACK_COMMAND_LIST = [
    'ignore', 'seek', 'revert-seek', 'quit', 'quit-watch-later', 'stop', 'frame-step', 'frame-back-step',
    'playlist-next', 'playlist-prev', 'playlist-shuffle', 'playlist-unshuffle', 'sub-step', 'sub-seek',
    'print-text', 'show-text', 'expand-text', 'expand-path', 'show-progress', 'sub-add', 'audio-add',
    'video-add', 'sub-remove', 'audio-remove', 'video-remove', 'sub-reload', 'audio-reload', 'video-reload',
    'rescan-external-files', 'screenshot', 'screenshot-to-file', 'screenshot-raw', 'loadfile', 'loadlist',
    'playlist-clear', 'playlist-remove', 'playlist-move', 'run', 'subprocess', 'set', 'change-list', 'add',
    'cycle', 'multiply', 'cycle-values', 'enable-section', 'disable-section', 'define-section', 'ab-loop',
    'drop-buffers', 'af', 'vf', 'af-command', 'vf-command', 'ao-reload', 'script-binding', 'script-message',
    'script-message-to', 'overlay-add', 'overlay-remove', 'osd-overlay', 'write-watch-later-config',
    'hook-add', 'hook-ack', 'mouse', 'keybind', 'keypress', 'keydown', 'keyup', 'apply-profile',
    'load-script', 'dump-cache', 'ab-loop-dump-cache', 'ab-loop-align-cache']

class MPVError(Exception):
    """An error originating from MPV or due to a problem with MPV."""
    def __init__(self, *args, **kwargs):
        super(MPVError, self).__init__(*args, **kwargs)

class WindowsSocket(threading.Thread):
    """
    Wraps a Windows named pipe in a high-level interface. (Internal)
    
    Data is automatically encoded and decoded as JSON. The callback
    function will be called for each inbound message.
    """
    def __init__(self, ipc_socket, callback=None, quit_callback=None):
        """Create the wrapper.

        *ipc_socket* is the pipe name. (Not including \\\\.\\pipe\\)
        *callback(json_data)* is the function for recieving events.
        *quit_callback* is called when the socket connection dies.
        """
        ipc_socket = "\\\\.\\pipe\\" + ipc_socket
        self.callback = callback
        self.quit_callback = quit_callback
        
        access = _winapi.GENERIC_READ | _winapi.GENERIC_WRITE
        limit = 5 # Connection may fail at first. Try 5 times.
        for _ in range(limit):
            try:
                pipe_handle = _winapi.CreateFile(
                    ipc_socket, access, 0, _winapi.NULL, _winapi.OPEN_EXISTING,
                    _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL
                    )
                break
            except OSError:
                time.sleep(1)
        else:
            raise MPVError("Cannot connect to pipe.")
        self.socket = PipeConnection(pipe_handle)

        if self.callback is None:
            self.callback = lambda data: None

        threading.Thread.__init__(self)

    def stop(self, join=True):
        """Terminate the thread."""
        if self.socket is not None:
            self.socket.close()
        if join:
            self.join()

    def send(self, data):
        """Send *data* to the pipe, encoded as JSON."""
        try:
            self.socket.send_bytes(json.dumps(data).encode('utf-8') + b'\n')
        except OSError as ex:
            if len(ex.args) == 1 and ex.args[0] == "handle is closed":
                raise BrokenPipeError("handle is closed")
            raise ex

    def run(self):
        """Process pipe events. Do not run this directly. Use *start*."""
        data = b''
        try:
            while True:
                current_data = self.socket.recv_bytes(2048)
                if current_data == b'':
                    break

                data += current_data
                if data[-1] != 10:
                    continue

                data = data.decode('utf-8', 'ignore').encode('utf-8')
                for item in data.split(b'\n'):
                    if item == b'':
                        continue
                    json_data = json.loads(item)
                    self.callback(json_data)
                data = b''
        except EOFError:
            if self.quit_callback:
                self.quit_callback()

class UnixSocket(threading.Thread):
    """
    Wraps a Unix/Linux socket in a high-level interface. (Internal)
    
    Data is automatically encoded and decoded as JSON. The callback
    function will be called for each inbound message.
    """
    def __init__(self, ipc_socket, callback=None, quit_callback=None):
        """Create the wrapper.

        *ipc_socket* is the path to the socket.
        *callback(json_data)* is the function for recieving events.
        *quit_callback* is called when the socket connection dies.
        """
        self.ipc_socket = ipc_socket
        self.callback = callback
        self.quit_callback = quit_callback
        self.socket = socket.socket(socket.AF_UNIX)
        self.socket.connect(self.ipc_socket)

        if self.callback is None:
            self.callback = lambda data: None

        threading.Thread.__init__(self)

    def stop(self, join=True):
        """Terminate the thread."""
        if self.socket is not None:
            try:
                self.socket.shutdown(socket.SHUT_WR)
                self.socket.close()
                self.socket = None
            except OSError:
                pass # Ignore socket close failure.
        if join:
            self.join()

    def send(self, data):
        """Send *data* to the socket, encoded as JSON."""
        if self.socket is None:
            raise BrokenPipeError("socket is closed")
        self.socket.send(json.dumps(data).encode('utf-8') + b'\n')

    def run(self):
        """Process socket events. Do not run this directly. Use *start*."""
        data = b''
        while True:
            current_data = self.socket.recv(1024)
            if current_data == b'':
                break

            data += current_data
            if data[-1] != 10:
                continue

            data = data.decode('utf-8', 'ignore').encode('utf-8')
            for item in data.split(b'\n'):
                if item == b'':
                    continue
                json_data = json.loads(item)
                self.callback(json_data)
            data = b''
        if self.quit_callback:
            self.quit_callback()

class MPVProcess:
    """
    Manages an MPV process, ensuring the socket or pipe is available. (Internal)
    """
    def __init__(self, ipc_socket, mpv_location=None, env=None, **kwargs):
        """
        Create and start the MPV process. Will block until socket/pipe is available.

        *ipc_socket* is the path to the Unix/Linux socket or name of the Windows pipe.
        *mpv_location* is the path to mpv. If left unset it tries the one in the PATH.

        All other arguments are forwarded to MPV as command-line arguments.
        """
        if mpv_location is None:
            if os.name == 'nt':
                mpv_location = "mpv.exe"
            else:
                mpv_location = "mpv"
        
        log.debug("Staring MPV from {0}.".format(mpv_location))
        if os.name == 'nt':
            ipc_socket = "\\\\.\\pipe\\" + ipc_socket

        if os.name != 'nt' and os.path.exists(ipc_socket):
            os.remove(ipc_socket)

        log.debug("Using IPC socket {0} for MPV.".format(ipc_socket))
        self.ipc_socket = ipc_socket
        args = self._get_arglist(mpv_location, **kwargs)

        self._start_process(ipc_socket, args, env=env)

    def _start_process(self, ipc_socket, args, env):
        self.process = subprocess.Popen(args)
        ipc_exists = False
        for _ in range(100): # Give MPV 10 seconds to start.
            time.sleep(0.1)
            self.process.poll()
            if os.path.exists(ipc_socket):
                ipc_exists = True
                log.debug("Found MPV socket.")
                break
            if self.process.returncode is not None:
                log.error("MPV failed with returncode {0}.".format(self.process.returncode))
                break
        else:
            self.process.terminate()
            raise MPVError("MPV start timed out.")
        
        if not ipc_exists or self.process.returncode is not None:
            self.process.terminate()
            raise MPVError("MPV not started.")

    def _set_default(self, prop_dict, key, value):
        if key not in prop_dict:
            prop_dict[key] = value

    def _get_arglist(self, exec_location, **kwargs):
        args = [exec_location]
        self._set_default(kwargs, "idle", True)
        self._set_default(kwargs, "input_ipc_server", self.ipc_socket)
        self._set_default(kwargs, "input_terminal", False)
        self._set_default(kwargs, "terminal", False)
        args.extend("--{0}={1}".format(v[0].replace("_", "-"), self._mpv_fmt(v[1]))
                    for v in kwargs.items())
        return args

    def _mpv_fmt(self, data):
        if data == True:
            return "yes"
        elif data == False:
            return "no"
        else:
            return data

    def stop(self):
        """Terminate the process."""
        self.process.terminate()
        if os.name != 'nt' and os.path.exists(self.ipc_socket):
            os.remove(self.ipc_socket)

class MPVInter:
    """
    Low-level interface to MPV. Does NOT manage an mpv process. (Internal)
    """
    def __init__(self, ipc_socket, callback=None, quit_callback=None):
        """Create the wrapper.

        *ipc_socket* is the path to the Unix/Linux socket or name of the Windows pipe.
        *callback(event_name, data)* is the function for recieving events.
        *quit_callback* is called when the socket connection to MPV dies.
        """
        Socket = UnixSocket
        if os.name == 'nt':
            Socket = WindowsSocket

        self.callback = callback
        self.quit_callback = quit_callback
        if self.callback is None:
            self.callback = lambda event, data: None
        
        self.socket = Socket(ipc_socket, self.event_callback, self.quit_callback)
        self.socket.start()
        self.command_id = 1
        self.rid_lock = threading.Lock()
        self.socket_lock = threading.Lock()
        self.cid_result = {}
        self.cid_wait = {}
    
    def stop(self, join=True):
        """Terminate the underlying connection."""
        self.socket.stop(join)

    def event_callback(self, data):
        """Internal callback for recieving events from MPV."""
        if "request_id" in data:
            self.cid_result[data["request_id"]] = data
            self.cid_wait[data["request_id"]].set()
        elif "event" in data:
            self.callback(data["event"], data)
    
    def command(self, command, *args):
        """
        Issue a command to MPV. Will block until completed or timeout is reached.
        
        *command* is the name of the MPV command

        All further arguments are forwarded to the MPV command.
        Throws TimeoutError if timeout of 120 seconds is reached.
        """
        self.rid_lock.acquire()
        command_id = self.command_id
        self.command_id += 1
        self.rid_lock.release()

        event = threading.Event()
        self.cid_wait[command_id] = event

        command_list = [command]
        command_list.extend(args)
        try:
            self.socket_lock.acquire()
            self.socket.send({"command":command_list, "request_id": command_id})
        finally:
            self.socket_lock.release()

        has_event = event.wait(timeout=TIMEOUT)
        if has_event:
            data = self.cid_result[command_id]
            del self.cid_result[command_id]
            del self.cid_wait[command_id]
            if data["error"] != "success":
                if data["error"] == "property unavailable":
                    return None
                raise MPVError(data["error"])
            else:
                return data.get("data")
        else:
            raise TimeoutError("No response from MPV.")

class EventHandler(threading.Thread):
    """Event handling thread. (Internal)"""
    def __init__(self):
        """Create an instance of the thread."""
        self.queue = queue.Queue()
        threading.Thread.__init__(self)
    
    def put_task(self, func, *args):
        """
        Put a new task to the thread.
        
        *func* is the function to call
        
        All further arguments are forwarded to *func*.
        """
        self.queue.put((func, args))

    def stop(self, join=True):
        """Terminate the thread."""
        self.queue.put("quit")
        self.join(join)

    def run(self):
        """Process socket events. Do not run this directly. Use *start*."""
        while True:
            event = self.queue.get()
            if event == "quit":
                break
            try:
                event[0](*event[1])
            except Exception:
                log.error("EventHandler caught exception from {0}.".format(event), exc_info=1)

class MPV:
    """
    The main MPV interface class. Use this to control MPV.
    
    This will expose all mpv commands as callable methods and all properties.
    You can set properties and call the commands directly.
    
    Please note that if you are using a really old MPV version, a fallback command
    list is used. Not all commands may actually work when this fallback is used.
    """
    def __init__(self, start_mpv=True, ipc_socket=None, mpv_location=None,
                 log_handler=None, loglevel=None, quit_callback=None, **kwargs):
        """
        Create the interface to MPV and process instance.

        *start_mpv* will start an MPV process if true. (Default: True)
        *ipc_socket* is the path to the Unix/Linux socket or name of Windows pipe. (Default: Random Temp File)
        *mpv_location* is the location of MPV for *start_mpv*. (Default: Use MPV in PATH)
        *log_handler(level, prefix, text)* is an optional handler for log events. (Default: Disabled)
        *loglevel* is the level for log messages. Levels are fatal, error, warn, info, v, debug, trace. (Default: Disabled)
        *quit_callback* is called when the socket connection to MPV dies.

        All other arguments are forwarded to MPV as command-line arguments if *start_mpv* is used.
        """
        self.properties = {}
        self.event_bindings = {}
        self.key_bindings = {}
        self.property_bindings = {}
        self.mpv_process = None
        self.mpv_inter = None
        self.quit_callback = quit_callback
        self.event_handler = EventHandler()
        self.event_handler.start()
        if ipc_socket is None:
            rand_file = "mpv{0}".format(random.randint(0, 2**48))
            if os.name == "nt":
                ipc_socket = rand_file
            else:
                ipc_socket = "/tmp/{0}".format(rand_file)

        if start_mpv:
            self._start_mpv(ipc_socket, mpv_location, **kwargs)

        self.mpv_inter = MPVInter(ipc_socket, self._callback, self._quit_callback)
        self.properties = set(x.replace("-", "_") for x in self.command("get_property", "property-list"))
        try:
            command_list = [x["name"] for x in self.command("get_property", "command-list")]
        except MPVError:
            log.warning("Using fallback command list.")
            command_list = FALLBACK_COMMAND_LIST
        for command in command_list:
            object.__setattr__(self, command.replace("-", "_"), self._get_wrapper(command))

        self._dir = list(self.properties)
        self._dir.extend(object.__dir__(self))

        self.observer_id = 1
        self.observer_lock = threading.Lock()
        self.keybind_id = 1
        self.keybind_lock = threading.Lock()
        
        if log_handler is not None and loglevel is not None:
            self.command("request_log_messages", loglevel)
            @self.on_event("log-message")
            def log_handler_event(data):
                self.event_handler.put_task(log_handler, data["level"], data["prefix"], data["text"].strip())

        @self.on_event("property-change")
        def event_handler(data):
            if data.get("id") in self.property_bindings:
                self.event_handler.put_task(self.property_bindings[data["id"]], data["name"], data.get("data"))

        @self.on_event("client-message")
        def client_message_handler(data):
            args = data["args"]
            if len(args) == 2 and args[0] == "custom-bind":
                self.event_handler.put_task(self.key_bindings[args[1]])

    def _start_mpv(self, ipc_socket, mpv_location, **kwargs):
        # Attempt to start MPV 3 times.
        for i in range(3):
            try:
                self.mpv_process = MPVProcess(ipc_socket, mpv_location, **kwargs)
                break
            except MPVError:
                log.warning("MPV start failed.", exc_info=1)
                continue
        else:
            raise MPVError("MPV process retry limit reached.")

    def _quit_callback(self):
        """
        Internal handler for quit events.
        """
        if self.quit_callback:
            self.quit_callback()
        self.terminate(join=False)

    def bind_event(self, name, callback):
        """
        Bind a callback to an MPV event.

        *name* is the MPV event name.
        *callback(event_data)* is the function to call.
        """
        if name not in self.event_bindings:
            self.event_bindings[name] = set()
        self.event_bindings[name].add(callback)

    def on_event(self, name):
        """
        Decorator to bind a callback to an MPV event.

        @on_event(name)
        def my_callback(event_data):
            pass
        """
        def wrapper(func):
            self.bind_event(name, func)
            return func
        return wrapper

    # Added for compatibility.
    def event_callback(self, name):
        """An alias for on_event to maintain compatibility with python-mpv."""
        return self.on_event(name)

    def on_key_press(self, name):
        """
        Decorator to bind a callback to an MPV keypress event.

        @on_key_press(key_name)
        def my_callback():
            pass
        """
        def wrapper(func):
            self.bind_key_press(name, func)
            return func
        return wrapper

    def bind_key_press(self, name, callback):
        """
        Bind a callback to an MPV keypress event.

        *name* is the key symbol.
        *callback()* is the function to call.
        """
        self.keybind_lock.acquire()
        keybind_id = self.keybind_id
        self.keybind_id += 1
        self.keybind_lock.release()

        bind_name = "bind{0}".format(keybind_id)
        self.key_bindings["bind{0}".format(keybind_id)] = callback
        try:
            self.keybind(name, "script-message custom-bind {0}".format(bind_name))
        except MPVError:
            self.define_section(bind_name, "{0} script-message custom-bind {1}".format(name, bind_name))
            self.enable_section(bind_name)

    def bind_property_observer(self, name, callback):
        """
        Bind a callback to an MPV property change.

        *name* is the property name.
        *callback(name, data)* is the function to call.

        Returns a unique observer ID needed to destroy the observer.
        """
        self.observer_lock.acquire()
        observer_id = self.observer_id
        self.observer_id += 1
        self.observer_lock.release()

        self.property_bindings[observer_id] = callback
        self.command("observe_property", observer_id, name)
        return observer_id

    def unbind_property_observer(self, observer_id):
        """
        Remove callback to an MPV property change.

        *observer_id* is the id returned by bind_property_observer.
        """
        self.command("unobserve_property", observer_id)
        del self.property_bindings[observer_id]

    def property_observer(self, name):
        """
        Decorator to bind a callback to an MPV property change.

        @property_observer(property_name)
        def my_callback(name, data):
            pass
        """
        def wrapper(func):
            self.bind_property_observer(name, func)
            return func
        return wrapper
    
    def wait_for_property(self, name):
        """
        Waits for the value of a property to change.

        *name* is the name of the property.
        """
        event = threading.Event()
        first_event = True
        def handler(*_):
            nonlocal first_event
            if first_event == True:
                first_event = False
            else:
                event.set()
        observer_id = self.bind_property_observer(name, handler)
        event.wait()
        self.unbind_property_observer(observer_id)

    def _get_wrapper(self, name):
        def wrapper(*args):
            return self.command(name, *args)
        return wrapper

    def _callback(self, event, data):
        if event in self.event_bindings:
            for callback in self.event_bindings[event]:
                self.event_handler.put_task(callback, data)

    def play(self, url):
        """Play the specified URL. An alias to loadfile()."""
        self.loadfile(url)

    def __del__(self):
        self.terminate()

    def terminate(self, join=True):
        """Terminate the connection to MPV and process (if *start_mpv* is used)."""
        if self.mpv_process:
            self.mpv_process.stop()
        if self.mpv_inter:
            self.mpv_inter.stop(join)
        self.event_handler.stop(join)

    def command(self, command, *args):
        """
        Send a command to MPV. All commands are bound to the class by default,
        except JSON IPC specific commands. This may also be useful to retain
        compatibility with python-mpv, as it does not bind all of the commands. 

        *command* is the command name.

        All further arguments are forwarded to the MPV command. 
        """
        return self.mpv_inter.command(command, *args)

    def __getattr__(self, name):
        if name in self.properties:
            return self.command("get_property", name.replace("_", "-"))
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name not in {"properties", "command"} and name in self.properties:
            return self.command("set_property", name.replace("_", "-"), value)
        return object.__setattr__(self, name, value)

    def __hasattr__(self, name):
        if object.__hasattr__(self, name):
            return True
        else:
            try:
                getattr(self, name)
                return True
            except MPVError:
                return False

    def __dir__(self):
        return self._dir
