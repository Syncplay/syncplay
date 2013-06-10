from PySide import QtGui #@UnresolvedImport
from PySide.QtCore import Qt #@UnresolvedImport
from syncplay import utils, constants
import sys
import time
import re

class MainWindow(QtGui.QMainWindow):
    def addClient(self, client):
        self._syncplayClient = client
        self.roomInput.setText(self._syncplayClient.getRoom())
    
    def promptFor(self, prompt=">", message=""):
        #TODO: Prompt user
        return None

    def showMessage(self, message, noTimestamp=False):
        message = unicode(message)
        message = message.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        message = message.replace("\n", "<br />")
        if(noTimestamp):
            self.newMessage(message + "<br />")
        else:
            self.newMessage(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message + "<br />")
    
    def showListMessage(self, message):
        message = unicode(message)
        message = message.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        message = message.replace("\t", "&nbsp;"*4)
        self._listBuffer += message + "<br />"
        
    def markEndOfUserlist(self):
        self.resetList()
        self.newListItem(self._listBuffer)
        self._listBuffer = "";
    
    def userListChange(self):
        self._syncplayClient.showUserList()
    
    def showDebugMessage(self, message):
        print(message)
        
    def showErrorMessage(self, message):
        print("ERROR:\t" + message)

    def joinRoom(self):
        room = self.roomInput.text()
        if room == "":
            if  self._syncplayClient.userlist.currentUser.file:
                room = self._syncplayClient.userlist.currentUser.file["name"]
            else:
                room = self._syncplayClient.defaultRoom
        self._syncplayClient.setRoom(room)
        self._syncplayClient.sendRoom()

    def seekPosition(self):
        s = re.match(constants.UI_SEEK_REGEX, self.seekInput.text())
        if(s):
            sign = self._extractSign(s.group('sign'))
            t = utils.parseTime(s.group('time'))
            if(t is None):
                return
            if(sign):
                t = self._syncplayClient.getGlobalPosition() + sign * t 
            self._syncplayClient.setPosition(t)
            self.seekInput.setText("")
        else:
            self.showMessage("Invalid seek value", True)
        
    def undoSeek(self):
        tmp_pos = self._syncplayClient.getPlayerPosition()
        self._syncplayClient.setPosition(self._syncplayClient.playerPositionBeforeLastSeek)
        self._syncplayClient.playerPositionBeforeLastSeek = tmp_pos
        
    def togglePause(self):
        self._syncplayClient.setPaused(not self._syncplayClient.getPlayerPaused())
        
    def exitSyncplay(self):
        self._syncplayClient.stop()
            
    def closeEvent(self, event):
        self.exitSyncplay()
        event.ignore()
            
    def _extractSign(self, m):
        if(m):
            if(m == "-"):
                return -1
            else:
                return 1
        else:
            return None
        
    def setOffset(self):
        newoffset, ok = QtGui.QInputDialog.getText(self,"Set Offset",
                "Offset (+/-):", QtGui.QLineEdit.Normal,
                "")
        if ok and newoffset != '':
            o = re.match(constants.UI_OFFSET_REGEX, "o " + newoffset)
            if(o):
                sign = self._extractSign(o.group('sign'))
                t = utils.parseTime(o.group('time'))
                if(t is None):
                    return
                if (o.group('sign') == "/"):
                        t =  self._syncplayClient.getPlayerPosition() - t
                elif(sign):
                        t = self._syncplayClient.getUserOffset() + sign * t
                self._syncplayClient.setUserOffset(t)
            else:
                self.showMessage("Invalid offset value", True)
        
    def openUserGuide(self):
        if sys.platform.startswith('linux'):
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/linux/")
        elif sys.platform.startswith('win'):
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/windows/")
        else:
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/")
        
    def addTopLayout(self, window):       
        window.topSplit = QtGui.QSplitter(Qt.Horizontal)

        window.outputLayout = QtGui.QVBoxLayout()
        window.outputbox = QtGui.QTextEdit()
        window.outputbox.setReadOnly(True)  
        window.outputlabel = QtGui.QLabel("Notifications")
        window.outputFrame = QtGui.QFrame()
        window.outputFrame.setLineWidth(0)
        window.outputFrame.setMidLineWidth(0)
        window.outputLayout.setContentsMargins(0,0,0,0)
        window.outputLayout.addWidget(window.outputlabel)
        window.outputLayout.addWidget(window.outputbox)
        window.outputFrame.setLayout(window.outputLayout)
        
        window.listLayout = QtGui.QVBoxLayout()
        window.listbox = QtGui.QTextEdit()
        window.listbox.setReadOnly(True)
        window.listlabel = QtGui.QLabel("List of who is playing what")
        window.listFrame = QtGui.QFrame()
        window.listFrame.setLineWidth(0)
        window.listFrame.setMidLineWidth(0)
        window.listLayout.setContentsMargins(0,0,0,0)
        window.listLayout.addWidget(window.listlabel)
        window.listLayout.addWidget(window.listbox)
        window.listFrame.setLayout(window.listLayout)
        
        window.topSplit.addWidget(window.outputFrame)
        window.topSplit.addWidget(window.listFrame)
        window.topSplit.setStretchFactor(0,4)
        window.topSplit.setStretchFactor(1,5)
        window.mainLayout.addWidget(window.topSplit)
        window.topSplit.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)

    def addBottomLayout(self, window):
        window.bottomLayout = QtGui.QHBoxLayout()

        window.addRoomBox(MainWindow)
        window.addSeekBox(MainWindow)
        window.addMiscBox(MainWindow)

        window.bottomLayout.addWidget(window.roomGroup, Qt.AlignLeft)
        window.bottomLayout.addWidget(window.seekGroup, Qt.AlignLeft)
        window.bottomLayout.addWidget(window.miscGroup, Qt.AlignLeft)

        window.mainLayout.addLayout(window.bottomLayout, Qt.AlignLeft)

    def addRoomBox(self, window):
        window.roomGroup = QtGui.QGroupBox("Room")
        
        window.roomInput = QtGui.QLineEdit()
        window.roomInput.returnPressed.connect(self.joinRoom)
        window.roomButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'door_in.png'), "Join room")
        window.roomButton.pressed.connect(self.joinRoom)
        window.roomLayout = QtGui.QHBoxLayout()
        window.roomInput.setMaximumWidth(150)
        
        window.roomLayout.addWidget(window.roomInput)
        window.roomLayout.addWidget(window.roomButton)
        
        window.roomGroup.setLayout(window.roomLayout)
        window.roomGroup.setFixedSize(window.roomGroup.sizeHint())
        
    def addSeekBox(self, window):
        window.seekGroup = QtGui.QGroupBox("Seek")
        
        window.seekInput = QtGui.QLineEdit()
        window.seekInput.returnPressed.connect(self.seekPosition)
        window.seekButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'clock_go.png'),"Seek to position")
        window.seekButton.pressed.connect(self.seekPosition)
        
        window.seekLayout = QtGui.QHBoxLayout()
        window.seekInput.setMaximumWidth(100)
        
        window.seekLayout.addWidget(window.seekInput)
        window.seekLayout.addWidget(window.seekButton)
        
        window.seekGroup.setLayout(window.seekLayout)
        window.seekGroup.setFixedSize(window.seekGroup.sizeHint())
        
    def addMiscBox(self, window):
        window.miscGroup = QtGui.QGroupBox("Other Commands")
        
        window.unseekButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'arrow_undo.png'),"Undo last seek")
        window.unseekButton.pressed.connect(self.undoSeek)
        window.pauseButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'control_pause_blue.png'),"Toggle pause")
        window.pauseButton.pressed.connect(self.togglePause)
        
        window.miscLayout = QtGui.QHBoxLayout()
        window.miscLayout.addWidget(window.unseekButton)
        window.miscLayout.addWidget(window.pauseButton)
        
        window.miscGroup.setLayout(window.miscLayout)
        window.miscGroup.setFixedSize(window.miscGroup.sizeHint())
        

    def addMenubar(self, window):
        window.menuBar = QtGui.QMenuBar()

        window.fileMenu = QtGui.QMenu("&File", self)
        window.exitAction = window.fileMenu.addAction(QtGui.QIcon(self.resourcespath + 'cross.png'), "E&xit")
        window.exitAction.triggered.connect(self.exitSyncplay)
        window.menuBar.addMenu(window.fileMenu)
        
        window.advancedMenu = QtGui.QMenu("&Advanced", self)
        window.setoffsetAction = window.advancedMenu.addAction(QtGui.QIcon(self.resourcespath + 'timeline_marker.png'),"Set &Offset")
        window.setoffsetAction.triggered.connect(self.setOffset)
        window.menuBar.addMenu(window.advancedMenu)
        
        window.helpMenu = QtGui.QMenu("&Help", self)
        window.userguideAction = window.helpMenu.addAction(QtGui.QIcon(self.resourcespath + 'help.png'), "Open User &Guide")
        window.userguideAction.triggered.connect(self.openUserGuide)
        
        window.menuBar.addMenu(window.helpMenu)
        window.mainLayout.setMenuBar(window.menuBar)
    
    def addMainFrame(self, window):
        window.mainFrame = QtGui.QFrame()
        window.mainFrame.setLineWidth(0)
        window.mainFrame.setMidLineWidth(0)
        window.mainFrame.setContentsMargins(0,0,0,0)
        window.mainFrame.setLayout(window.mainLayout)
        
        window.setCentralWidget(window.mainFrame)
        
    def newMessage(self, message):
        self.outputbox.moveCursor(QtGui.QTextCursor.End)
        self.outputbox.insertHtml(message)
        self.outputbox.moveCursor(QtGui.QTextCursor.End)
        
    def resetList(self):
        self.listbox.setText("")
        
    def newListItem(self, item):
        self.listbox.moveCursor(QtGui.QTextCursor.End)
        self.listbox.insertHtml(item)
        self.listbox.moveCursor(QtGui.QTextCursor.End)
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.QtGui = QtGui
        self._listBuffer = ""
        if sys.platform.startswith('linux'):
            self.resourcespath = utils.findWorkingDir() + "/resources/"
        else:
            self.resourcespath = utils.findWorkingDir() + "\\resources\\"
        self.setWindowTitle("Syncplay - Main Window")
        self.mainLayout = QtGui.QVBoxLayout()
        self.addTopLayout(self)
        self.addBottomLayout(self)
        self.addMenubar(self)
        self.addMainFrame(self)
        self.resize(700,500)
        self.setWindowIcon(QtGui.QIcon(self.resourcespath + "syncplay.png"))
        self.show()
