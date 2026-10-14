# coding:utf8

"""
Client-side filesystem-watch helper for media directory monitoring.

FileMonitor is deliberately playlist-blind: it knows about paths and native
filesystem watch characteristics only. It maintains the most useful native
watchdog watches within a budget and reports structured filesystem events back
to its owner (FileSwitchManager) on the Twisted reactor thread. It never touches
mediaFilesCache, playlist state, episode parsing or file-switching decisions.

watchdog is an optional dependency: if it is unavailable, or a watch cannot be
established, FileMonitor simply provides no events and Syncplay falls back to its
own reconciliation scanning.
"""

import os
import sys
from collections import namedtuple

from twisted.internet import reactor

from syncplay import constants

try:
    from watchdog.observers import Observer as _Observer
    from watchdog.events import FileSystemEventHandler as _FileSystemEventHandler
    watchdogAvailable = True
except ImportError:
    watchdogAvailable = False
    _FileSystemEventHandler = object

# Simple immutable value handed to the owner's callback. It carries filesystem
# facts only - never playlist or file-matching information.
FileMonitorEvent = namedtuple("FileMonitorEvent", ["root", "eventType", "sourcePath", "destinationPath", "isDirectory"])


def isWindowsNetworkPath(path):
    # A Windows UNC path, or a mapped drive the OS reports as remote. Everywhere
    # else this is False and a single recursive native watch is trusted at depth.
    if not path or sys.platform != "win32":
        return False
    if path.startswith("\\\\") or path.startswith("//"):
        return True
    try:
        import ctypes
        drive = os.path.splitdrive(os.path.abspath(path))[0]
        if not drive:
            return False
        DRIVE_REMOTE = 4
        return ctypes.windll.kernel32.GetDriveTypeW(drive + "\\") == DRIVE_REMOTE
    except Exception:
        return False


def _normPath(path):
    return os.path.normcase(os.path.normpath(path))


def _pathIsWithin(path, root):
    # Component-aware containment so that, for example, "P:\\TV2" is not treated
    # as being inside "P:\\TV".
    normedPath = _normPath(path)
    normedRoot = _normPath(root)
    if normedPath == normedRoot:
        return True
    return normedPath.startswith(normedRoot + os.sep)


if watchdogAvailable:
    class _WatchdogAdapter(_FileSystemEventHandler):
        def __init__(self, monitor):
            _FileSystemEventHandler.__init__(self)
            self._monitor = monitor

        def on_any_event(self, event):
            self._monitor._onWatchdogEvent(event)


class FileMonitor(object):
    def __init__(self, eventCallback, debugCallback=None):
        self._eventCallback = eventCallback
        self._debugCallback = debugCallback
        self._observer = None
        self._adapter = None
        self._mediaDirectories = []
        self._rootWatches = {}      # normed root -> (watch, path, isNetwork)
        self._priorityWatches = {}  # normed dir  -> (watch, path)

    def isAvailable(self):
        return watchdogAvailable

    def _debug(self, message):
        if self._debugCallback:
            try:
                self._debugCallback(message)
            except Exception:
                pass

    def _ensureObserver(self):
        if self._observer is None:
            observer = _Observer()
            self._adapter = _WatchdogAdapter(self)
            observer.start()
            self._observer = observer
        return self._observer

    # -- public API -------------------------------------------------------

    def setMediaDirectories(self, mediaDirectories):
        if not watchdogAvailable:
            return
        newRoots = [directory for directory in (mediaDirectories or []) if directory]
        self._mediaDirectories = list(newRoots)
        newNormedRoots = set(_normPath(root) for root in newRoots)

        for normedRoot in list(self._rootWatches.keys()):
            if normedRoot not in newNormedRoots:
                self._removeRootWatch(normedRoot)

        for normedDir in list(self._priorityWatches.keys()):
            watchedPath = self._priorityWatches[normedDir][1]
            if not any(_pathIsWithin(watchedPath, root) for root in newRoots):
                self._removePriorityWatch(normedDir)

        for root in newRoots:
            normedRoot = _normPath(root)
            if normedRoot in self._rootWatches:
                continue
            isNetwork = isWindowsNetworkPath(root)
            if isNetwork and self._networkWatchCount() >= constants.FOLDER_SEARCH_NETWORK_WATCH_LIMIT:
                self._debug("Network watch budget reached; media root not natively watched: {}".format(root))
                continue
            self._scheduleRoot(root, isNetwork)

    def setPriorityDirectories(self, directories):
        # Supplemental non-recursive watches are only useful for Windows network
        # roots; a local recursive root watch already reports changes at depth.
        if not watchdogAvailable:
            return
        wanted = []
        seen = set()
        for directory in (directories or []):
            if not directory:
                continue
            normedDir = _normPath(directory)
            if normedDir in seen or normedDir in self._rootWatches:
                continue
            if self._findNetworkRoot(directory) is None:
                continue
            seen.add(normedDir)
            wanted.append((normedDir, directory))

        wantedNormed = set(normedDir for normedDir, _ in wanted)
        for normedDir in list(self._priorityWatches.keys()):
            if normedDir not in wantedNormed:
                self._removePriorityWatch(normedDir)

        for normedDir, directory in wanted:
            if normedDir in self._priorityWatches:
                continue
            if self._networkWatchCount() >= constants.FOLDER_SEARCH_NETWORK_WATCH_LIMIT:
                self._debug("Network watch budget reached; priority directory not watched: {}".format(directory))
                break
            self._schedulePriority(directory)

    def stop(self):
        observer = self._observer
        self._observer = None
        self._adapter = None
        self._rootWatches = {}
        self._priorityWatches = {}
        if observer is not None:
            try:
                observer.unschedule_all()
                observer.stop()
                observer.join(5.0)
            except Exception:
                pass

    # -- watch bookkeeping ------------------------------------------------

    def _networkWatchCount(self):
        count = sum(1 for entry in self._rootWatches.values() if entry[2])
        count += len(self._priorityWatches)
        return count

    def _scheduleRoot(self, root, isNetwork):
        try:
            observer = self._ensureObserver()
            watch = observer.schedule(self._adapter, root, recursive=True)
            self._rootWatches[_normPath(root)] = (watch, root, isNetwork)
        except Exception as e:
            self._debug("Could not watch media root {}: {}: {}".format(root, type(e).__name__, e))

    def _schedulePriority(self, directory):
        try:
            observer = self._ensureObserver()
            watch = observer.schedule(self._adapter, directory, recursive=False)
            self._priorityWatches[_normPath(directory)] = (watch, directory)
        except Exception as e:
            self._debug("Could not watch priority directory {}: {}: {}".format(directory, type(e).__name__, e))

    def _removeRootWatch(self, normedRoot):
        entry = self._rootWatches.pop(normedRoot, None)
        if entry is not None and self._observer is not None:
            try:
                self._observer.unschedule(entry[0])
            except Exception:
                pass

    def _removePriorityWatch(self, normedDir):
        entry = self._priorityWatches.pop(normedDir, None)
        if entry is not None and self._observer is not None:
            try:
                self._observer.unschedule(entry[0])
            except Exception:
                pass

    # -- event handling ---------------------------------------------------

    def _findRoot(self, path):
        if not path:
            return None
        best = None
        bestLength = -1
        for root in self._mediaDirectories:
            if _pathIsWithin(path, root):
                length = len(_normPath(root))
                if length > bestLength:
                    best = root
                    bestLength = length
        return best

    def _findNetworkRoot(self, path):
        root = self._findRoot(path)
        if root is not None and isWindowsNetworkPath(root):
            return root
        return None

    def _onWatchdogEvent(self, event):
        # Runs on the watchdog worker thread. Copy the useful fields and hand off
        # to the reactor thread; do not touch shared Syncplay state here.
        try:
            sourcePath = getattr(event, "src_path", None)
            destinationPath = getattr(event, "dest_path", None) or None
            root = self._findRoot(sourcePath)
            if root is None and destinationPath:
                root = self._findRoot(destinationPath)
            if root is None:
                return
            payload = FileMonitorEvent(
                root,
                getattr(event, "event_type", None),
                sourcePath,
                destinationPath,
                bool(getattr(event, "is_directory", False)),
            )
        except Exception:
            return
        try:
            reactor.callFromThread(self._eventCallback, payload)
        except Exception:
            pass
