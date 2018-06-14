# -*- coding: utf-8 -*-
# Copyright (c) 2001-2017
# Allen Short
# Andy Gayton
# Andrew Bennetts
# Antoine Pitrou
# Apple Computer, Inc.
# Ashwini Oruganti
# bakbuk
# Benjamin Bruheim
# Bob Ippolito
# Burak Nehbit
# Canonical Limited
# Christopher Armstrong
# Christopher R. Wood
# David Reid
# Donovan Preston
# Elvis Stansvik
# Eric Mangold
# Eyal Lotem
# Glenn Tarbox
# Google Inc.
# Hybrid Logic Ltd.
# Hynek Schlawack
# Itamar Turner-Trauring
# James Knight
# Jason A. Mobarak
# Jean-Paul Calderone
# Jessica McKellar
# Jonathan Jacobs
# Jonathan Lange
# Jonathan D. Simms
# Jürgen Hermann
# Julian Berman
# Kevin Horn
# Kevin Turner
# Kyle Altendorf
# Laurens Van Houtven
# Mary Gardiner
# Matthew Lefkowitz
# Massachusetts Institute of Technology
# Moshe Zadka
# Paul Swartz
# Pavel Pergamenshchik
# Ralph Meijer
# Richard Wall
# Sean Riley
# Software Freedom Conservancy
# Tarashish Mishra
# Travis B. Hartwell
# Thijs Triemstra
# Thomas Herve
# Timothy Allen
# Tom Prince

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
This module provides support for Twisted to be driven by the Qt mainloop.

In order to use this support, simply do the following::
    |  app = QApplication(sys.argv) # your code to init Qt
    |  import qt5reactor
    |  qt5reactor.install()

Then use twisted.internet APIs as usual.  The other methods here are not
intended to be called directly.

If you don't instantiate a QApplication or QCoreApplication prior to
installing the reactor, a QCoreApplication will be constructed
by the reactor.  QCoreApplication does not require a GUI so trial testing
can occur normally.

Twisted can be initialized after QApplication.exec_() with a call to
reactor.runReturn().  calling reactor.stop() will unhook twisted but
leave your Qt application running

Qt5 Port: U{Burak Nehbit<mailto:burak@nehbit.net>}

Current maintainer: U{Christopher R. Wood<mailto:chris@leastauthority.com>}

Previous maintainer: U{Tarashish Mishra<mailto:sunu@sunu.in>}
Previous maintainer: U{Glenn H Tarbox, PhD<mailto:glenn@tarbox.org>}
Previous maintainer: U{Itamar Shtull-Trauring<mailto:twisted@itamarst.org>}
Original port to QT4: U{Gabe Rudy<mailto:rudy@goldenhelix.com>}
Subsequent port by therve
"""

import sys

from syncplay.vendor.Qt.QtCore import (
     QCoreApplication, QEventLoop, QObject, QSocketNotifier, QTimer, Signal)
from twisted.internet import posixbase
from twisted.internet.interfaces import IReactorFDSet
from twisted.python import log, runtime
from zope.interface import implementer


class TwistedSocketNotifier(QObject):
    """Connection between an fd event and reader/writer callbacks."""

    activated = Signal(int)

    def __init__(self, parent, reactor, watcher, socketType):
        QObject.__init__(self, parent)
        self.reactor = reactor
        self.watcher = watcher
        fd = self.watcher.fileno()
        self.notifier = QSocketNotifier(fd, socketType, parent)
        self.notifier.setEnabled(True)
        if socketType == QSocketNotifier.Read:
            self.fn = self.read
        else:
            self.fn = self.write
        self.notifier.activated.connect(self.fn)

    def shutdown(self):
        self.notifier.setEnabled(False)
        self.notifier.activated.disconnect(self.fn)
        self.fn = self.watcher = None
        self.notifier.deleteLater()
        self.deleteLater()

    def read(self, fd):
        if not self.watcher:
            return
        w = self.watcher
        # doRead can cause self.shutdown to be called so keep
        # a reference to self.watcher

        def _read():
            # Don't call me again, until the data has been read
            self.notifier.setEnabled(False)
            why = None
            try:
                why = w.doRead()
                inRead = True
            except:
                inRead = False
                log.err()
                why = sys.exc_info()[1]
            if why:
                self.reactor._disconnectSelectable(w, why, inRead)
            elif self.watcher:
                self.notifier.setEnabled(True)
                # Re enable notification following sucessfull read
            self.reactor._iterate(fromqt=True)

        log.callWithLogger(w, _read)

    def write(self, sock):
        if not self.watcher:
            return
        w = self.watcher

        def _write():
            why = None
            self.notifier.setEnabled(False)
            try:
                why = w.doWrite()
            except:
                log.err()
                why = sys.exc_info()[1]
            if why:
                self.reactor._disconnectSelectable(w, why, False)
            elif self.watcher:
                self.notifier.setEnabled(True)
            self.reactor._iterate(fromqt=True)

        log.callWithLogger(w, _write)


@implementer(IReactorFDSet)
class QtReactor(posixbase.PosixReactorBase):
    # implements(IReactorFDSet)

    def __init__(self):
        self._reads = {}
        self._writes = {}
        self._notifiers = {}
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.iterate_qt)
        if QCoreApplication.instance() is None:
            # Application Object has not been started yet
            self.qApp = QCoreApplication([])
            self._ownApp = True
        else:
            self.qApp = QCoreApplication.instance()
            self._ownApp = False
        self._blockApp = None
        posixbase.PosixReactorBase.__init__(self)

    def _add(self, xer, primary, type):
        """
        Private method for adding a descriptor from the event loop.

        It takes care of adding it if  new or modifying it if already added
        for another state (read -> read/write for example).
        """
        if xer not in primary:
            primary[xer] = TwistedSocketNotifier(None, self, xer, type)

    def addReader(self, reader):
        """Add a FileDescriptor for notification of data available to read."""
        self._add(reader, self._reads, QSocketNotifier.Read)

    def addWriter(self, writer):
        """Add a FileDescriptor for notification of data available to write."""
        self._add(writer, self._writes, QSocketNotifier.Write)

    def _remove(self, xer, primary):
        """
        Private method for removing a descriptor from the event loop.

        It does the inverse job of _add, and also add a check in case of the fd
        has gone away.
        """
        if xer in primary:
            notifier = primary.pop(xer)
            notifier.shutdown()

    def removeReader(self, reader):
        """Remove a Selectable for notification of data available to read."""
        self._remove(reader, self._reads)

    def removeWriter(self, writer):
        """Remove a Selectable for notification of data available to write."""
        self._remove(writer, self._writes)

    def removeAll(self):
        """Remove all selectables, and return a list of them."""
        return self._removeAll(self._reads, self._writes)

    def getReaders(self):
        return list(self._reads.keys())

    def getWriters(self):
        return list(self._writes.keys())

    def callLater(self, howlong, *args, **kargs):
        rval = super(QtReactor, self).callLater(howlong, *args, **kargs)
        self.reactorInvocation()
        return rval

    def reactorInvocation(self):
        self._timer.stop()
        self._timer.setInterval(0)
        self._timer.start()

    def _iterate(self, delay=None, fromqt=False):
        """See twisted.internet.interfaces.IReactorCore.iterate."""
        self.runUntilCurrent()
        self.doIteration(delay, fromqt=fromqt)

    iterate = _iterate

    def iterate_qt(self, delay=None):
        self.iterate(delay=delay, fromqt=True)

    def doIteration(self, delay=None, fromqt=False):
        """This method is called by a Qt timer or by network activity on a file descriptor"""
        if not self.running and self._blockApp:
            self._blockApp.quit()
        self._timer.stop()
        if delay is None:
            delay = 0
        delay = max(delay, 1)
        if not fromqt:
            self.qApp.processEvents(QEventLoop.AllEvents, delay * 1000)
        t = self.timeout()
        if t is None:
            timeout = 0.01
        else:
            timeout = min(t, 0.01)
        self._timer.setInterval(timeout * 1000)
        self._timer.start()

    def runReturn(self, installSignalHandlers=True):
        self.startRunning(installSignalHandlers=installSignalHandlers)
        self.reactorInvocation()

    def run(self, installSignalHandlers=True):
        if self._ownApp:
            self._blockApp = self.qApp
        else:
            self._blockApp = QEventLoop()
        self.runReturn()
        self._blockApp.exec_()
        if self.running:
            self.stop()
            self.runUntilCurrent()

    # def sigInt(self, *args):
    #     print('I received a sigint. BAIBAI')
    #     posixbase.PosixReactorBase.sigInt()
    #
    # def sigTerm(self, *args):
    #     print('I received a sigterm. BAIBAI')
    #     posixbase.PosixReactorBase.sigTerm()
    #
    # def sigBreak(self, *args):
    #     print('I received a sigbreak. BAIBAI')
    #     posixbase.PosixReactorBase.sigBreak()


class QtEventReactor(QtReactor):
    def __init__(self, *args, **kwargs):
        self._events = {}
        super(QtEventReactor, self).__init__()

    def addEvent(self, event, fd, action):
        """Add a new win32 event to the event loop."""
        self._events[event] = (fd, action)

    def removeEvent(self, event):
        """Remove an event."""
        if event in self._events:
            del self._events[event]

    def doEvents(self):
        handles = list(self._events.keys())
        if len(handles) > 0:
            val = None
            while val != WAIT_TIMEOUT:
                val = MsgWaitForMultipleObjects(handles, 0, 0, QS_ALLINPUT | QS_ALLEVENTS)
                if val >= WAIT_OBJECT_0 and val < WAIT_OBJECT_0 + len(handles):
                    event_id = handles[val - WAIT_OBJECT_0]
                    if event_id in self._events:
                        fd, action = self._events[event_id]
                        log.callWithLogger(fd, self._runAction, action, fd)
                elif val == WAIT_TIMEOUT:
                    pass
                else:
                    #print 'Got an unexpected return of %r' % val
                    return

    def _runAction(self, action, fd):
        try:
            closed = getattr(fd, action)()
        except:
            closed = sys.exc_info()[1]
            log.deferr()
        if closed:
            self._disconnectSelectable(fd, closed, action == 'doRead')

    def iterate(self, delay=None, fromqt=False):
        """See twisted.internet.interfaces.IReactorCore.iterate."""
        self.runUntilCurrent()
        self.doEvents()
        self.doIteration(delay, fromqt=fromqt)


def posixinstall():
    """Install the Qt reactor."""
    from twisted.internet.main import installReactor
    p = QtReactor()
    installReactor(p)


def win32install():
    """Install the Qt reactor."""
    from twisted.internet.main import installReactor
    p = QtEventReactor()
    installReactor(p)


if runtime.platform.getType() == 'win32':
    from win32event import CreateEvent, MsgWaitForMultipleObjects
    from win32event import WAIT_OBJECT_0, WAIT_TIMEOUT, QS_ALLINPUT, QS_ALLEVENTS
    install = win32install
else:
    install = posixinstall


__all__ = ["install"]
