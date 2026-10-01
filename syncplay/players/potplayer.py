import os
import subprocess
import sys
import threading
import time

if not sys.platform.startswith("win"):
    raise ImportError("PotPlayer is only available on Windows")

import ctypes
import ctypes.wintypes as wintypes

from syncplay import constants, utils
from syncplay.messages import getMessage
from syncplay.players.basePlayer import BasePlayer

_user32 = ctypes.WinDLL("user32", use_last_error=True)
_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

_LRESULT = ctypes.c_ssize_t
_WPARAM = ctypes.c_size_t
_LPARAM = ctypes.c_ssize_t
_WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
_WNDPROC = ctypes.WINFUNCTYPE(_LRESULT, wintypes.HWND, wintypes.UINT, _WPARAM, _LPARAM)

_WM_CLOSE = 0x0010
_WM_COPYDATA = 0x004A
_WM_USER = 0x0400
_SMTO_ABORTIFHUNG = 0x0002
_PM_REMOVE = 0x0001
_QS_ALLINPUT = 0x04FF
_MSGFLT_ALLOW = 1
_HWND_MESSAGE = wintypes.HWND(-3)


class _COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [("dwData", ctypes.c_size_t), ("cbData", wintypes.DWORD), ("lpData", ctypes.c_void_p)]


class _WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT), ("lpfnWndProc", _WNDPROC), ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int), ("hInstance", wintypes.HINSTANCE), ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HANDLE), ("hbrBackground", wintypes.HBRUSH), ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR)
    ]


_user32.SendMessageTimeoutW.argtypes = [
    wintypes.HWND, wintypes.UINT, _WPARAM, _LPARAM, wintypes.UINT, wintypes.UINT, ctypes.POINTER(_LRESULT)]
_user32.SendMessageTimeoutW.restype = _LRESULT
_user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, _WPARAM, _LPARAM]
_user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, _WPARAM, _LPARAM]
_user32.DefWindowProcW.restype = _LRESULT
_user32.EnumWindows.argtypes = [_WNDENUMPROC, wintypes.LPARAM]
_user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
_user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
_user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
_user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
_user32.IsWindow.argtypes = [wintypes.HWND]
_user32.DestroyWindow.argtypes = [wintypes.HWND]
_user32.RegisterClassW.argtypes = [ctypes.POINTER(_WNDCLASSW)]
_user32.RegisterClassW.restype = wintypes.ATOM
_user32.CreateWindowExW.argtypes = [
    wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID]
_user32.CreateWindowExW.restype = wintypes.HWND
_user32.ChangeWindowMessageFilterEx.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.DWORD, wintypes.LPVOID]
_user32.PeekMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT, wintypes.UINT]
_user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
_user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]
_user32.MsgWaitForMultipleObjects.argtypes = [wintypes.DWORD, wintypes.LPVOID, wintypes.BOOL, wintypes.DWORD, wintypes.DWORD]
_kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
_kernel32.GetModuleHandleW.restype = wintypes.HMODULE


def _windowPid(hwnd):
    pid = wintypes.DWORD()
    _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def _windowClass(hwnd):
    buffer = ctypes.create_unicode_buffer(256)
    _user32.GetClassNameW(hwnd, buffer, 256)
    return buffer.value


def _windowText(hwnd):
    length = _user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    _user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value


class _CopyDataReceiver(object):
    """Hidden message-only window collecting the WM_COPYDATA answers PotPlayer sends back."""

    _classCounter = 0
    _classLock = threading.Lock()

    def __init__(self):
        self.replies = {}
        self._wndProc = _WNDPROC(self._handleMessage)  # must stay referenced while the window exists
        with _CopyDataReceiver._classLock:
            _CopyDataReceiver._classCounter += 1
            className = "SyncplayPotPlayerReceiver{}_{}".format(os.getpid(), _CopyDataReceiver._classCounter)
        instance = _kernel32.GetModuleHandleW(None)
        windowClass = _WNDCLASSW(lpfnWndProc=self._wndProc, hInstance=instance, lpszClassName=className)
        if not _user32.RegisterClassW(ctypes.byref(windowClass)):
            raise ctypes.WinError(ctypes.get_last_error())
        self.hwnd = _user32.CreateWindowExW(0, className, className, 0, 0, 0, 0, 0, _HWND_MESSAGE, None, instance, None)
        if not self.hwnd:
            raise ctypes.WinError(ctypes.get_last_error())
        _user32.ChangeWindowMessageFilterEx(self.hwnd, _WM_COPYDATA, _MSGFLT_ALLOW, None)

    def _handleMessage(self, hwnd, message, wParam, lParam):
        if message == _WM_COPYDATA:
            data = ctypes.cast(lParam, ctypes.POINTER(_COPYDATASTRUCT)).contents
            self.replies[data.dwData] = ctypes.string_at(data.lpData, data.cbData) if data.cbData else b""
            return 1
        return _user32.DefWindowProcW(hwnd, message, wParam, lParam)

    def pump(self, timeout):
        message = wintypes.MSG()
        _user32.MsgWaitForMultipleObjects(0, None, False, max(0, int(timeout * 1000)), _QS_ALLINPUT)
        while _user32.PeekMessageW(ctypes.byref(message), None, 0, 0, _PM_REMOVE):
            _user32.TranslateMessage(ctypes.byref(message))
            _user32.DispatchMessageW(ctypes.byref(message))


_threadData = threading.local()
_allReceivers = []  # Never freed: a window procedure must outlive its window, even if a thread forgets to release it


def _receiver():
    if not hasattr(_threadData, "receiver"):
        _threadData.receiver = _CopyDataReceiver()
        _allReceivers.append(_threadData.receiver)
    return _threadData.receiver


def _releaseThreadReceiver():
    # Windows destroys a thread's windows when it exits, so do it ourselves while the callback is still safe to run
    receiver = getattr(_threadData, "receiver", None)
    if receiver is not None:
        del _threadData.receiver
        _user32.DestroyWindow(receiver.hwnd)


class PotPlayerApi(object):
    """One PotPlayer window, driven through the remote-control messages of the PotPlayer SDK."""

    POT_GET_TOTAL_TIME = 0x5002
    POT_GET_CURRENT_TIME = 0x5004
    POT_SET_CURRENT_TIME = 0x5005
    POT_GET_PLAY_STATUS = 0x5006
    POT_SET_PLAY_STATUS = 0x5007
    POT_GET_SPEED = 0x5015
    POT_SET_SPEED = 0x5016
    POT_GET_PLAYFILE_NAME = 0x6020
    POT_SET_SHOW_MESSAGE = 0x6040

    STATUS_STOPPED = -1
    STATUS_ENDED = 0  # Not in the SDK header: reported once playback reaches the end of the file
    STATUS_PAUSED = 1
    STATUS_PLAYING = 2

    WINDOW_CLASSES = ("PotPlayer64", "PotPlayer")
    TITLE_SUFFIX = " - PotPlayer"

    class NotRespondingError(Exception):
        pass

    def __init__(self, hwnd, process=None, newInstance=True):
        self.hwnd = hwnd
        self.pid = _windowPid(hwnd)
        self.process = process
        self.newInstance = newInstance

    @staticmethod
    def findWindows(pid=None):
        found = []

        def callback(hwnd, _):
            if _windowClass(hwnd) in PotPlayerApi.WINDOW_CLASSES and (pid is None or _windowPid(hwnd) == pid):
                found.append(hwnd)
            return True

        _user32.EnumWindows(_WNDENUMPROC(callback), 0)
        return found

    @staticmethod
    def launch(exePath, args, filePath, newInstance):
        """Start PotPlayer and bind to the window of the process we started.
        Without `/new` the instance also accepts files handed over with `/current`."""
        command = [exePath] + list(args) + ([filePath] if filePath else []) + (["/new"] if newInstance else [])
        process = subprocess.Popen(command)
        deadline = time.time() + constants.POTPLAYER_OPEN_MAX_WAIT_TIME
        while time.time() < deadline:
            windows = PotPlayerApi.findWindows(process.pid)
            if windows:
                api = PotPlayerApi(windows[0], process, newInstance)
                while time.time() < deadline:
                    try:
                        api.getStatus()
                        return api
                    except PotPlayerApi.NotRespondingError:
                        time.sleep(0.05)
                break
            if process.poll() is not None:
                break
            time.sleep(0.05)
        raise PotPlayerApi.NotRespondingError()

    def isAlive(self):
        return bool(_user32.IsWindow(self.hwnd))

    def _send(self, message, wParam, lParam):
        result = _LRESULT()
        sent = _user32.SendMessageTimeoutW(
            self.hwnd, message, wParam, lParam, _SMTO_ABORTIFHUNG, constants.POTPLAYER_COMMAND_TIMEOUT, ctypes.byref(result))
        if not sent:
            raise PotPlayerApi.NotRespondingError()
        return result.value

    def command(self, code, value=0):
        return self._send(_WM_USER, code, value)

    def _sendString(self, code, text):
        data = ctypes.create_string_buffer(text.encode("utf-8"))
        copyData = _COPYDATASTRUCT(code, ctypes.sizeof(data), ctypes.cast(data, ctypes.c_void_p))
        self._send(_WM_COPYDATA, _receiver().hwnd, ctypes.addressof(copyData))

    def _getString(self, code):
        receiver = _receiver()
        receiver.replies.pop(code, None)
        self.command(code, receiver.hwnd)
        deadline = time.time() + constants.POTPLAYER_COMMAND_TIMEOUT / 1000.0
        while code not in receiver.replies:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise PotPlayerApi.NotRespondingError()
            receiver.pump(min(remaining, 0.02))
        return receiver.replies.pop(code).rstrip(b"\0").decode("utf-8", "replace")

    def getStatus(self):
        return self.command(self.POT_GET_PLAY_STATUS)

    def getPositionMs(self):
        return self.command(self.POT_GET_CURRENT_TIME)

    def getDurationMs(self):
        return self.command(self.POT_GET_TOTAL_TIME)

    def getSpeed(self):
        return self.command(self.POT_GET_SPEED)

    def getFilePath(self):
        return self._getString(self.POT_GET_PLAYFILE_NAME)

    def getTitle(self):
        title = _windowText(self.hwnd).rstrip()
        if title.endswith(self.TITLE_SUFFIX):
            return title[:-len(self.TITLE_SUFFIX)].rstrip()
        return "" if title == self.TITLE_SUFFIX.strip(" -") else title

    def play(self):
        self.command(self.POT_SET_PLAY_STATUS, self.STATUS_PLAYING)

    def pause(self):
        self.command(self.POT_SET_PLAY_STATUS, self.STATUS_PAUSED)

    def seekMs(self, position):
        self.command(self.POT_SET_CURRENT_TIME, int(position))

    def setSpeed(self, rate):
        self.command(self.POT_SET_SPEED, int(round(rate * 1000)))

    def showMessage(self, text):
        self._sendString(self.POT_SET_SHOW_MESSAGE, text)

    def close(self):
        _user32.PostMessageW(self.hwnd, _WM_CLOSE, 0, 0)


class PotPlayer(BasePlayer):
    speedSupported = True
    alertOSDSupported = False
    customOpenDialog = False
    chatOSDSupported = False
    osdMessageSeparator = "; "

    def __init__(self, client, playerPath, args):
        from twisted.internet import reactor
        self.reactor = reactor
        self._client = client
        self._playerPath = playerPath
        self._args = list(args)
        self._api = None
        self._lock = threading.RLock()
        self._openLock = threading.Lock()
        self._stopped = threading.Event()
        self._snapsToKeyframes = False  # PotPlayer's "Use keyframe to jump to a time" seems to be on
        self._commandSerial = 0  # bumped by every command we send, so polls started before it are dropped
        self._desiredPaused = None
        self._resetFileState()

    @staticmethod
    def run(client, playerPath, filePath, args):
        player = PotPlayer(client, PotPlayer.getExpandedPath(playerPath), args)
        player._start(filePath)
        return player

    def _start(self, filePath):
        # Like MPC, block until the player is up so the client never syncs against a missing player.
        # Only skip `/new` when no other PotPlayer is open, so we never hijack the user's own player.
        newInstance = bool(PotPlayerApi.findWindows())
        try:
            api = PotPlayerApi.launch(self._playerPath, self._args, filePath, newInstance)
        except (PotPlayerApi.NotRespondingError, OSError):
            self._client.ui.showErrorMessage(getMessage("potplayer-launch-error"), True)
            self._client.stop(True)
            return
        with self._lock:
            self._api = api
        self._debug("PotPlayer started (pid {}, {})".format(api.pid, "/new" if newInstance else "accepts /current"))
        self._client.initPlayer(self)
        threading.Thread(target=self._pollLoop, name="PotPlayer", daemon=True).start()

    def _debug(self, message):
        self.reactor.callFromThread(self._client.ui.showDebugMessage, message)

    # --- state ------------------------------------------------------------------------------------

    def _resetFileState(self):
        self._fileLoaded = False
        self._title = None
        self._status = PotPlayerApi.STATUS_STOPPED
        self._rawPosition = None
        self._anchorPosition = 0.0
        self._anchorTime = time.perf_counter()
        self._speed = 1000
        self._duration = 0
        self._seekTarget = None
        self._eofReported = False
        self._loadingSince = None  # a new file was detected but PotPlayer is still starting it
        self._loadingPosition = None
        self._enforcePausedUntil = 0.0

    def _predictPosition(self, now):
        # PotPlayer only refreshes the reported time every ~500 ms, but each refresh is exact,
        # so we anchor on refreshes and interpolate in between.
        position = self._anchorPosition
        if self._status == PotPlayerApi.STATUS_PLAYING:
            position += (now - self._anchorTime) * self._speed
        if self._duration:
            position = min(position, self._duration)
        return max(position, 0.0)

    def _setAnchor(self, position, now):
        self._anchorPosition, self._anchorTime = float(position), now

    # --- polling ----------------------------------------------------------------------------------

    def _pollLoop(self):
        try:
            self._pollUntilStopped()
        finally:
            _releaseThreadReceiver()

    def _pollUntilStopped(self):
        iteration = 0
        while not self._stopped.is_set():
            api = self._api
            try:
                self._poll(api, fullRead=iteration % constants.POTPLAYER_FULL_POLL_EVERY == 0)
            except PotPlayerApi.NotRespondingError:
                if not api.isAlive() and api is self._api and not self._stopped.is_set():
                    self._stopped.set()
                    self.reactor.callFromThread(self._client.stop, False)
                    return
            except Exception as e:
                self._debug("PotPlayer polling error: {}".format(e))
                time.sleep(0.5)
            iteration += 1
            time.sleep(constants.POTPLAYER_POLL_INTERVAL)

    def _poll(self, api, fullRead):
        serial = self._commandSerial
        status = api.getStatus()
        rawPosition = api.getPositionMs()
        if fullRead or status != self._status:
            duration, speed, title = api.getDurationMs(), api.getSpeed(), api.getTitle()
        else:
            duration, speed, title = self._duration, self._speed, self._title
        now = time.perf_counter()
        newFile = False
        enforcePaused = None
        with self._lock:
            if api is not self._api or serial != self._commandSerial:
                return
            if duration <= 0 or status == PotPlayerApi.STATUS_STOPPED or not title:
                if self._title is not None:
                    self._resetFileState()
                return
            if title != self._title:
                self._resetFileState()
                self._title, self._status, self._speed, self._duration = title, status, speed, duration
                self._rawPosition = rawPosition
                self._setAnchor(rawPosition, now)
                self._loadingSince, self._loadingPosition = now, rawPosition
            else:
                self._duration = duration
                self._updateClock(status, rawPosition, speed, now)
                if self._loadingSince is not None:
                    if self._hasStartedPlayback(status, rawPosition, now):
                        self._loadingSince = None
                        newFile = True
                elif (
                    now < self._enforcePausedUntil and self._desiredPaused is not None
                    and status in (PotPlayerApi.STATUS_PAUSED, PotPlayerApi.STATUS_PLAYING)
                    and (status == PotPlayerApi.STATUS_PAUSED) != self._desiredPaused
                ):
                    enforcePaused = self._desiredPaused
        if newFile:
            self._onNewFile(api)
        elif enforcePaused is not None:
            self._debug("PotPlayer changed play state while loading, setting paused={} again".format(enforcePaused))
            self.setPaused(enforcePaused)

    def _hasStartedPlayback(self, status, rawPosition, now):
        # PotPlayer ignores commands (and may resume an old position) until playback has really started
        waited = now - self._loadingSince
        if waited > constants.POTPLAYER_NEWFILE_SETTLE_TIMEOUT:
            return True
        if status == PotPlayerApi.STATUS_PLAYING:
            return rawPosition != self._loadingPosition
        return status == PotPlayerApi.STATUS_PAUSED and waited > 0.5

    def _updateClock(self, status, rawPosition, speed, now):
        predicted = self._predictPosition(now)
        if status == PotPlayerApi.STATUS_ENDED:
            # PotPlayer jumps back to 0 shortly after the end; keep reporting the end instead
            self._status, self._rawPosition = status, rawPosition
            self._setAnchor(self._duration, now)
            if not self._eofReported:
                self._eofReported = True
                self.reactor.callFromThread(self._client.eofReportedByPlayer)
            return
        if self._status == PotPlayerApi.STATUS_ENDED:
            self._eofReported = False
            predicted = rawPosition
        if status != self._status or speed != self._speed:
            self._setAnchor(predicted, now)
            self._status, self._speed = status, speed
        if rawPosition != self._rawPosition:
            self._rawPosition = rawPosition
            if not self._isRefreshFromBeforeSeek(rawPosition, now):
                self._checkSeekLanding(rawPosition)
                self._setAnchor(rawPosition, now)

    def _isRefreshFromBeforeSeek(self, rawPosition, now):
        # A periodic refresh racing our seek still carries the old timeline; don't take it as a user seek
        if self._seekTarget is None:
            return False
        target, before, seekTime, wasPlaying = self._seekTarget
        elapsed = now - seekTime
        if elapsed > constants.POTPLAYER_SEEK_SETTLE_TIME:
            self._seekTarget = None
            return False
        oldTimeline = before + (elapsed * self._speed if wasPlaying else 0)
        margin = constants.POTPLAYER_SEEK_LANDING_MARGIN
        return abs(rawPosition - oldTimeline) < margin and abs(rawPosition - target) > margin

    def _checkSeekLanding(self, rawPosition):
        if self._seekTarget is None:
            return
        target = self._seekTarget[0]
        self._seekTarget = None
        # Not a stale refresh, so this is where the seek landed: far from the target means a keyframe
        if (
            abs(rawPosition - target) > constants.POTPLAYER_SEEK_LANDING_MARGIN and not self._snapsToKeyframes
            and target < self._duration - 2000
        ):
            self._snapsToKeyframes = True
            self.reactor.callFromThread(self._client.ui.showErrorMessage, getMessage("potplayer-keyframe-seek-warning"))

    def _onNewFile(self, api):
        try:
            path = api.getFilePath()
        except PotPlayerApi.NotRespondingError:
            with self._lock:
                self._title = None  # retry on the next poll
            return
        with self._lock:
            duration = self._duration / 1000.0
        filename = path if utils.isURL(path) else os.path.basename(path)
        self._debug("PotPlayer loaded {} ({:.3f}s)".format(path, duration))
        self.reactor.callFromThread(self._client.updateFile, filename, duration, path)
        self.setPaused(self._client.getGlobalPaused())
        self.setPosition(self._client.getGlobalPosition())
        with self._lock:
            self._fileLoaded = True
            self._enforcePausedUntil = time.perf_counter() + constants.POTPLAYER_NEWFILE_ENFORCE_TIME

    # --- BasePlayer -------------------------------------------------------------------------------

    def askForStatus(self):
        with self._lock:
            loaded = self._fileLoaded
            paused = self._status != PotPlayerApi.STATUS_PLAYING
            position = self._predictPosition(time.perf_counter()) / 1000.0
        if loaded:
            self._client.updatePlayerStatus(paused, position)
        else:
            self._client.updatePlayerStatus(self._client.getGlobalPaused(), self._client.getGlobalPosition())

    def setPaused(self, value):
        with self._lock:
            api = self._api
            if api is None:
                return
            self._commandSerial += 1
            self._desiredPaused = value
            now = time.perf_counter()
            self._setAnchor(self._predictPosition(now), now)
            if self._status != PotPlayerApi.STATUS_ENDED:
                self._status = PotPlayerApi.STATUS_PAUSED if value else PotPlayerApi.STATUS_PLAYING
        self._sendCommand(api.pause if value else api.play)

    def setPosition(self, value):
        target = max(0.0, value * 1000.0)
        with self._lock:
            api = self._api
            if api is None:
                return
            self._commandSerial += 1
            now = time.perf_counter()
            before = self._predictPosition(now)
            if self._snapsToKeyframes and abs(target - before) < constants.SEEK_THRESHOLD * 1000:
                # A small correction would land on an earlier keyframe and look like a new seek to everyone
                return
            self._seekTarget = (target, before, now, self._status == PotPlayerApi.STATUS_PLAYING)
            self._setAnchor(target, now)
        self._sendCommand(lambda: api.seekMs(target))

    def setSpeed(self, value):
        with self._lock:
            api = self._api
            if api is None:
                return
            self._commandSerial += 1
            now = time.perf_counter()
            self._setAnchor(self._predictPosition(now), now)
            self._speed = int(round(value * 1000))
        self._sendCommand(lambda: api.setSpeed(value))

    def _sendCommand(self, action):
        try:
            action()
        except PotPlayerApi.NotRespondingError:
            pass
        with self._lock:
            # also drop polls that read PotPlayer while the command was still on its way
            self._commandSerial += 1

    def displayMessage(
        self, message,
        duration=(constants.OSD_DURATION * 1000), OSDType=constants.OSD_NOTIFICATION, mood=constants.MESSAGE_NEUTRAL
    ):
        api = self._api
        if api is None:
            return
        try:
            api.showMessage(message)
        except PotPlayerApi.NotRespondingError:
            pass

    def setFeatures(self, featureList):
        pass

    def drop(self):
        self._stopped.set()
        with self._lock:
            api = self._api
        if api is not None:
            api.close()

    def openFile(self, filePath, resetPosition=False):
        if not utils.isURL(filePath):
            normedPath = os.path.normpath(filePath)
            if os.path.isfile(normedPath):
                filePath = normedPath
        threading.Thread(target=self._openFile, args=(filePath,), name="PotPlayer open file", daemon=True).start()

    def _openFile(self, filePath):
        try:
            with self._openLock:
                api = self._api
                if api is None or self._stopped.is_set():
                    return
                if self._isPlayingPath(api, filePath):
                    return  # already open; the client rewinds it itself
                if not self._openInCurrentInstance(api, filePath):
                    self._openInNewInstance(filePath)
        finally:
            _releaseThreadReceiver()

    def _isPlayingPath(self, api, filePath):
        try:
            # An empty PotPlayer still reports the last file it played, so check something is open first
            if api.getDurationMs() <= 0 or not api.getTitle():
                return False
            currentPath = api.getFilePath()
        except PotPlayerApi.NotRespondingError:
            return False
        if utils.isURL(filePath):
            return currentPath == filePath
        return os.path.normcase(os.path.normpath(currentPath)) == os.path.normcase(filePath)

    def _openInCurrentInstance(self, api, filePath):
        """Hand the file to our own window with `/current`. Only safe when ours is the only PotPlayer
        window and was not started with `/new` (such instances never accept `/current`)."""
        if api.newInstance or PotPlayerApi.findWindows() != [api.hwnd]:
            return False
        previousTitle = api.getTitle()
        helper = subprocess.Popen([self._playerPath, filePath, "/current"])
        deadline = time.time() + constants.POTPLAYER_OPEN_FILE_TIMEOUT
        while time.time() < deadline:
            if api.getTitle() not in (previousTitle, ""):
                self._debug("PotPlayer opened {} in the same window".format(filePath))
                return True
            time.sleep(0.05)
        if helper.poll() is None:
            helper.kill()
        self._debug("PotPlayer did not take {} with /current, starting a new window".format(filePath))
        return False

    def _openInNewInstance(self, filePath):
        try:
            newApi = PotPlayerApi.launch(self._playerPath, self._args, filePath, newInstance=True)
        except (PotPlayerApi.NotRespondingError, OSError):
            self.reactor.callFromThread(
                self._client.ui.showErrorMessage, getMessage("potplayer-file-open-error").format(filePath))
            return
        with self._lock:
            oldApi, self._api = self._api, newApi
            self._resetFileState()
        self._debug("PotPlayer switched to a new window (pid {}) for {}".format(newApi.pid, filePath))
        oldApi.close()

    @staticmethod
    def getDefaultPlayerPathsList():
        return constants.POTPLAYER_PATHS

    @staticmethod
    def getIconPath(path):
        return constants.POTPLAYER_ICONPATH

    @staticmethod
    def isValidPlayerPath(path):
        if PotPlayer.getExpandedPath(path):
            return True
        return False

    @staticmethod
    def getExpandedPath(path):
        if os.path.isfile(path) and os.path.basename(path).lower() in constants.POTPLAYER_EXECUTABLES:
            return path
        for executable in constants.POTPLAYER_EXECUTABLES:
            candidate = os.path.join(path, executable)
            if os.path.isfile(candidate):
                return candidate

    @staticmethod
    def getPlayerPathErrors(playerPath, filePath):
        return None
