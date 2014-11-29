from PySide import QtGui
from PySide.QtCore import Qt, QSettings, QSize, QPoint
from syncplay import utils, constants, version
from syncplay.messages import getMessage
import sys
import time
import re
import os
from syncplay.utils import formatTime, sameFilename, sameFilesize, sameFileduration, RoomPasswordProvider, formatSize

class UserlistItemDelegate(QtGui.QStyledItemDelegate):
    def __init__(self):
        QtGui.QStyledItemDelegate.__init__(self)

    def sizeHint(self, option, index):
        size = QtGui.QStyledItemDelegate.sizeHint(self, option, index)
        if (index.column() == 0):
            size.setWidth(size.width() + constants.USERLIST_GUI_USERNAME_OFFSET)
        return size

    def paint(self, itemQPainter, optionQStyleOptionViewItem, indexQModelIndex):
        column = indexQModelIndex.column()
        if column == 0:
            currentQAbstractItemModel = indexQModelIndex.model()
            itemQModelIndex = currentQAbstractItemModel.index(indexQModelIndex.row(), 0, indexQModelIndex.parent())
            if sys.platform.startswith('win'):
                resourcespath = utils.findWorkingDir() + "\\resources\\"
            else:
                resourcespath = utils.findWorkingDir() + "/resources/"
            controlIconQPixmap = QtGui.QPixmap(resourcespath + "user_key.png")
            tickIconQPixmap = QtGui.QPixmap(resourcespath + "tick.png")
            crossIconQPixmap = QtGui.QPixmap(resourcespath + "cross.png")
            roomController = currentQAbstractItemModel.data(itemQModelIndex, Qt.UserRole + constants.USERITEM_CONTROLLER_ROLE)
            userReady = currentQAbstractItemModel.data(itemQModelIndex, Qt.UserRole + constants.USERITEM_READY_ROLE)

            if roomController and not controlIconQPixmap.isNull():
                itemQPainter.drawPixmap (
                    optionQStyleOptionViewItem.rect.x()+6,
                    optionQStyleOptionViewItem.rect.y(),
                    controlIconQPixmap.scaled(16, 16, Qt.KeepAspectRatio))

            if userReady and not tickIconQPixmap.isNull():
                itemQPainter.drawPixmap (
                    (optionQStyleOptionViewItem.rect.x()-10),
                    optionQStyleOptionViewItem.rect.y(),
                    tickIconQPixmap.scaled(16, 16, Qt.KeepAspectRatio))

            elif userReady == False and not crossIconQPixmap.isNull():
                itemQPainter.drawPixmap (
                    (optionQStyleOptionViewItem.rect.x()-10),
                    optionQStyleOptionViewItem.rect.y(),
                    crossIconQPixmap.scaled(16, 16, Qt.KeepAspectRatio))
            isUserRow = indexQModelIndex.parent() != indexQModelIndex.parent().parent()
            if isUserRow:
                optionQStyleOptionViewItem.rect.setX(optionQStyleOptionViewItem.rect.x()+constants.USERLIST_GUI_USERNAME_OFFSET)
        QtGui.QStyledItemDelegate.paint(self, itemQPainter, optionQStyleOptionViewItem, indexQModelIndex)

class MainWindow(QtGui.QMainWindow):
    class topSplitter(QtGui.QSplitter):
        def createHandle(self):
            return self.topSplitterHandle(self.orientation(), self)

        class topSplitterHandle(QtGui.QSplitterHandle):
            def mouseReleaseEvent(self, event):
                QtGui.QSplitterHandle.mouseReleaseEvent(self, event)
                self.parent().parent().parent().updateListGeometry()

            def mouseMoveEvent(self, event):
                QtGui.QSplitterHandle.mouseMoveEvent(self, event)
                self.parent().parent().parent().updateListGeometry()

    def addClient(self, client):
        self._syncplayClient = client
        self.roomInput.setText(self._syncplayClient.getRoom())
        self.config = self._syncplayClient.getConfig()
        try:
            if self.contactLabel and not self.config['showContactInfo']:
                self.contactLabel.hide()
            if not constants.SHOW_BUTTON_LABELS:
                self.hideRoomSeekLabels()
                self.hideMiscLabels()
        except ():
            pass

    def promptFor(self, prompt=">", message=""):
        # TODO: Prompt user
        return None

    def showMessage(self, message, noTimestamp=False):
        message = unicode(message)
        message = message.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        message = message.replace("&lt;", "<span style=\"{}\">&lt;".format(constants.STYLE_USERNAME))
        message = message.replace("&gt;", "&gt;</span>")
        message = message.replace("\n", "<br />")
        if noTimestamp:
            self.newMessage(message + "<br />")
        else:
            self.newMessage(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message + "<br />")

    def showUserList(self, currentUser, rooms):
        self._usertreebuffer = QtGui.QStandardItemModel()
        self._usertreebuffer.setHorizontalHeaderLabels(
            (getMessage("roomuser-heading-label"), getMessage("size-heading-label"), getMessage("duration-heading-label"), getMessage("filename-heading-label") ))
        usertreeRoot = self._usertreebuffer.invisibleRootItem()

        for room in rooms:
            roomitem = QtGui.QStandardItem(room)
            font = QtGui.QFont()
            font.setItalic(True)
            if room == currentUser.room:
                font.setWeight(QtGui.QFont.Bold)
            roomitem.setFont(font)
            roomitem.setFlags(roomitem.flags() & ~Qt.ItemIsEditable)
            usertreeRoot.appendRow(roomitem)
            isControlledRoom = RoomPasswordProvider.isControlledRoom(room)

            if isControlledRoom:
                if room == currentUser.room and currentUser.isController():
                    roomitem.setIcon(QtGui.QIcon(self.resourcespath + 'lock_open.png'))
                else:
                    roomitem.setIcon(QtGui.QIcon(self.resourcespath + 'lock.png'))
            else:
                roomitem.setIcon(QtGui.QIcon(self.resourcespath + 'chevrons_right.png'))

            for user in rooms[room]:
                useritem = QtGui.QStandardItem(user.username)
                isController = user.isController()
                useritem.setData(isController, Qt.UserRole + constants.USERITEM_CONTROLLER_ROLE)
                if user.file:
                    filesizeitem = QtGui.QStandardItem(formatSize(user.file['size']))
                    filedurationitem = QtGui.QStandardItem("({})".format(formatTime(user.file['duration'])))
                    filenameitem = QtGui.QStandardItem((user.file['name']))
                    if currentUser.file:
                        sameName = sameFilename(user.file['name'], currentUser.file['name'])
                        sameSize = sameFilesize(user.file['size'], currentUser.file['size'])
                        sameDuration = sameFileduration(user.file['duration'], currentUser.file['duration'])
                        sameRoom = room == currentUser.room
                        underlinefont = QtGui.QFont()
                        underlinefont.setUnderline(True)
                        if sameRoom:
                            if not sameName:
                                filenameitem.setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_DIFFERENTITEM_COLOR)))
                                filenameitem.setFont(underlinefont)
                            if not sameSize:
                                if currentUser.file is not None and formatSize(user.file['size']) == formatSize(currentUser.file['size']):
                                    filesizeitem = QtGui.QStandardItem(formatSize(user.file['size'],precise=True))
                                filesizeitem.setFont(underlinefont)
                                filesizeitem.setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_DIFFERENTITEM_COLOR)))
                            if not sameDuration:
                                filedurationitem.setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_DIFFERENTITEM_COLOR)))
                                filedurationitem.setFont(underlinefont)
                else:
                    filenameitem = QtGui.QStandardItem(getMessage("nofile-note"))
                    filedurationitem = QtGui.QStandardItem("")
                    filesizeitem = QtGui.QStandardItem("")
                    if room == currentUser.room:
                        filenameitem.setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_NOFILEITEM_COLOR)))
                font = QtGui.QFont()
                if currentUser.username == user.username:
                    font.setWeight(QtGui.QFont.Bold)
                if isControlledRoom and not isController:
                    useritem.setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_NOTCONTROLLER_COLOR)))
                useritem.setFont(font)
                useritem.setFlags(useritem.flags() & ~Qt.ItemIsEditable)
                filenameitem.setFlags(filenameitem.flags() & ~Qt.ItemIsEditable)
                filesizeitem.setFlags(filesizeitem.flags() & ~Qt.ItemIsEditable)
                filedurationitem.setFlags(filedurationitem.flags() & ~Qt.ItemIsEditable)
                roomitem.appendRow((useritem, filesizeitem, filedurationitem, filenameitem))
        self.listTreeModel = self._usertreebuffer
        self.listTreeView.setModel(self.listTreeModel)
        self.listTreeView.setItemDelegate(UserlistItemDelegate())
        self.listTreeView.setItemsExpandable(False)
        self.listTreeView.setRootIsDecorated(False)
        self.listTreeView.expandAll()
        self.updateListGeometry()

    def updateListGeometry(self):
        try:
            roomtocheck = 0
            while self.listTreeModel.item(roomtocheck):
                self.listTreeView.setFirstColumnSpanned(roomtocheck, self.listTreeView.rootIndex(), True)
                roomtocheck += 1
            self.listTreeView.header().setStretchLastSection(False)
            self.listTreeView.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
            self.listTreeView.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
            self.listTreeView.header().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
            self.listTreeView.header().setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
            NarrowTabsWidth = self.listTreeView.header().sectionSize(0)+self.listTreeView.header().sectionSize(1)+self.listTreeView.header().sectionSize(2)
            if self.listTreeView.header().width() < (NarrowTabsWidth+self.listTreeView.header().sectionSize(3)):
                self.listTreeView.header().resizeSection(3,self.listTreeView.header().width()-NarrowTabsWidth)
            else:
                self.listTreeView.header().setResizeMode(3, QtGui.QHeaderView.Stretch)
            self.listTreeView.expandAll()
        except:
            pass

    def roomClicked(self, item):
        while item.parent().row() != -1:
            item = item.parent()
        self.joinRoom(item.sibling(item.row(), 0).data())

    def userListChange(self):
        self._syncplayClient.showUserList()

    def updateRoomName(self, room=""):
        self.roomInput.setText(room)

    def showDebugMessage(self, message):
        print(message)

    def showErrorMessage(self, message, criticalerror=False):
        message = unicode(message)
        if criticalerror:
            QtGui.QMessageBox.critical(self, "Syncplay", message)
        message = message.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        message = message.replace("\n", "<br />")
        message = "<span style=\"{}\">".format(constants.STYLE_ERRORNOTIFICATION) + message + "</span>"
        self.newMessage(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message + "<br />")

    def joinRoom(self, room=None):
        if room == None:
            room = self.roomInput.text()
        if room == "":
            if self._syncplayClient.userlist.currentUser.file:
                room = self._syncplayClient.userlist.currentUser.file["name"]
            else:
                room = self._syncplayClient.defaultRoom
        self.roomInput.setText(room)
        if room != self._syncplayClient.getRoom():
            self._syncplayClient.setRoom(room)
            self._syncplayClient.sendRoom()

    def seekPosition(self):
        s = re.match(constants.UI_SEEK_REGEX, self.seekInput.text())
        if s:
            sign = self._extractSign(s.group('sign'))
            t = utils.parseTime(s.group('time'))
            if t is None:
                return
            if sign:
                t = self._syncplayClient.getGlobalPosition() + sign * t
            self._syncplayClient.setPosition(t)

        else:
            self.showErrorMessage("Invalid seek value")

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

    def setupSizes(self):
        self.hideRoomSeekLabels()
        self.miscThreshold = self.seekGroup.sizeHint().width()+self.roomGroup.sizeHint().width()+self.miscGroup.sizeHint().width()+30
        self.hideMiscLabels()
        self.setMinimumWidth(self.seekGroup.sizeHint().width()+self.roomGroup.sizeHint().width()+self.miscGroup.sizeHint().width()+30)
        self.seekGroup.setMinimumWidth(self.seekGroup.sizeHint().width())
        self.roomGroup.setMinimumWidth(self.roomGroup.sizeHint().width())
        self.miscGroup.setMinimumWidth(self.miscGroup.sizeHint().width())
        self.showRoomSeekLabels()
        self.showMiscLabels()
        windowMaximumWidth = self.maximumWidth()
        self.seekGroup.setMaximumWidth(self.seekGroup.sizeHint().width())
        self.roomGroup.setMaximumWidth(self.roomGroup.sizeHint().width())
        self.miscGroup.setMaximumWidth(self.miscGroup.sizeHint().width())
        self.setMaximumWidth(windowMaximumWidth)
        self.roomSeekThreshold = self.mainLayout.sizeHint().width()

    def hideRoomSeekLabels(self):
        self.roomButton.setText("")
        self.seekButton.setText("")

    def hideMiscLabels(self):
        self.unseekButton.setText("")
        if constants.MERGE_PLAYPAUSE_BUTTONS:
            self.playpauseButton.setText("")
        else:
            self.playButton.setText("")
            self.pauseButton.setText("")

    def showRoomSeekLabels(self):
        if not constants.SHOW_BUTTON_LABELS:
            return
        self.roomButton.setText(getMessage("joinroom-guibuttonlabel"))
        self.seekButton.setText(getMessage("seektime-guibuttonlabel"))

    def showMiscLabels(self):
        self.unseekButton.setText(getMessage("undoseek-guibuttonlabel"))
        if not constants.SHOW_BUTTON_LABELS:
            return
        if constants.MERGE_PLAYPAUSE_BUTTONS:
            self.playpauseButton.setText(getMessage("togglepause-guibuttonlabel"))
        else:
            self.playButton.setText(getMessage("play-guibuttonlabel"))
            self.pauseButton.setText(getMessage("pause-guibuttonlabel"))

    def resizeEvent(self,resizeEvent):
        self.updateListGeometry()
        if self.roomGroup and self.miscThreshold:
            currentWidth = self.mainFrame.size().width()
            if currentWidth < self.miscThreshold:
                 if self.unseekButton.text() != "":
                    self.hideMiscLabels()
            else:
                if self.unseekButton.text() == "":
                    self.showMiscLabels()

            if currentWidth < self.roomSeekThreshold:
                if self.roomButton.text() != "":
                    self.hideRoomSeekLabels()
            else:
                if self.roomButton.text() == "":
                    self.showRoomSeekLabels()

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
        if os.path.isdir(self.mediadirectory):
            defaultdirectory = self.mediadirectory
        elif os.path.isdir(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MoviesLocation)):
            defaultdirectory = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MoviesLocation)
        elif os.path.isdir(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)):
            defaultdirectory = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)
        else:
            defaultdirectory = ""
        browserfilter = "All files (*)"
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self, getMessage("browseformedia-label"), defaultdirectory,
                                                            browserfilter, "", options)
        if fileName:
            if sys.platform.startswith('win'):
                fileName = fileName.replace("/", "\\")
            self.mediadirectory = os.path.dirname(fileName)
            self.saveMediaBrowseSettings()
            self._syncplayClient._player.openFile(fileName)

    def createControlledRoom(self):
        controlroom, ok = QtGui.QInputDialog.getText(self, getMessage("createcontrolledroom-msgbox-label"),
                getMessage("controlledroominfo-msgbox-label"), QtGui.QLineEdit.Normal,
                utils.stripRoomName(self._syncplayClient.getRoom()))
        if ok and controlroom != '':
            self._syncplayClient.createControlledRoom(controlroom)

    def identifyAsController(self):
        msgboxtitle = getMessage("identifyascontroller-msgbox-label")
        msgboxtext = getMessage("identifyinfo-msgbox-label")
        controlpassword, ok = QtGui.QInputDialog.getText(self, msgboxtitle, msgboxtext, QtGui.QLineEdit.Normal, "")
        if ok and controlpassword != '':
            self._syncplayClient.identifyAsController(controlpassword)

    def _extractSign(self, m):
        if m:
            if m == "-":
                return -1
            else:
                return 1
        else:
            return None

    def setOffset(self):
        newoffset, ok = QtGui.QInputDialog.getText(self, getMessage("setoffset-msgbox-label"),
                                                   getMessage("offsetinfo-msgbox-label"), QtGui.QLineEdit.Normal,
                                                   "")
        if ok and newoffset != '':
            o = re.match(constants.UI_OFFSET_REGEX, "o " + newoffset)
            if o:
                sign = self._extractSign(o.group('sign'))
                t = utils.parseTime(o.group('time'))
                if t is None:
                    return
                if o.group('sign') == "/":
                    t = self._syncplayClient.getPlayerPosition() - t
                elif sign:
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
        window.topSplit = self.topSplitter(Qt.Horizontal, self)

        window.outputLayout = QtGui.QVBoxLayout()
        window.outputbox = QtGui.QTextEdit()
        window.outputbox.setReadOnly(True)
        window.outputlabel = QtGui.QLabel(getMessage("notifications-heading-label"))
        window.outputFrame = QtGui.QFrame()
        window.outputFrame.setLineWidth(0)
        window.outputFrame.setMidLineWidth(0)
        window.outputLayout.setContentsMargins(0, 0, 0, 0)
        window.outputLayout.addWidget(window.outputlabel)
        window.outputLayout.addWidget(window.outputbox)
        window.outputFrame.setLayout(window.outputLayout)

        window.listLayout = QtGui.QVBoxLayout()
        window.listTreeModel = QtGui.QStandardItemModel()
        window.listTreeView = QtGui.QTreeView()
        window.listTreeView.setModel(window.listTreeModel)
        window.listTreeView.setIndentation(21)
        window.listTreeView.doubleClicked.connect(self.roomClicked)
        window.listlabel = QtGui.QLabel(getMessage("userlist-heading-label"))
        window.listFrame = QtGui.QFrame()
        window.listFrame.setLineWidth(0)
        window.listFrame.setMidLineWidth(0)
        window.listLayout.setContentsMargins(0, 0, 0, 0)
        window.listLayout.addWidget(window.listlabel)
        window.listLayout.addWidget(window.listTreeView)
        window.contactLabel = QtGui.QLabel()
        window.contactLabel.setWordWrap(True)
        window.contactLabel.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        window.contactLabel.setLineWidth(1)
        window.contactLabel.setMidLineWidth(0)
        window.contactLabel.setMargin(2)
        window.contactLabel.setText(getMessage("contact-label"))
        window.contactLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        window.contactLabel.setOpenExternalLinks(True)
        window.listLayout.addWidget(window.contactLabel)
        window.listFrame.setLayout(window.listLayout)

        window.topSplit.addWidget(window.outputFrame)
        window.topSplit.addWidget(window.listFrame)
        window.topSplit.setStretchFactor(0,4)
        window.topSplit.setStretchFactor(1,5)
        window.mainLayout.addWidget(window.topSplit)
        window.topSplit.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)

    def addBottomLayout(self, window):
        window.bottomLayout = QtGui.QHBoxLayout()

        window.addRoomBox(MainWindow)
        window.addSeekBox(MainWindow)
        window.addMiscBox(MainWindow)

        window.bottomLayout.addWidget(window.roomGroup)
        window.bottomLayout.addWidget(window.seekGroup)
        window.bottomLayout.addWidget(window.miscGroup)

        window.mainLayout.addLayout(window.bottomLayout, Qt.AlignLeft)

    def addRoomBox(self, window):
        window.roomGroup = QtGui.QGroupBox(getMessage("room-heading-label"))

        window.roomInput = QtGui.QLineEdit()
        window.roomInput.returnPressed.connect(self.joinRoom)
        window.roomButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'door_in.png'),
                                              getMessage("joinroom-guibuttonlabel"))
        window.roomButton.pressed.connect(self.joinRoom)
        window.roomLayout = QtGui.QHBoxLayout()
        window.roomInput.setFixedWidth(150)

        self.roomButton.setToolTip(getMessage("joinroom-tooltip"))

        window.roomLayout.addWidget(window.roomInput)
        window.roomLayout.addWidget(window.roomButton)

        window.roomGroup.setLayout(window.roomLayout)
        window.roomGroup.setFixedHeight(window.roomGroup.sizeHint().height())

    def addSeekBox(self, window):
        window.seekGroup = QtGui.QGroupBox(getMessage("seek-heading-label"))

        window.seekInput = QtGui.QLineEdit()
        window.seekInput.returnPressed.connect(self.seekPosition)
        window.seekButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'clock_go.png'),
                                              getMessage("seektime-guibuttonlabel"))
        window.seekButton.pressed.connect(self.seekPosition)

        self.seekButton.setToolTip(getMessage("seektime-tooltip"))

        window.seekLayout = QtGui.QHBoxLayout()
        window.seekInput.setText("0:00")
        window.seekInput.setFixedWidth(60)

        window.seekLayout.addWidget(window.seekInput)
        window.seekLayout.addWidget(window.seekButton)

        window.seekGroup.setLayout(window.seekLayout)
        window.seekGroup.setFixedHeight(window.seekGroup.sizeHint().height())

    def addMiscBox(self, window):
        window.miscGroup = QtGui.QGroupBox(getMessage("othercommands-heading-label"))

        window.unseekButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'arrow_undo.png'),
                                                getMessage("undoseek-guibuttonlabel"))
        window.unseekButton.pressed.connect(self.undoSeek)
        self.unseekButton.setToolTip(getMessage("undoseek-tooltip"))

        window.miscLayout = QtGui.QHBoxLayout()
        window.miscLayout.addWidget(window.unseekButton)
        if constants.MERGE_PLAYPAUSE_BUTTONS == True:
            window.playpauseButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'control_pause_blue.png'),
                                                       getMessage("togglepause-guibuttonlabel"))
            window.playpauseButton.pressed.connect(self.togglePause)
            window.miscLayout.addWidget(window.playpauseButton)
            self.playpauseButton.setToolTip(getMessage("togglepause-tooltip"))
        else:
            window.playButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'control_play_blue.png'),
                                                  getMessage("play-guibuttonlabel"))
            window.playButton.pressed.connect(self.play)
            window.playButton.setMaximumWidth(60)
            window.miscLayout.addWidget(window.playButton)
            window.pauseButton = QtGui.QPushButton(QtGui.QIcon(self.resourcespath + 'control_pause_blue.png'),
                                                   getMessage("pause-guibuttonlabel"))
            window.pauseButton.pressed.connect(self.pause)
            window.pauseButton.setMaximumWidth(60)
            window.miscLayout.addWidget(window.pauseButton)
            self.playButton.setToolTip(getMessage("play-tooltip"))
            self.pauseButton.setToolTip(getMessage("pause-tooltip"))

        window.miscGroup.setLayout(window.miscLayout)
        window.miscGroup.setFixedHeight(window.miscGroup.sizeHint().height())


    def addMenubar(self, window):
        window.menuBar = QtGui.QMenuBar()

        window.fileMenu = QtGui.QMenu(getMessage("file-menu-label"), self)
        window.openAction = window.fileMenu.addAction(QtGui.QIcon(self.resourcespath + 'folder_explore.png'),
                                                      getMessage("openmedia-menu-label"))
        window.openAction.triggered.connect(self.browseMediapath)

        window.exitAction = window.fileMenu.addAction(QtGui.QIcon(self.resourcespath + 'cross.png'),
                                                      getMessage("file-menu-label"))
        window.exitAction.triggered.connect(self.exitSyncplay)
        window.menuBar.addMenu(window.fileMenu)

        window.advancedMenu = QtGui.QMenu(getMessage("advanced-menu-label"), self)
        window.setoffsetAction = window.advancedMenu.addAction(QtGui.QIcon(self.resourcespath + 'timeline_marker.png'),
                                                               getMessage("setoffset-menu-label"))
        window.setoffsetAction.triggered.connect(self.setOffset)

        window.createcontrolledroomAction = window.advancedMenu.addAction(
            QtGui.QIcon(self.resourcespath + 'page_white_key.png'), getMessage("createcontrolledroom-menu-label"))
        window.createcontrolledroomAction.triggered.connect(self.createControlledRoom)
        window.identifyascontroller = window.advancedMenu.addAction(QtGui.QIcon(self.resourcespath + 'key_go.png'),
                                                                    getMessage("identifyascontroller-menu-label"))
        window.identifyascontroller.triggered.connect(self.identifyAsController)
        window.menuBar.addMenu(window.advancedMenu)

        window.helpMenu = QtGui.QMenu(getMessage("help-menu-label"), self)
        window.userguideAction = window.helpMenu.addAction(QtGui.QIcon(self.resourcespath + 'help.png'),
                                                           getMessage("userguide-menu-label"))
        window.userguideAction.triggered.connect(self.openUserGuide)

        window.menuBar.addMenu(window.helpMenu)
        window.mainLayout.setMenuBar(window.menuBar)

    def addMainFrame(self, window):
        window.mainFrame = QtGui.QFrame()
        window.mainFrame.setLineWidth(0)
        window.mainFrame.setMidLineWidth(0)
        window.mainFrame.setContentsMargins(0, 0, 0, 0)
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
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        rewindFile = False
        if QtGui.QDropEvent.proposedAction(event) == Qt.MoveAction:
            QtGui.QDropEvent.setDropAction(event, Qt.CopyAction)  # Avoids file being deleted
            rewindFile = True
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            dropfilepath = os.path.abspath(unicode(event.mimeData().urls()[0].toLocalFile()))
            if rewindFile == False:
                self._syncplayClient._player.openFile(dropfilepath)
            else:
                self._syncplayClient.setPosition(0)
                self._syncplayClient._player.openFile(dropfilepath, resetPosition=True)
                self._syncplayClient.setPosition(0)

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
        if sys.platform.startswith('win'):
            self.resourcespath = utils.findWorkingDir() + "\\resources\\"
        else:
            self.resourcespath = utils.findWorkingDir() + "/resources/"
        self.setWindowFlags(self.windowFlags() & Qt.AA_DontUseNativeMenuBar)
        self.setWindowTitle("Syncplay v" + version)
        self.mainLayout = QtGui.QVBoxLayout()
        self.addTopLayout(self)
        self.addBottomLayout(self)
        self.addMenubar(self)
        self.addMainFrame(self)
        self.setupSizes()
        self.loadSettings()
        self.setWindowIcon(QtGui.QIcon(self.resourcespath + "syncplay.png"))
        self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint & Qt.AA_DontUseNativeMenuBar & Qt.WindowMinimizeButtonHint & ~Qt.WindowContextHelpButtonHint)
        self.show()
        self.setAcceptDrops(True)
