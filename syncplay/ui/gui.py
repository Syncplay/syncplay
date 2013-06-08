from PySide import QtGui #@UnresolvedImport
from PySide.QtCore import Qt #@UnresolvedImport
from syncplay import utils, constants
import sys
import time
import re

class MainDialog(QtGui.QDialog):
    def addClient(self, client):
        self._syncplayClient = client
    
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
            
    def showList(self):
        self._syncplayClient.getUserList() #TODO: remove?
        
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
            o = re.match(constants.UI_OFFSET_REGEX, newoffset)
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
        self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/")
        
    def addTopLayout(self, dialog):       
        dialog.topSplit = QtGui.QSplitter(Qt.Horizontal)

        dialog.outputLayout = QtGui.QVBoxLayout()
        dialog.outputbox = QtGui.QTextEdit()
        dialog.outputbox.setReadOnly(True)  
        dialog.outputlabel = QtGui.QLabel("Notifications")
        dialog.outputFrame = QtGui.QFrame()
        dialog.outputFrame.setLineWidth(0)
        dialog.outputFrame.setMidLineWidth(0)
        dialog.outputLayout.setContentsMargins(0,0,0,0)
        dialog.outputLayout.addWidget(dialog.outputlabel)
        dialog.outputLayout.addWidget(dialog.outputbox)
        dialog.outputFrame.setLayout(dialog.outputLayout)
        
        dialog.listLayout = QtGui.QVBoxLayout()
        dialog.listbox = QtGui.QTextEdit()
        dialog.listbox.setReadOnly(True)
        dialog.listlabel = QtGui.QLabel("List of who is playing what")
        dialog.listFrame = QtGui.QFrame()
        dialog.listFrame.setLineWidth(0)
        dialog.listFrame.setMidLineWidth(0)
        dialog.listLayout.setContentsMargins(0,0,0,0)
        dialog.listLayout.addWidget(dialog.listlabel)
        dialog.listLayout.addWidget(dialog.listbox)
        dialog.listFrame.setLayout(dialog.listLayout)
        
        dialog.topSplit.addWidget(dialog.outputFrame)
        dialog.topSplit.addWidget(dialog.listFrame)
        dialog.topSplit.setStretchFactor(0,3)
        dialog.topSplit.setStretchFactor(1,2)
        dialog.mainLayout.addWidget(dialog.topSplit)
        dialog.topSplit.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)

    def addBottomLayout(self, dialog):
        dialog.bottomLayout = QtGui.QHBoxLayout()

        dialog.addRoomBox(MainDialog)
        dialog.addSeekBox(MainDialog)
        dialog.addMiscBox(MainDialog)

        dialog.bottomLayout.addWidget(dialog.roomGroup, Qt.AlignLeft)
        dialog.bottomLayout.addWidget(dialog.seekGroup, Qt.AlignLeft)
        dialog.bottomLayout.addWidget(dialog.miscGroup, Qt.AlignLeft)

        dialog.mainLayout.addLayout(dialog.bottomLayout, Qt.AlignLeft)

    def addRoomBox(self, dialog):
        dialog.roomGroup = QtGui.QGroupBox("Room")
        
        dialog.roomInput = QtGui.QLineEdit()
        dialog.roomButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'door_in.png'), "Join room")
        dialog.roomButton.pressed.connect(self.joinRoom)
        dialog.roomLayout = QtGui.QHBoxLayout()
        dialog.roomInput.setMaximumWidth(150)
        
        dialog.roomLayout.addWidget(dialog.roomInput)
        dialog.roomLayout.addWidget(dialog.roomButton)
        
        dialog.roomGroup.setLayout(dialog.roomLayout)
        dialog.roomGroup.setFixedSize(dialog.roomGroup.sizeHint())
        
    def addSeekBox(self, dialog):
        dialog.seekGroup = QtGui.QGroupBox("Seek")
        
        dialog.seekInput = QtGui.QLineEdit()
        dialog.seekButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'clock_go.png'),"Seek to position")
        dialog.seekButton.pressed.connect(self.seekPosition)
        
        dialog.seekLayout = QtGui.QHBoxLayout()
        dialog.seekInput.setMaximumWidth(100)
        
        dialog.seekLayout.addWidget(dialog.seekInput)
        dialog.seekLayout.addWidget(dialog.seekButton)
        
        dialog.seekGroup.setLayout(dialog.seekLayout)
        dialog.seekGroup.setFixedSize(dialog.seekGroup.sizeHint())
        
    def addMiscBox(self, dialog):
        dialog.miscGroup = QtGui.QGroupBox("Other Commands")
        
        dialog.unseekButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'arrow_undo.png'),"Undo last seek")
        dialog.unseekButton.pressed.connect(self.undoSeek)
        dialog.pauseButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'control_pause_blue.png'),"Toggle pause")
        dialog.pauseButton.pressed.connect(self.togglePause)
        dialog.showListButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'table_refresh.png'),"Update list")
        dialog.showListButton.pressed.connect(self.showList)
        
        dialog.miscLayout = QtGui.QHBoxLayout()
        dialog.miscLayout.addWidget(dialog.unseekButton)
        dialog.miscLayout.addWidget(dialog.pauseButton)
        dialog.miscLayout.addWidget(dialog.showListButton)
        
        dialog.miscGroup.setLayout(dialog.miscLayout)
        dialog.miscGroup.setFixedSize(dialog.miscGroup.sizeHint())
        

    def addMenubar(self, dialog):
        dialog.menuBar = QtGui.QMenuBar()

        dialog.fileMenu = QtGui.QMenu("&File", self)
        dialog.exitAction = dialog.fileMenu.addAction(QtGui.QIcon(self.resourcespath + 'cross.png'), "E&xit")
        dialog.exitAction.triggered.connect(self.exitSyncplay)
        dialog.menuBar.addMenu(dialog.fileMenu)
        
        dialog.advancedMenu = QtGui.QMenu("&Advanced", self)
        dialog.setoffsetAction = dialog.advancedMenu.addAction(QtGui.QIcon(self.resourcespath + 'timeline_marker.png'),"Set &Offset")
        dialog.setoffsetAction.triggered.connect(self.setOffset)
        dialog.menuBar.addMenu(dialog.advancedMenu)
        
        dialog.helpMenu = QtGui.QMenu("&Help", self)
        dialog.userguideAction = dialog.helpMenu.addAction(QtGui.QIcon(self.resourcespath + 'help.png'), "Open User &Guide")
        dialog.userguideAction.triggered.connect(self.openUserGuide)
        
        dialog.menuBar.addMenu(dialog.helpMenu)
        dialog.mainLayout.setMenuBar(dialog.menuBar)
        
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
        super(MainDialog, self).__init__()
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
        self.setLayout(self.mainLayout)
        self.resize(700,500)
        self.setWindowIcon(QtGui.QIcon(self.resourcespath + "syncplay.png"))
        self.show()
