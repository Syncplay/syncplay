from PySide import QtGui #@UnresolvedImport
from PySide.QtCore import Qt, QSettings, QSize, QPoint #@UnresolvedImport
from syncplay import utils, constants, version
import sys
import time
import re
import os 
from syncplay.utils import formatTime, sameFilename, sameFilesize, sameFileduration

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
        message = message.replace("&lt;", "<span style=\"color:#367AA9;font-weight:bold;\">&lt;")
        message = message.replace("&gt;", "&gt;</span>")
        message = message.replace("\n", "<br />")
        if(noTimestamp):
            self.newMessage(message + "<br />")
        else:
            self.newMessage(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message + "<br />")
    
    def showUserList(self, currentUser, rooms):
        self._usertreebuffer = QtGui.QStandardItemModel()
        self._usertreebuffer.setColumnCount(2)
        self._usertreebuffer.setHorizontalHeaderLabels(("Room / User","File being played"))
        usertreeRoot = self._usertreebuffer.invisibleRootItem()
        
        for room in rooms:
            roomitem = QtGui.QStandardItem(room)
            if (room == currentUser.room):
                font = QtGui.QFont()
                font.setWeight(QtGui.QFont.Bold)
                roomitem.setFont(font)
            blankitem = QtGui.QStandardItem("")
            roomitem.setFlags(roomitem.flags()  & ~Qt.ItemIsEditable) 
            blankitem.setFlags(blankitem.flags() & ~Qt.ItemIsEditable)
            usertreeRoot.appendRow((roomitem, blankitem))
            for user in rooms[room]:
                useritem = QtGui.QStandardItem(user.username)
                fileitem = QtGui.QStandardItem("")
                if (user.file):
                    fileitem = QtGui.QStandardItem(user.file['name'] + " ("+formatTime(user.file['duration'])+")")
                    if (currentUser.file):                     
                        sameName = sameFilename(user.file['name'], currentUser.file['name'])
                        sameSize = sameFilesize(user.file['size'], currentUser.file['size'])
                        sameDuration = sameFileduration(user.file['duration'], currentUser.file['duration'])
                        sameRoom = room == currentUser.room
                        differentName = not sameName
                        differentSize = not sameSize
                        differentDuration = not sameDuration
                        if (sameName or sameRoom):
                            if (differentSize and sameDuration):
                                fileitem = QtGui.QStandardItem(user.file['name'] + " ("+formatTime(user.file['duration'])+")" + " (Different size!)")
                            elif (differentSize and differentDuration):
                                fileitem = QtGui.QStandardItem(user.file['name'] + " ("+formatTime(user.file['duration'])+")" + " (Different size and duration!)")
                            elif (differentDuration):
                                fileitem = QtGui.QStandardItem(user.file['name'] + " ("+formatTime(user.file['duration'])+")" + " (Different duration!)")
                            if (sameRoom and (differentName or differentSize or differentDuration)):
                                fileitem.setForeground(QtGui.QBrush(QtGui.QColor('red')))
                else:
                    fileitem = QtGui.QStandardItem("(No file being played)")
                    if (room == currentUser.room):
                        fileitem.setForeground(QtGui.QBrush(QtGui.QColor('blue')))
                if(currentUser.username == user.username):
                    font = QtGui.QFont()
                    font.setWeight(QtGui.QFont.Bold)
                    useritem.setFont(font)
                useritem.setFlags(useritem.flags()  & ~Qt.ItemIsEditable)
                fileitem.setFlags(fileitem.flags()  & ~Qt.ItemIsEditable)
                roomitem.appendRow((useritem, fileitem))
       
        self.listTreeModel = self._usertreebuffer
        self.listTreeView.setModel(self.listTreeModel)
        self.listTreeView.setItemsExpandable(False)
        self.listTreeView.expandAll()
        self.listTreeView.resizeColumnToContents(0)
        self.listTreeView.resizeColumnToContents(1)
        
    def roomClicked(self, item):
        while(item.parent().row() != -1):
            item = item.parent()
        self.joinRoom(item.sibling(item.row(), 0).data())
    
    def userListChange(self):
        self._syncplayClient.showUserList()
    
    def showDebugMessage(self, message):
        print(message)
        
    def showErrorMessage(self, message, criticalerror = False):
        message = unicode(message)
        if criticalerror:
            QtGui.QMessageBox.critical(self,"Syncplay", message)
        message = message.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        message = message.replace("\n", "<br />")
        message = "<span style=\"color:#FF0000;\">" + message + "</span>"
        self.newMessage(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message + "<br />")

    def joinRoom(self, room = None):
        if room == None:
            room = self.roomInput.text()
        if room == "":
            if  self._syncplayClient.userlist.currentUser.file:
                room = self._syncplayClient.userlist.currentUser.file["name"]
            else:
                room = self._syncplayClient.defaultRoom
        self.roomInput.setText(room)
        if(room != self._syncplayClient.getRoom()):
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

        else:
            self.showMessage("Invalid seek value", True)
        
    def undoSeek(self):
        tmp_pos = self._syncplayClient.getPlayerPosition()
        self._syncplayClient.setPosition(self._syncplayClient.playerPositionBeforeLastSeek)
        self._syncplayClient.playerPositionBeforeLastSeek = tmp_pos
        
    def togglePause(self):
        self._syncplayClient.setPaused(not self._syncplayClient.getPlayerPaused())
        
    def play(self):
        self._syncplayClient.setPaused(False)
        
    def pause(self):
        self._syncplayClient.setPaused(True)
        
    def exitSyncplay(self):
        self._syncplayClient.stop()
            
    def closeEvent(self, event):
        self.exitSyncplay()
        self.saveSettings()
        
    def loadMediaBrowseSettings(self):
        settings = QSettings("Syncplay", "MediaBrowseDialog")
        settings.beginGroup("MediaBrowseDialog")
        self.mediadirectory = settings.value("mediadir", "")
        settings.endGroup()
                        
    def saveMediaBrowseSettings(self):
        settings = QSettings("Syncplay", "MediaBrowseDialog")
        settings.beginGroup("MediaBrowseDialog")
        settings.setValue("mediadir", self.mediadirectory)
        settings.endGroup()
        
    def browseMediapath(self):
        self.loadMediaBrowseSettings()
        options = QtGui.QFileDialog.Options()
        if (os.path.isdir(self.mediadirectory)):
            defaultdirectory = self.mediadirectory
        elif (os.path.isdir(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MoviesLocation))):
            defaultdirectory = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MoviesLocation)
        elif (os.path.isdir(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation))):
            defaultdirectory = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)
        else:
            defaultdirectory = ""
        browserfilter = "All files (*)"       
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self,"Browse for media files",defaultdirectory,
                browserfilter, "", options)
        if fileName:
            if sys.platform.startswith('win'):
                fileName = fileName.replace("/","\\")
            self.mediadirectory = os.path.dirname(fileName)
            self.saveMediaBrowseSettings()
            self._syncplayClient._player.openFile(fileName)
            
    def _extractSign(self, m):
        if(m):
            if(m == "-"):
                return -1
            else:
                return 1
        else:
            return None
        
    def setOffset(self):
        newoffset, ok = QtGui.QInputDialog.getText(self,"Set offset",
                "Offset (see http://syncplay.pl/guide/ for usage instructions):", QtGui.QLineEdit.Normal,
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
                self.showErrorMessage("Invalid offset value")
        
    def openUserGuide(self):
        if sys.platform.startswith('linux'):
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/linux/")
        elif sys.platform.startswith('win'):
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/windows/")
        else:
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/")

    def drop(self):
        self.close()
        
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
        window.listTreeModel = QtGui.QStandardItemModel()
        window.listTreeView = QtGui.QTreeView()
        window.listTreeView.setModel(window.listTreeModel)
        window.listTreeView.doubleClicked.connect(self.roomClicked)
        window.listlabel = QtGui.QLabel("List of who is playing what")
        window.listFrame = QtGui.QFrame()
        window.listFrame.setLineWidth(0)
        window.listFrame.setMidLineWidth(0)
        window.listLayout.setContentsMargins(0,0,0,0)
        window.listLayout.addWidget(window.listlabel)
        window.listLayout.addWidget(window.listTreeView)
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
        window.seekButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'clock_go.png'),"Seek to time")
        window.seekButton.pressed.connect(self.seekPosition)
        
        window.seekLayout = QtGui.QHBoxLayout()
        window.seekInput.setMaximumWidth(50)
        window.seekInput.setText("0:00")
        
        window.seekLayout.addWidget(window.seekInput)
        window.seekLayout.addWidget(window.seekButton)
        
        window.seekGroup.setLayout(window.seekLayout)
        window.seekGroup.setFixedSize(window.seekGroup.sizeHint())
        
    def addMiscBox(self, window):
        window.miscGroup = QtGui.QGroupBox("Other commands")
        
        window.unseekButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'arrow_undo.png'),"Undo seek")
        window.unseekButton.pressed.connect(self.undoSeek)

        window.miscLayout = QtGui.QHBoxLayout()
        window.miscLayout.addWidget(window.unseekButton)
        if constants.MERGE_PLAYPAUSE_BUTTONS == True:
            window.playpauseButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'control_pause_blue.png'),"Toggle pause")
            window.playpauseButton.pressed.connect(self.togglePause)
            window.miscLayout.addWidget(window.playpauseButton)
        else:
            window.playButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'control_play_blue.png'),"Play")
            window.playButton.pressed.connect(self.play)
            window.playButton.setMaximumWidth(60)
            window.miscLayout.addWidget(window.playButton)
            window.pauseButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'control_pause_blue.png'),"Pause")
            window.pauseButton.pressed.connect(self.pause)
            window.pauseButton.setMaximumWidth(60)
            window.miscLayout.addWidget(window.pauseButton)
        
        window.miscGroup.setLayout(window.miscLayout)
        window.miscGroup.setFixedSize(window.miscGroup.sizeHint())
        

    def addMenubar(self, window):
        window.menuBar = QtGui.QMenuBar()

        window.fileMenu = QtGui.QMenu("&File", self)
        window.openAction = window.fileMenu.addAction(QtGui.QIcon(self.resourcespath + 'folder_explore.png'), "&Open media file")
        window.openAction.triggered.connect(self.browseMediapath)
        window.exitAction = window.fileMenu.addAction(QtGui.QIcon(self.resourcespath + 'cross.png'), "E&xit")
        window.exitAction.triggered.connect(self.exitSyncplay)
        window.menuBar.addMenu(window.fileMenu)
        
        window.advancedMenu = QtGui.QMenu("&Advanced", self)
        window.setoffsetAction = window.advancedMenu.addAction(QtGui.QIcon(self.resourcespath + 'timeline_marker.png'),"Set &offset")
        window.setoffsetAction.triggered.connect(self.setOffset)
        window.menuBar.addMenu(window.advancedMenu)
        
        window.helpMenu = QtGui.QMenu("&Help", self)
        window.userguideAction = window.helpMenu.addAction(QtGui.QIcon(self.resourcespath + 'help.png'), "Open user &guide")
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
        
    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            if sys.platform.startswith('linux'):
                dropfilepath = unicode(urls[0].path())
            else:
                dropfilepath = unicode(urls[0].path().replace("/","\\"))[1:] # Removes starting slash 
            self._syncplayClient._player.openFile(dropfilepath)
    
    def saveSettings(self):
        settings = QSettings("Syncplay", "MainWindow")
        settings.beginGroup("MainWindow")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.endGroup()
    
    def loadSettings(self):
        settings = QSettings("Syncplay", "MainWindow")
        settings.beginGroup("MainWindow")
        self.resize(settings.value("size", QSize(700, 500)))
        self.move(settings.value("pos", QPoint(200, 200)))
        settings.endGroup()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.QtGui = QtGui
        if sys.platform.startswith('linux'):
            self.resourcespath = utils.findWorkingDir() + "/resources/"
        else:
            self.resourcespath = utils.findWorkingDir() + "\\resources\\"
        self.setWindowTitle("Syncplay v" + version)
        self.mainLayout = QtGui.QVBoxLayout()
        self.addTopLayout(self)
        self.addBottomLayout(self)
        self.addMenubar(self)
        self.addMainFrame(self)
        self.loadSettings()
        self.setWindowIcon(QtGui.QIcon(self.resourcespath + "syncplay.png"))
        self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint & Qt.WindowMinimizeButtonHint & ~Qt.WindowContextHelpButtonHint)
        self.show()
        self.setAcceptDrops(True)
