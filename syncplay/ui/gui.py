
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from functools import wraps
from platform import python_version

from twisted.internet import task

from syncplay import utils, constants, version, revision, release_number
from syncplay.messages import getMessage
from syncplay.ui.consoleUI import ConsoleUI
from syncplay.utils import resourcespath
from syncplay.utils import isLinux, isWindows, isMacOS
from syncplay.utils import formatTime, sameFilename, sameFilesize, sameFileduration, RoomPasswordProvider, formatSize, isURL
from syncplay.vendor import Qt
from syncplay.vendor.Qt import QtCore, QtWidgets, QtGui, __binding__, __binding_version__, __qt_version__, IsPySide, IsPySide2, IsPySide6
from syncplay.vendor.Qt.QtCore import Qt, QSettings, QSize, QPoint, QUrl, QLine, QDateTime
applyDPIScaling = True
if isLinux():
    applyDPIScaling = False
else:
    applyDPIScaling = True
try:
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, applyDPIScaling)
except AttributeError:
    pass  # To ignore error "Attribute Qt::AA_EnableHighDpiScaling must be set before QCoreApplication is created"
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, applyDPIScaling)
if IsPySide6:
    from PySide6.QtCore import QStandardPaths
elif IsPySide2:
    from PySide2.QtCore import QStandardPaths
if isMacOS() and IsPySide:
    from Foundation import NSURL
    from Cocoa import NSString, NSUTF8StringEncoding
lastCheckedForUpdates = None
from syncplay.vendor import darkdetect
if isMacOS() or isWindows():
	isDarkMode = darkdetect.isDark()
else:
	isDarkMode = None


class ConsoleInGUI(ConsoleUI):
    def showMessage(self, message, noTimestamp=False):
        self._syncplayClient.ui.showMessage(message, True)

    def showDebugMessage(self, message):
        self._syncplayClient.ui.showDebugMessage(message)

    def showErrorMessage(self, message, criticalerror=False):
        self._syncplayClient.ui.showErrorMessage(message, criticalerror)

    def updateRoomName(self, room=""): #bob
        self._syncplayClient.ui.updateRoomName(room)

    def getUserlist(self):
        self._syncplayClient.showUserList(self)


class UserlistItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, view=None):
        self.view = view
        QtWidgets.QStyledItemDelegate.__init__(self)

    def sizeHint(self, option, index):
        size = QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)
        if (index.column() == constants.USERLIST_GUI_USERNAME_COLUMN):
            size.setWidth(size.width() + constants.USERLIST_GUI_USERNAME_OFFSET)
        return size

    def paint(self, itemQPainter, optionQStyleOptionViewItem, indexQModelIndex):
        column = indexQModelIndex.column()
        midY = int((optionQStyleOptionViewItem.rect.y() + optionQStyleOptionViewItem.rect.bottomLeft().y()) / 2)
        if column == constants.USERLIST_GUI_USERNAME_COLUMN:
            currentQAbstractItemModel = indexQModelIndex.model()
            itemQModelIndex = currentQAbstractItemModel.index(indexQModelIndex.row(), constants.USERLIST_GUI_USERNAME_COLUMN, indexQModelIndex.parent())
            controlIconQPixmap = QtGui.QPixmap(resourcespath + "user_key.png")
            tickIconQPixmap = QtGui.QPixmap(resourcespath + "tick.png")
            crossIconQPixmap = QtGui.QPixmap(resourcespath + "cross.png")
            roomController = currentQAbstractItemModel.data(itemQModelIndex, Qt.UserRole + constants.USERITEM_CONTROLLER_ROLE)
            userReady = currentQAbstractItemModel.data(itemQModelIndex, Qt.UserRole + constants.USERITEM_READY_ROLE)
            isUserRow = indexQModelIndex.parent() != indexQModelIndex.parent().parent()
            bkgColor = self.view.palette().color(QtGui.QPalette.Base)
            if isUserRow and (isMacOS() or isLinux()):
                blankRect = QtCore.QRect(0, optionQStyleOptionViewItem.rect.y(), optionQStyleOptionViewItem.rect.width(), optionQStyleOptionViewItem.rect.height())
                itemQPainter.fillRect(blankRect, bkgColor)

            if roomController and not controlIconQPixmap.isNull():
                itemQPainter.drawPixmap(
                    optionQStyleOptionViewItem.rect.x()+6,
                    midY-8,
                    controlIconQPixmap.scaled(16, 16, Qt.KeepAspectRatio))

            if userReady and not tickIconQPixmap.isNull():
                itemQPainter.drawPixmap(
                    (optionQStyleOptionViewItem.rect.x()-10),
                    midY - 8,
                    tickIconQPixmap.scaled(16, 16, Qt.KeepAspectRatio))

            elif userReady == False and not crossIconQPixmap.isNull():
                itemQPainter.drawPixmap(
                    (optionQStyleOptionViewItem.rect.x()-10),
                    midY - 8,
                    crossIconQPixmap.scaled(16, 16, Qt.KeepAspectRatio))
            if isUserRow:
                optionQStyleOptionViewItem.rect.setX(optionQStyleOptionViewItem.rect.x()+constants.USERLIST_GUI_USERNAME_OFFSET)
        if column == constants.USERLIST_GUI_FILENAME_COLUMN:
            currentQAbstractItemModel = indexQModelIndex.model()
            itemQModelIndex = currentQAbstractItemModel.index(indexQModelIndex.row(), constants.USERLIST_GUI_FILENAME_COLUMN, indexQModelIndex.parent())
            fileSwitchRole = currentQAbstractItemModel.data(itemQModelIndex, Qt.UserRole + constants.FILEITEM_SWITCH_ROLE)
            if fileSwitchRole == constants.FILEITEM_SWITCH_FILE_SWITCH:
                fileSwitchIconQPixmap = QtGui.QPixmap(resourcespath + "film_go.png")
                itemQPainter.drawPixmap(
                    (optionQStyleOptionViewItem.rect.x()),
                    midY - 8,
                    fileSwitchIconQPixmap.scaled(16, 16, Qt.KeepAspectRatio))
                optionQStyleOptionViewItem.rect.setX(optionQStyleOptionViewItem.rect.x()+16)

            elif fileSwitchRole == constants.FILEITEM_SWITCH_STREAM_SWITCH:
                streamSwitchIconQPixmap = QtGui.QPixmap(resourcespath + "world_go.png")
                itemQPainter.drawPixmap(
                    (optionQStyleOptionViewItem.rect.x()),
                    midY - 8,
                    streamSwitchIconQPixmap.scaled(16, 16, Qt.KeepAspectRatio))
                optionQStyleOptionViewItem.rect.setX(optionQStyleOptionViewItem.rect.x()+16)
        QtWidgets.QStyledItemDelegate.paint(self, itemQPainter, optionQStyleOptionViewItem, indexQModelIndex)


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        if isMacOS():
            self.setWindowTitle("")
            self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint)
        else:
            self.setWindowTitle(getMessage("about-dialog-title"))
            if isWindows():
                self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QtGui.QPixmap(resourcespath + 'syncplay.png'))
        nameLabel = QtWidgets.QLabel("<center><strong>Syncplay</strong></center>")
        nameLabel.setFont(QtGui.QFont("Helvetica", 18))
        linkLabel = QtWidgets.QLabel()
        if isDarkMode:
            linkLabel.setText(("<center><a href=\"https://syncplay.pl\" style=\"{}\">syncplay.pl</a></center>").format(constants.STYLE_DARK_ABOUT_LINK_COLOR))
        else:
            linkLabel.setText("<center><a href=\"https://syncplay.pl\">syncplay.pl</a></center>")
        linkLabel.setOpenExternalLinks(True)
        versionExtString = version + revision
        versionLabel = QtWidgets.QLabel(
            "<p><center>" + getMessage("about-dialog-release").format(versionExtString, release_number) +
            "<br />Python " + python_version() + " - " + __binding__ + " " + __binding_version__ +
            " - Qt " + __qt_version__ + "</center></p>")
        licenseLabel = QtWidgets.QLabel(
            "<center><p>Copyright &copy; 2012&ndash;2019 Syncplay</p><p>" +
            getMessage("about-dialog-license-text") + "</p></center>")
        aboutIcon = QtGui.QIcon()
        aboutIcon.addFile(resourcespath + "syncplayAbout.png")
        aboutIconLabel = QtWidgets.QLabel()
        aboutIconLabel.setPixmap(aboutIcon.pixmap(64, 64))
        aboutLayout = QtWidgets.QGridLayout()
        aboutLayout.addWidget(aboutIconLabel, 0, 0, 3, 4, Qt.AlignHCenter)
        aboutLayout.addWidget(nameLabel, 3, 0, 1, 4)
        aboutLayout.addWidget(linkLabel, 4, 0, 1, 4)
        aboutLayout.addWidget(versionLabel, 5, 0, 1, 4)
        aboutLayout.addWidget(licenseLabel, 6, 0, 1, 4)
        licenseButton = QtWidgets.QPushButton(getMessage("about-dialog-license-button"))
        licenseButton.setAutoDefault(False)
        licenseButton.clicked.connect(self.openLicense)
        aboutLayout.addWidget(licenseButton, 7, 0, 1, 2)
        dependenciesButton = QtWidgets.QPushButton(getMessage("about-dialog-dependencies"))
        dependenciesButton.setAutoDefault(False)
        dependenciesButton.clicked.connect(self.openDependencies)
        aboutLayout.addWidget(dependenciesButton, 7, 2, 1, 2)
        aboutLayout.setVerticalSpacing(10)
        aboutLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setSizeGripEnabled(False)
        self.setLayout(aboutLayout)

    def openLicense(self):
        if isWindows():
                QtGui.QDesktopServices.openUrl(QUrl("file:///" + resourcespath + "license.rtf"))
        else:
                QtGui.QDesktopServices.openUrl(QUrl("file://" + resourcespath + "license.rtf"))

    def openDependencies(self):
        if isWindows():
            QtGui.QDesktopServices.openUrl(QUrl("file:///" + resourcespath + "third-party-notices.txt"))
        else:
            QtGui.QDesktopServices.openUrl(QUrl("file://" + resourcespath + "third-party-notices.txt"))


class CertificateDialog(QtWidgets.QDialog):
    def __init__(self, tlsData, parent=None):
        super(CertificateDialog, self).__init__(parent)
        if isMacOS():
            self.setWindowTitle("")
            self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint)
        else:
            self.setWindowTitle(getMessage("tls-information-title"))
            if isWindows():
                self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QtGui.QPixmap(resourcespath + 'syncplay.png'))
        statusLabel = QtWidgets.QLabel(getMessage("tls-dialog-status-label").format(tlsData["subject"]))
        descLabel = QtWidgets.QLabel(getMessage("tls-dialog-desc-label").format(tlsData["subject"]))
        connDataLabel = QtWidgets.QLabel(getMessage("tls-dialog-connection-label").format(tlsData["protocolVersion"], tlsData["cipher"]))
        certDataLabel = QtWidgets.QLabel(getMessage("tls-dialog-certificate-label").format(tlsData["issuer"], tlsData["expires"]))
        if isMacOS():
            statusLabel.setFont(QtGui.QFont("Helvetica", 12))
            descLabel.setFont(QtGui.QFont("Helvetica", 12))
            connDataLabel.setFont(QtGui.QFont("Helvetica", 12))
            certDataLabel.setFont(QtGui.QFont("Helvetica", 12))
        lockIcon = QtGui.QIcon()
        lockIcon.addFile(resourcespath + "lock_green_dialog.png")
        lockIconLabel = QtWidgets.QLabel()
        lockIconLabel.setPixmap(lockIcon.pixmap(64, 64))
        certLayout = QtWidgets.QGridLayout()
        certLayout.addWidget(lockIconLabel, 1, 0, 3, 1, Qt.AlignLeft | Qt.AlignTop)
        certLayout.addWidget(statusLabel, 0, 1, 1, 3)
        certLayout.addWidget(descLabel, 1, 1, 1, 3)
        certLayout.addWidget(connDataLabel, 2, 1, 1, 3)
        certLayout.addWidget(certDataLabel, 3, 1, 1, 3)
        closeButton = QtWidgets.QPushButton("Close")
        closeButton.setFixedWidth(100)
        closeButton.setAutoDefault(False)
        closeButton.clicked.connect(self.closeDialog)
        certLayout.addWidget(closeButton, 4, 3, 1, 1)
        certLayout.setVerticalSpacing(10)
        certLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setSizeGripEnabled(False)
        self.setLayout(certLayout)

    def closeDialog(self):
        self.close()


class MainWindow(QtWidgets.QMainWindow):
    insertPosition = None
    playlistState = []
    updatingPlaylist = False
    playlistIndex = None
    sslInformation = "N/A"
    sslMode = False


    def setPlaylistInsertPosition(self, newPosition):
        if not self.playlist.isEnabled():
            return
        if MainWindow.insertPosition != newPosition:
            MainWindow.insertPosition = newPosition
            self.playlist.forceUpdate()

    class PlaylistItemDelegate(QtWidgets.QStyledItemDelegate):
        def paint(self, itemQPainter, optionQStyleOptionViewItem, indexQModelIndex):
            itemQPainter.save()
            currentQAbstractItemModel = indexQModelIndex.model()
            currentlyPlayingFile = currentQAbstractItemModel.data(indexQModelIndex, Qt.UserRole + constants.PLAYLISTITEM_CURRENTLYPLAYING_ROLE)
            if currentlyPlayingFile:
                currentlyplayingIconQPixmap = QtGui.QPixmap(resourcespath + "bullet_right_grey.png")
                midY = int((optionQStyleOptionViewItem.rect.y() + optionQStyleOptionViewItem.rect.bottomLeft().y()) / 2)
                itemQPainter.drawPixmap(
                    (optionQStyleOptionViewItem.rect.x()+4),
                    midY-8,
                    currentlyplayingIconQPixmap.scaled(6, 16, Qt.KeepAspectRatio))
                optionQStyleOptionViewItem.rect.setX(optionQStyleOptionViewItem.rect.x()+10)

            QtWidgets.QStyledItemDelegate.paint(self, itemQPainter, optionQStyleOptionViewItem, indexQModelIndex)

            lineAbove = False
            lineBelow = False
            if MainWindow.insertPosition == 0 and indexQModelIndex.row() == 0:
                lineAbove = True
            elif MainWindow.insertPosition and indexQModelIndex.row() == MainWindow.insertPosition-1:
                lineBelow = True
            if lineAbove:
                line = QLine(optionQStyleOptionViewItem.rect.topLeft(), optionQStyleOptionViewItem.rect.topRight())
                itemQPainter.drawLine(line)
            elif lineBelow:
                line = QLine(optionQStyleOptionViewItem.rect.bottomLeft(), optionQStyleOptionViewItem.rect.bottomRight())
                itemQPainter.drawLine(line)
            itemQPainter.restore()

    class PlaylistGroupBox(QtWidgets.QGroupBox):

        def dragEnterEvent(self, event):
            data = event.mimeData()
            urls = data.urls()
            window = self.parent().parent().parent().parent().parent()
            if urls and urls[0].scheme() == 'file':
                event.acceptProposedAction()
                window.setPlaylistInsertPosition(window.playlist.count())
            else:
                super(MainWindow.PlaylistGroupBox, self).dragEnterEvent(event)

        def dragLeaveEvent(self, event):
            window = self.parent().parent().parent().parent().parent()
            window.setPlaylistInsertPosition(None)

        def dropEvent(self, event):
            window = self.parent().parent().parent().parent().parent()
            if not window.playlist.isEnabled():
                return
            window.setPlaylistInsertPosition(None)
            if QtGui.QDropEvent.proposedAction(event) == Qt.MoveAction:
                QtGui.QDropEvent.setDropAction(event, Qt.CopyAction)  # Avoids file being deleted
            data = event.mimeData()
            urls = data.urls()

            if urls and urls[0].scheme() == 'file':
                indexRow = window.playlist.count() if window.clearedPlaylistNote else 0

                for url in urls[::-1]:
                    if isMacOS() and IsPySide:
                        macURL = NSString.alloc().initWithString_(str(url.toString()))
                        pathString = macURL.stringByAddingPercentEscapesUsingEncoding_(NSUTF8StringEncoding)
                        dropfilepath = os.path.abspath(NSURL.URLWithString_(pathString).filePathURL().path())
                    else:
                        dropfilepath = os.path.abspath(str(url.toLocalFile()))
                    if os.path.isfile(dropfilepath):
                        window.addFileToPlaylist(dropfilepath, indexRow)
                    elif os.path.isdir(dropfilepath):
                        window.addFolderToPlaylist(dropfilepath)
            else:
                super(MainWindow.PlaylistWidget, self).dropEvent(event)

    class PlaylistWidget(QtWidgets.QListWidget):
        selfWindow = None
        playlistIndexFilename = None

        def setPlaylistIndexFilename(self, filename):
            if filename != self.playlistIndexFilename:
                self.playlistIndexFilename = filename
            self.updatePlaylistIndexIcon()

        def updatePlaylistIndexIcon(self):
            for item in range(self.count()):
                itemFilename = self.item(item).text()
                isPlayingFilename = itemFilename == self.playlistIndexFilename
                self.item(item).setData(Qt.UserRole + constants.PLAYLISTITEM_CURRENTLYPLAYING_ROLE, isPlayingFilename)
                fileIsAvailable = self.selfWindow.isFileAvailable(itemFilename)
                fileIsUntrusted = self.selfWindow.isItemUntrusted(itemFilename)
                if fileIsUntrusted:
                    if isDarkMode:
                        self.item(item).setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_DARK_UNTRUSTEDITEM_COLOR)))
                    else:
                        self.item(item).setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_UNTRUSTEDITEM_COLOR)))
                elif fileIsAvailable:
                    self.item(item).setForeground(QtGui.QBrush(self.selfWindow.palette().color(QtGui.QPalette.Text)))
                else:
                    if isDarkMode:
                        self.item(item).setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_DARK_DIFFERENTITEM_COLOR)))
                    else:
                        self.item(item).setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_DIFFERENTITEM_COLOR)))
            self.selfWindow._syncplayClient.fileSwitch.setFilenameWatchlist(self.selfWindow.newWatchlist)
            self.forceUpdate()

        def setWindow(self, window):
            self.selfWindow = window

        def dragLeaveEvent(self, event):
            window = self.parent().parent().parent().parent().parent().parent()
            window.setPlaylistInsertPosition(None)

        def forceUpdate(self):
            root = self.rootIndex()
            self.dataChanged(root, root)

        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Delete:
                self.remove_selected_items()
            else:
                super(MainWindow.PlaylistWidget, self).keyPressEvent(event)

        def updatePlaylist(self, newPlaylist):
            for index in range(self.count()):
                self.takeItem(0)
            uniquePlaylist = []
            for item in newPlaylist:
                if item not in uniquePlaylist:
                    uniquePlaylist.append(item)
            self.insertItems(0, uniquePlaylist)
            self.updatePlaylistIndexIcon()

        def remove_selected_items(self):
            for item in self.selectedItems():
                self.takeItem(self.row(item))

        def dragEnterEvent(self, event):
            data = event.mimeData()
            urls = data.urls()
            if urls and urls[0].scheme() == 'file':
                event.acceptProposedAction()
            else:
                super(MainWindow.PlaylistWidget, self).dragEnterEvent(event)

        def dragMoveEvent(self, event):
            data = event.mimeData()
            urls = data.urls()
            if urls and urls[0].scheme() == 'file':
                event.acceptProposedAction()
                indexRow = self.indexAt(event.pos()).row()
                window = self.parent().parent().parent().parent().parent().parent()
                if indexRow == -1 or not window.clearedPlaylistNote:
                    indexRow = window.playlist.count()
                window.setPlaylistInsertPosition(indexRow)
            else:
                super(MainWindow.PlaylistWidget, self).dragMoveEvent(event)

        def dropEvent(self, event):
            window = self.parent().parent().parent().parent().parent().parent()
            if not window.playlist.isEnabled():
                return
            window.setPlaylistInsertPosition(None)
            if QtGui.QDropEvent.proposedAction(event) == Qt.MoveAction:
                QtGui.QDropEvent.setDropAction(event, Qt.CopyAction)  # Avoids file being deleted
            data = event.mimeData()
            urls = data.urls()

            if urls and urls[0].scheme() == 'file':
                indexRow = self.indexAt(event.pos()).row()
                if not window.clearedPlaylistNote:
                    indexRow = 0
                if indexRow == -1:
                    indexRow = window.playlist.count()
                for url in urls[::-1]:
                    if isMacOS() and IsPySide:
                        macURL = NSString.alloc().initWithString_(str(url.toString()))
                        pathString = macURL.stringByAddingPercentEscapesUsingEncoding_(NSUTF8StringEncoding)
                        dropfilepath = os.path.abspath(NSURL.URLWithString_(pathString).filePathURL().path())
                    else:
                        dropfilepath = os.path.abspath(str(url.toLocalFile()))
                    if os.path.isfile(dropfilepath):
                        window.addFileToPlaylist(dropfilepath, indexRow)
                    elif os.path.isdir(dropfilepath):
                        window.addFolderToPlaylist(dropfilepath)
            else:
                super(MainWindow.PlaylistWidget, self).dropEvent(event)

    class topSplitter(QtWidgets.QSplitter):
        def createHandle(self):
            return self.topSplitterHandle(self.orientation(), self)

        class topSplitterHandle(QtWidgets.QSplitterHandle):
            def mouseReleaseEvent(self, event):
                QtWidgets.QSplitterHandle.mouseReleaseEvent(self, event)
                self.parent().parent().parent().updateListGeometry()

            def mouseMoveEvent(self, event):
                QtWidgets.QSplitterHandle.mouseMoveEvent(self, event)
                self.parent().parent().parent().updateListGeometry()

    def needsClient(f):  # @NoSelf
        @wraps(f)
        def wrapper(self, *args, **kwds):
            if not self._syncplayClient:
                self.showDebugMessage("Tried to use client before it was ready!")
                return
            return f(self, *args, **kwds)
        return wrapper

    def fillRoomsCombobox(self):
        previousRoomSelection = self.roomsCombobox.currentText()
        self.roomsCombobox.clear()
        for roomListValue in self.config['roomList']:
            self.roomsCombobox.addItem(roomListValue)
        for room in self.currentRooms:
            if room not in self.config['roomList']:
                self.roomsCombobox.addItem(room)
        self.roomsCombobox.setEditText(previousRoomSelection)

    def addRoomToList(self, newRoom=None):
        if newRoom is None:
            newRoom = self.roomsCombobox.currentText()
        if not newRoom:
            return
        roomList = self.config['roomList']
        if newRoom not in roomList:
            roomList.append(newRoom)
        self.config['roomList'] = roomList
        roomList = sorted(roomList)
        self._syncplayClient.setRoomList(roomList)
        self.relistRoomList(roomList)

    def addClient(self, client):
        self._syncplayClient = client
        if self.console:
            self.console.addClient(client)
        self.config = self._syncplayClient.getConfig()
        self.roomsCombobox.setEditText(self._syncplayClient.getRoom())
        self.fillRoomsCombobox()
        try:
            self.playlistGroup.blockSignals(True)
            self.playlistGroup.setChecked(self.config['sharedPlaylistEnabled'])
            self.playlistGroup.blockSignals(False)
            self._syncplayClient.fileSwitch.setMediaDirectories(self.config["mediaSearchDirectories"])
            if not self.config["mediaSearchDirectories"]:
                self._syncplayClient.ui.showErrorMessage(getMessage("no-media-directories-error"))
            self.updateReadyState(self.config['readyAtStart'])
            autoplayInitialState = self.config['autoplayInitialState']
            if autoplayInitialState is not None:
                self.autoplayPushButton.blockSignals(True)
                self.autoplayPushButton.setChecked(autoplayInitialState)
                self.autoplayPushButton.blockSignals(False)
            if self.config['autoplayMinUsers'] > 1:
                self.autoplayThresholdSpinbox.blockSignals(True)
                self.autoplayThresholdSpinbox.setValue(self.config['autoplayMinUsers'])
                self.autoplayThresholdSpinbox.blockSignals(False)
            self.changeAutoplayState()
            self.changeAutoplayThreshold()
            self.updateAutoPlayIcon()
        except:
            self.showErrorMessage("Failed to load some settings.")
        self.automaticUpdateCheck()

    def promptFor(self, prompt=">", message=""):
        # TODO: Prompt user
        return None

    def setFeatures(self, featureList):
        if not featureList["readiness"]:
            self.readyPushButton.setEnabled(False)
        if not featureList["chat"]:
            self.chatFrame.setEnabled(False)
            self.chatInput.setReadOnly(True)
        if not featureList["sharedPlaylists"]:
            self.playlistGroup.setEnabled(False)
        self.chatInput.setMaxLength(constants.MAX_CHAT_MESSAGE_LENGTH)
        #self.roomsCombobox.setMaxLength(constants.MAX_ROOM_NAME_LENGTH)

    def setSSLMode(self, sslMode, sslInformation):
        self.sslMode = sslMode
        self.sslInformation = sslInformation
        self.sslButton.setVisible(sslMode)

    def getSSLInformation(self):
        return self.sslInformation

    def showMessage(self, message, noTimestamp=False):
        message = str(message)
        username = None
        messageWithUsername = re.match(constants.MESSAGE_WITH_USERNAME_REGEX, message, re.UNICODE)
        if messageWithUsername:
            username = messageWithUsername.group("username")
            message = messageWithUsername.group("message")
        message = message.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        if username:
            message = constants.STYLE_USER_MESSAGE.format(constants.STYLE_USERNAME, username, message)
        message = message.replace("\n", "<br />")
        if noTimestamp:
            self.newMessage("{}<br />".format(message))
        else:
            self.newMessage(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message + "<br />")

    @needsClient
    def getFileSwitchState(self, filename):
        if filename:
            if filename == getMessage("nofile-note"):
                return constants.FILEITEM_SWITCH_NO_SWITCH
            if self._syncplayClient.userlist.currentUser.file and utils.sameFilename(filename, self._syncplayClient.userlist.currentUser.file['name']):
                return constants.FILEITEM_SWITCH_NO_SWITCH
            if isURL(filename):
                return constants.FILEITEM_SWITCH_STREAM_SWITCH
            elif filename not in self.newWatchlist:
                if self._syncplayClient.fileSwitch.findFilepath(filename):
                    return constants.FILEITEM_SWITCH_FILE_SWITCH
                else:
                    self.newWatchlist.extend([filename])
        return constants.FILEITEM_SWITCH_NO_SWITCH

    @needsClient
    def isItemUntrusted(self, filename):
        return isURL(filename) and not self._syncplayClient.isURITrusted(filename)

    @needsClient
    def isFileAvailable(self, filename):
        if filename:
            if filename == getMessage("nofile-note"):
                return None
            if isURL(filename):
                return True
            elif filename not in self.newWatchlist:
                if self._syncplayClient.fileSwitch.findFilepath(filename):
                    return True
                else:
                    self.newWatchlist.extend([filename])
        return False

    @needsClient
    def showUserList(self, currentUser, rooms):
        self._usertreebuffer = QtGui.QStandardItemModel()
        self._usertreebuffer.setHorizontalHeaderLabels(
            (
                getMessage("roomuser-heading-label"), getMessage("size-heading-label"),
                getMessage("duration-heading-label"), getMessage("filename-heading-label")
            ))
        usertreeRoot = self._usertreebuffer.invisibleRootItem()
        if (
            self._syncplayClient.userlist.currentUser.file and
            self._syncplayClient.userlist.currentUser.file and
            os.path.isfile(self._syncplayClient.userlist.currentUser.file["path"])
        ):
            self._syncplayClient.fileSwitch.setCurrentDirectory(os.path.dirname(self._syncplayClient.userlist.currentUser.file["path"]))

        self.currentRooms = []
        for room in rooms:
            self.currentRooms.append(room)
            if self.hideEmptyRooms:
                foundEmptyRooms = False
                for user in rooms[room]:
                    if user.username.strip() == "":
                        foundEmptyRooms = True
                if foundEmptyRooms:
                    continue
            self.newWatchlist = []
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
                    roomitem.setIcon(QtGui.QPixmap(resourcespath + 'lock_open.png'))
                else:
                    roomitem.setIcon(QtGui.QPixmap(resourcespath + 'lock.png'))
            else:
                roomitem.setIcon(QtGui.QPixmap(resourcespath + 'chevrons_right.png'))

            for user in rooms[room]:
                if user.username.strip() == "":
                    continue
                useritem = QtGui.QStandardItem(user.username)
                isController = user.isController()
                sameRoom = room == currentUser.room
                if sameRoom:
                    isReadyWithFile = user.isReadyWithFile()
                else:
                    isReadyWithFile = None
                useritem.setData(isController, Qt.UserRole + constants.USERITEM_CONTROLLER_ROLE)
                useritem.setData(isReadyWithFile, Qt.UserRole + constants.USERITEM_READY_ROLE)
                if user.file:
                    filesizeitem = QtGui.QStandardItem(formatSize(user.file['size']))
                    filedurationitem = QtGui.QStandardItem("({})".format(formatTime(user.file['duration'])))
                    filename = user.file['name']
                    if isURL(filename):
                        filename = urllib.parse.unquote(filename)
                    filenameitem = QtGui.QStandardItem(filename)
                    fileSwitchState = self.getFileSwitchState(user.file['name']) if room == currentUser.room else None
                    if fileSwitchState != constants.FILEITEM_SWITCH_NO_SWITCH:
                        filenameTooltip = getMessage("switch-to-file-tooltip").format(filename)
                    else:
                        filenameTooltip = filename
                    filenameitem.setToolTip(filenameTooltip)
                    filenameitem.setData(fileSwitchState, Qt.UserRole + constants.FILEITEM_SWITCH_ROLE)
                    if currentUser.file:
                        sameName = sameFilename(user.file['name'], currentUser.file['name'])
                        sameSize = sameFilesize(user.file['size'], currentUser.file['size'])
                        sameDuration = sameFileduration(user.file['duration'], currentUser.file['duration'])
                        underlinefont = QtGui.QFont()
                        underlinefont.setUnderline(True)
                        differentItemColor = constants.STYLE_DARK_DIFFERENTITEM_COLOR if isDarkMode else constants.STYLE_DIFFERENTITEM_COLOR
                        if sameRoom:
                            if not sameName:
                                filenameitem.setForeground(QtGui.QBrush(QtGui.QColor(differentItemColor)))
                                filenameitem.setFont(underlinefont)
                            if not sameSize:
                                if formatSize(user.file['size']) == formatSize(currentUser.file['size']):
                                    filesizeitem = QtGui.QStandardItem(formatSize(user.file['size'], precise=True))
                                filesizeitem.setFont(underlinefont)
                                filesizeitem.setForeground(QtGui.QBrush(QtGui.QColor(differentItemColor)))
                            if not sameDuration:
                                filedurationitem.setForeground(QtGui.QBrush(QtGui.QColor(differentItemColor)))
                                filedurationitem.setFont(underlinefont)
                else:
                    filenameitem = QtGui.QStandardItem(getMessage("nofile-note"))
                    filedurationitem = QtGui.QStandardItem("")
                    filesizeitem = QtGui.QStandardItem("")
                    if room == currentUser.room:
                        if isDarkMode:
                            filenameitem.setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_DARK_NOFILEITEM_COLOR)))
                        else:
                            filenameitem.setForeground(QtGui.QBrush(QtGui.QColor(constants.STYLE_NOFILEITEM_COLOR)))
                font = QtGui.QFont()
                if currentUser.username == user.username:
                    font.setWeight(QtGui.QFont.Bold)
                    self.updateReadyState(currentUser.isReadyWithFile())
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
        self.listTreeView.setItemDelegate(UserlistItemDelegate(view=self.listTreeView))
        self.listTreeView.setItemsExpandable(False)
        self.listTreeView.setRootIsDecorated(False)
        self.listTreeView.expandAll()
        self.updateListGeometry()
        self._syncplayClient.fileSwitch.setFilenameWatchlist(self.newWatchlist)
        self.fillRoomsCombobox()

    @needsClient
    def undoPlaylistChange(self):
        self._syncplayClient.playlist.undoPlaylistChange()

    @needsClient
    def shuffleRemainingPlaylist(self):
        self._syncplayClient.playlist.shuffleRemainingPlaylist()

    @needsClient
    def shuffleEntirePlaylist(self):
        self._syncplayClient.playlist.shuffleEntirePlaylist()

    @needsClient
    def openPlaylistMenu(self, position):
        indexes = self.playlist.selectedIndexes()
        if len(indexes) > 0:
            item = self.playlist.selectedIndexes()[0]
        else:
            item = None
        menu = QtWidgets.QMenu()

        if item:
            firstFile = item.sibling(item.row(), 0).data()
            pathFound = self._syncplayClient.fileSwitch.findFilepath(firstFile) if not isURL(firstFile) else None
            if self._syncplayClient.userlist.currentUser.file is None or firstFile != self._syncplayClient.userlist.currentUser.file["name"]:
                if isURL(firstFile):
                    menu.addAction(QtGui.QPixmap(resourcespath + "world_go.png"), getMessage("openstreamurl-menu-label"), lambda: self.openFile(firstFile, resetPosition=True, fromUser=True))
                elif pathFound:
                        menu.addAction(QtGui.QPixmap(resourcespath + "film_go.png"), getMessage("openmedia-menu-label"), lambda: self.openFile(pathFound, resetPosition=True, fromUser=True))
            if pathFound:
                menu.addAction(QtGui.QPixmap(resourcespath + "folder_film.png"),
                               getMessage('open-containing-folder'),
                               lambda: utils.open_system_file_browser(pathFound))
            if self._syncplayClient.isUntrustedTrustableURI(firstFile):
                domain = utils.getDomainFromURL(firstFile)
                if domain:
                    menu.addAction(QtGui.QPixmap(resourcespath + "shield_add.png"), getMessage("addtrusteddomain-menu-label").format(domain), lambda: self.addTrustedDomain(domain))
            menu.addAction(QtGui.QPixmap(resourcespath + "delete.png"), getMessage("removefromplaylist-menu-label"), lambda: self.deleteSelectedPlaylistItems())
            menu.addSeparator()
        menu.addAction(QtGui.QPixmap(resourcespath + "arrow_switch.png"), getMessage("shuffleremainingplaylist-menu-label"), lambda: self.shuffleRemainingPlaylist())
        menu.addAction(QtGui.QPixmap(resourcespath + "arrow_switch.png"), getMessage("shuffleentireplaylist-menu-label"), lambda: self.shuffleEntirePlaylist())
        menu.addAction(QtGui.QPixmap(resourcespath + "arrow_undo.png"), getMessage("undoplaylist-menu-label"), lambda: self.undoPlaylistChange())
        menu.addAction(QtGui.QPixmap(resourcespath + "film_edit.png"), getMessage("editplaylist-menu-label"), lambda: self.openEditPlaylistDialog())
        menu.addAction(QtGui.QPixmap(resourcespath + "film_add.png"), getMessage("addfilestoplaylist-menu-label"), lambda: self.OpenAddFilesToPlaylistDialog())
        menu.addAction(QtGui.QPixmap(resourcespath + "world_add.png"), getMessage("addurlstoplaylist-menu-label"), lambda: self.OpenAddURIsToPlaylistDialog())
        menu.addSeparator()
        menu.addAction(getMessage("loadplaylistfromfile-menu-label"),lambda: self.OpenLoadPlaylistFromFileDialog()) # TODO: Add icon
        menu.addAction("Load and shuffle playlist from file",lambda: self.OpenLoadPlaylistFromFileDialog(shuffle=True))  # TODO: Add icon and messages_en
        menu.addAction(getMessage("saveplaylisttofile-menu-label"),lambda: self.OpenSavePlaylistToFileDialog()) # TODO: Add icon
        menu.addSeparator()
        menu.addAction(QtGui.QPixmap(resourcespath + "film_folder_edit.png"), getMessage("setmediadirectories-menu-label"), lambda: self.openSetMediaDirectoriesDialog())
        menu.addAction(QtGui.QPixmap(resourcespath + "shield_edit.png"), getMessage("settrusteddomains-menu-label"), lambda: self.openSetTrustedDomainsDialog())
        menu.exec_(self.playlist.viewport().mapToGlobal(position))

    def openRoomMenu(self, position):
        # TODO: Deselect items after right click
        indexes = self.listTreeView.selectedIndexes()
        if len(indexes) > 0:
            item = self.listTreeView.selectedIndexes()[0]
        else:
            return

        menu = QtWidgets.QMenu()
        username = item.sibling(item.row(), 0).data()

        if len(username) < 15:
            shortUsername = username
        else:
            shortUsername = "{}...".format(username[0:12])

        if username == self._syncplayClient.userlist.currentUser.username:
            addUsersFileToPlaylistLabelText = getMessage("addyourfiletoplaylist-menu-label")
            addUsersStreamToPlaylistLabelText = getMessage("addyourstreamstoplaylist-menu-label")
        else:
            addUsersFileToPlaylistLabelText = getMessage("addotherusersfiletoplaylist-menu-label").format(shortUsername)
            addUsersStreamToPlaylistLabelText = getMessage("addotherusersstreamstoplaylist-menu-label").format(shortUsername)

        filename = item.sibling(item.row(), 3).data()
        while item.parent().row() != -1:
            item = item.parent()
        roomToJoin = item.sibling(item.row(), 0).data()
        if roomToJoin != self._syncplayClient.getRoom():
            menu.addAction(getMessage("joinroom-menu-label").format(roomToJoin), lambda: self.joinRoom(roomToJoin))
        elif username and filename and filename != getMessage("nofile-note"):
            if self.config['sharedPlaylistEnabled'] and not self.isItemInPlaylist(filename):
                if isURL(filename):
                    menu.addAction(QtGui.QPixmap(resourcespath + "world_add.png"), addUsersStreamToPlaylistLabelText, lambda: self.addStreamToPlaylist(filename))
                else:
                    menu.addAction(QtGui.QPixmap(resourcespath + "film_add.png"), addUsersFileToPlaylistLabelText, lambda: self.addStreamToPlaylist(filename))

            if self._syncplayClient.userlist.currentUser.file is None or filename != self._syncplayClient.userlist.currentUser.file["name"]:
                if isURL(filename):
                    menu.addAction(QtGui.QPixmap(resourcespath + "world_go.png"), getMessage("openusersstream-menu-label").format(shortUsername), lambda: self.openFile(filename, resetPosition=False, fromUser=True))
                else:
                    pathFound = self._syncplayClient.fileSwitch.findFilepath(filename)
                    if pathFound:
                        menu.addAction(QtGui.QPixmap(resourcespath + "film_go.png"), getMessage("openusersfile-menu-label").format(shortUsername), lambda: self.openFile(pathFound, resetPosition=False, fromUser=True))
            if self._syncplayClient.isUntrustedTrustableURI(filename):
                domain = utils.getDomainFromURL(filename)
                if domain:
                    menu.addAction(QtGui.QPixmap(resourcespath + "shield_add.png"), getMessage("addtrusteddomain-menu-label").format(domain), lambda: self.addTrustedDomain(domain))

            if not isURL(filename) and filename != getMessage("nofile-note"):
                path = self._syncplayClient.fileSwitch.findFilepath(filename)
                if path:
                    menu.addAction(QtGui.QPixmap(resourcespath + "folder_film.png"), getMessage('open-containing-folder'), lambda: utils.open_system_file_browser(path))
        else:
            return
        menu.exec_(self.listTreeView.viewport().mapToGlobal(position))

    def updateListGeometry(self):
        try:
            roomtocheck = 0
            while self.listTreeModel.item(roomtocheck):
                self.listTreeView.setFirstColumnSpanned(roomtocheck, self.listTreeView.rootIndex(), True)
                roomtocheck += 1
            self.listTreeView.header().setStretchLastSection(False)
            if IsPySide6 or IsPySide2:
                self.listTreeView.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
                self.listTreeView.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                self.listTreeView.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                self.listTreeView.header().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            if IsPySide:
                self.listTreeView.header().setResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
                self.listTreeView.header().setResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                self.listTreeView.header().setResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                self.listTreeView.header().setResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            NarrowTabsWidth = self.listTreeView.header().sectionSize(0)+self.listTreeView.header().sectionSize(1)+self.listTreeView.header().sectionSize(2)
            if self.listTreeView.header().width() < (NarrowTabsWidth+self.listTreeView.header().sectionSize(3)):
                self.listTreeView.header().resizeSection(3, self.listTreeView.header().width()-NarrowTabsWidth)
            else:
                if IsPySide6 or IsPySide2:
                    self.listTreeView.header().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
                if IsPySide:
                    self.listTreeView.header().setResizeMode(3, QtWidgets.QHeaderView.Stretch)
            self.listTreeView.expandAll()
        except:
            pass

    def updateReadyState(self, newState):
        oldState = self.readyPushButton.isChecked()
        if newState != oldState and newState is not None:
            self.readyPushButton.blockSignals(True)
            self.readyPushButton.setChecked(newState)
            self.readyPushButton.blockSignals(False)
        self.updateReadyIcon()

    @needsClient
    def playlistItemClicked(self, item):
        # TODO: Integrate into client.py code
        filename = item.data()
        if self._isTryingToChangeToCurrentFile(filename):
            return
        if isURL(filename):
            self._syncplayClient.openFile(filename, resetPosition=True)
        else:
            pathFound = self._syncplayClient.fileSwitch.findFilepath(filename, highPriority=True)
            if pathFound:
                self._syncplayClient.openFile(pathFound, resetPosition=True)
            else:
                self._syncplayClient.ui.showErrorMessage(getMessage("cannot-find-file-for-playlist-switch-error").format(filename))

    def _isTryingToChangeToCurrentFile(self, filename):
        if self._syncplayClient.userlist.currentUser.file and filename == self._syncplayClient.userlist.currentUser.file["name"]:
            self.showDebugMessage("File change request ignored (Syncplay should not be asked to change to current filename)")
            return True
        else:
            return False

    def roomClicked(self, item):
        username = item.sibling(item.row(), 0).data()
        filename = item.sibling(item.row(), 3).data()
        while item.parent().row() != -1:
            item = item.parent()
        roomToJoin = item.sibling(item.row(), 0).data()
        if roomToJoin != self._syncplayClient.getRoom():
            self.joinRoom(item.sibling(item.row(), 0).data())
        elif username and filename and username != self._syncplayClient.userlist.currentUser.username:
            if self._isTryingToChangeToCurrentFile(filename):
                return
            if isURL(filename):
                self._syncplayClient.openFile(filename)
            else:
                pathFound = self._syncplayClient.fileSwitch.findFilepath(filename, highPriority=True)
                if pathFound:
                    self._syncplayClient.openFile(pathFound)
                else:
                    self._syncplayClient.fileSwitch.updateInfo()
                    self.showErrorMessage(getMessage("switch-file-not-found-error").format(filename))

    @needsClient
    def userListChange(self):
        self._syncplayClient.showUserList()

    def fileSwitchFoundFiles(self):
        self._syncplayClient.showUserList()
        self.playlist.updatePlaylistIndexIcon()

    def updateRoomName(self, room=""):
        self.roomsCombobox.setEditText(room)
        try:
            if self.config['autosaveJoinsToList']:
                self.addRoomToList(room)
        except:
            pass

    def showDebugMessage(self, message):
        print(message)

    def showErrorMessage(self, message, criticalerror=False):
        message = str(message)
        if criticalerror:
            QtWidgets.QMessageBox.critical(self, "Syncplay", message)
        message = message.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        message = message.replace("&lt;a href=&quot;https://syncplay.pl/trouble&quot;&gt;", '<a href="https://syncplay.pl/trouble">').replace("&lt;/a&gt;", "</a>")
        message = message.replace("&lt;a href=&quot;https://mpv.io/&quot;&gt;", '<a href="https://mpv.io/">').replace("&lt;/a&gt;", "</a>")
        message = message.replace("&lt;a href=&quot;https://github.com/stax76/mpv.net/&quot;&gt;", '<a href="https://github.com/stax76/mpv.net/">').replace("&lt;/a&gt;", "</a>")
        message = message.replace("\n", "<br />")
        if isDarkMode:
            message = "<span style=\"{}\">".format(constants.STYLE_DARK_ERRORNOTIFICATION) + message + "</span>"
        else:
            message = "<span style=\"{}\">".format(constants.STYLE_ERRORNOTIFICATION) + message + "</span>"
        self.newMessage(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message + "<br />")

    @needsClient
    def joinRoom(self, room=None):
        if room is None:
            room = self.roomsCombobox.currentText()
        if room == "":
            if self._syncplayClient.userlist.currentUser.file:
                room = self._syncplayClient.userlist.currentUser.file["name"]
            else:
                room = self._syncplayClient.defaultRoom
        self.roomsCombobox.setEditText(room)
        if room != self._syncplayClient.getRoom():
            self._syncplayClient.setRoom(room, resetAutoplay=True)
            self._syncplayClient.sendRoom()
            if self.config['autosaveJoinsToList']:
                self.addRoomToList(room)

    def seekPositionDialog(self):
        seekTime, ok = QtWidgets.QInputDialog.getText(
            self, getMessage("seektime-menu-label"),
            getMessage("seektime-msgbox-label"), QtWidgets.QLineEdit.Normal,
            "0:00")
        if ok and seekTime != '':
            self.seekPosition(seekTime)

    def seekFromButton(self):
        self.seekPosition(self.seekInput.text())

    @needsClient
    def seekPosition(self, seekTime):
        s = re.match(constants.UI_SEEK_REGEX, seekTime)
        if s:
            sign = self._extractSign(s.group('sign'))
            t = utils.parseTime(s.group('time'))
            if t is None:
                return
            if sign:
                t = self._syncplayClient.getGlobalPosition() + sign * t
            self._syncplayClient.setPosition(t)
        else:
            self.showErrorMessage(getMessage("invalid-seek-value"))

    @needsClient
    def undoSeek(self):
        tmp_pos = self._syncplayClient.getPlayerPosition()
        self._syncplayClient.setPosition(self._syncplayClient.playerPositionBeforeLastSeek)
        self._syncplayClient.playerPositionBeforeLastSeek = tmp_pos

    @needsClient
    def togglePause(self):
        self._syncplayClient.setPaused(not self._syncplayClient.getPlayerPaused())

    @needsClient
    def play(self):
        self._syncplayClient.setPaused(False)

    @needsClient
    def pause(self):
        self._syncplayClient.setPaused(True)

    @needsClient
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

    def getInitialMediaDirectory(self, includeUserSpecifiedDirectories=True):
        if IsPySide:
            if self.config["mediaSearchDirectories"] and os.path.isdir(self.config["mediaSearchDirectories"][0]) and includeUserSpecifiedDirectories:
                defaultdirectory = self.config["mediaSearchDirectories"][0]
            elif includeUserSpecifiedDirectories and os.path.isdir(self.mediadirectory):
                defaultdirectory = self.mediadirectory
            elif os.path.isdir(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MoviesLocation)):
                defaultdirectory = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MoviesLocation)
            elif os.path.isdir(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)):
                defaultdirectory = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)
            else:
                defaultdirectory = ""
        elif IsPySide6 or IsPySide2:
            if self.config["mediaSearchDirectories"] and os.path.isdir(self.config["mediaSearchDirectories"][0]) and includeUserSpecifiedDirectories:
                defaultdirectory = self.config["mediaSearchDirectories"][0]
            elif includeUserSpecifiedDirectories and os.path.isdir(self.mediadirectory):
                defaultdirectory = self.mediadirectory
            elif os.path.isdir(QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)[0]):
                defaultdirectory = QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)[0]
            elif os.path.isdir(QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]):
                defaultdirectory = QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]
            else:
                defaultdirectory = ""
        return defaultdirectory

    @needsClient
    def browseMediapath(self):
        if self._syncplayClient._player.customOpenDialog == True:
            self._syncplayClient._player.openCustomOpenDialog()
            return

        self.loadMediaBrowseSettings()
        if isMacOS() and IsPySide:
            options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.DontUseNativeDialog)
        else:
            options = QtWidgets.QFileDialog.Options()
        self.mediadirectory = ""
        currentdirectory = os.path.dirname(self._syncplayClient.userlist.currentUser.file["path"]) if self._syncplayClient.userlist.currentUser.file else None
        if currentdirectory and os.path.isdir(currentdirectory):
            defaultdirectory = currentdirectory
        else:
            defaultdirectory = self.getInitialMediaDirectory()
        browserfilter = "All files (*)"
        fileName, filtr = QtWidgets.QFileDialog.getOpenFileName(
            self, getMessage("browseformedia-label"), defaultdirectory,
            browserfilter, "", options)
        if fileName:
            if isWindows():
                fileName = fileName.replace("/", "\\")
            self.mediadirectory = os.path.dirname(fileName)
            self._syncplayClient.fileSwitch.setCurrentDirectory(self.mediadirectory)
            self.saveMediaBrowseSettings()
            self._syncplayClient.openFile(fileName, resetPosition=False, fromUser=True)

    @needsClient
    def OpenAddFilesToPlaylistDialog(self):
        if self._syncplayClient._player.customOpenDialog == True:
            self._syncplayClient._player.openCustomOpenDialog()
            return

        self.loadMediaBrowseSettings()
        if isMacOS() and IsPySide:
            options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.DontUseNativeDialog)
        else:
            options = QtWidgets.QFileDialog.Options()
        self.mediadirectory = ""
        currentdirectory = os.path.dirname(self._syncplayClient.userlist.currentUser.file["path"]) if self._syncplayClient.userlist.currentUser.file else None
        if currentdirectory and os.path.isdir(currentdirectory):
            defaultdirectory = currentdirectory
        else:
            defaultdirectory = self.getInitialMediaDirectory()
        browserfilter = "All files (*)"
        fileNames, filtr = QtWidgets.QFileDialog.getOpenFileNames(
            self, getMessage("browseformedia-label"), defaultdirectory,
            browserfilter, "", options)
        self.updatingPlaylist = True
        if fileNames:
            for fileName in fileNames:
                if isWindows():
                    fileName = fileName.replace("/", "\\")
                self.mediadirectory = os.path.dirname(fileName)
                self._syncplayClient.fileSwitch.setCurrentDirectory(self.mediadirectory)
                self.saveMediaBrowseSettings()
                self.addFileToPlaylist(fileName)
        self.updatingPlaylist = False
        self.playlist.updatePlaylist(self.getPlaylistState())

    @needsClient
    def OpenLoadPlaylistFromFileDialog(self, shuffle=False):
        self.loadMediaBrowseSettings()
        if isMacOS() and IsPySide:
            options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.DontUseNativeDialog)
        else:
            options = QtWidgets.QFileDialog.Options()
        self.mediadirectory = ""
        currentdirectory = os.path.dirname(self._syncplayClient.userlist.currentUser.file["path"]) if self._syncplayClient.userlist.currentUser.file else None
        if currentdirectory and os.path.isdir(currentdirectory):
            defaultdirectory = currentdirectory
        else:
            defaultdirectory = self.getInitialMediaDirectory()
        browserfilter = "Playlists (*.txt *.m3u8)"
        filepath, filtr = QtWidgets.QFileDialog.getOpenFileName(
            self, "Load playlist from file", defaultdirectory,
            browserfilter, "", options) # TODO: Note Shuffle and move to messages_en
        if os.path.isfile(filepath):
            self._syncplayClient.playlist.loadPlaylistFromFile(filepath, shuffle=shuffle)
            self.playlist.updatePlaylist(self.getPlaylistState())

    @needsClient
    def OpenSavePlaylistToFileDialog(self):
        self.loadMediaBrowseSettings()
        if isMacOS() and IsPySide:
            options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.DontUseNativeDialog)
        else:
            options = QtWidgets.QFileDialog.Options()
        self.mediadirectory = ""
        currentdirectory = os.path.dirname(self._syncplayClient.userlist.currentUser.file["path"]) if self._syncplayClient.userlist.currentUser.file else None
        if currentdirectory and os.path.isdir(currentdirectory):
            defaultdirectory = currentdirectory
        else:
            defaultdirectory = self.getInitialMediaDirectory()
        browserfilter = "Playlist (*.txt)"
        filepath, filtr = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save playlist to file", defaultdirectory,
            browserfilter, "", options) # TODO: Move to messages_en
        if filepath:
            self._syncplayClient.playlist.savePlaylistToFile(filepath)

    @needsClient
    def OpenAddURIsToPlaylistDialog(self):
        URIsDialog = QtWidgets.QDialog()
        URIsDialog.setWindowTitle(getMessage("adduris-msgbox-label"))
        URIsLayout = QtWidgets.QGridLayout()
        URIsLabel = QtWidgets.QLabel(getMessage("adduris-msgbox-label"))
        URIsLayout.addWidget(URIsLabel, 0, 0, 1, 1)
        URIsTextbox = QtWidgets.QPlainTextEdit()
        URIsTextbox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        URIsLayout.addWidget(URIsTextbox, 1, 0, 1, 1)
        URIsButtonBox = QtWidgets.QDialogButtonBox()
        URIsButtonBox.setOrientation(Qt.Horizontal)
        URIsButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        URIsButtonBox.accepted.connect(URIsDialog.accept)
        URIsButtonBox.rejected.connect(URIsDialog.reject)
        URIsLayout.addWidget(URIsButtonBox, 2, 0, 1, 1)
        URIsDialog.setLayout(URIsLayout)
        URIsDialog.setModal(True)
        URIsDialog.setWindowFlags(URIsDialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        URIsDialog.show()
        result = URIsDialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            URIsToAdd = utils.convertMultilineStringToList(URIsTextbox.toPlainText())
            self.updatingPlaylist = True
            for URI in URIsToAdd:
                URI = URI.rstrip()
                URI = urllib.parse.unquote(URI)
                if URI != "":
                    self.addStreamToPlaylist(URI)
            self.updatingPlaylist = False

    def openEditRoomsDialog(self):
        RoomsDialog = QtWidgets.QDialog()
        RoomsLayout = QtWidgets.QGridLayout()
        RoomsTextbox = QtWidgets.QPlainTextEdit()
        RoomsDialog.setWindowTitle(getMessage("roomlist-msgbox-label"))
        RoomsPlaylistLabel = QtWidgets.QLabel(getMessage("roomlist-msgbox-label"))
        RoomsTextbox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        RoomsTextbox.setPlainText(utils.getListAsMultilineString(self.config['roomList']))
        RoomsLayout.addWidget(RoomsPlaylistLabel, 0, 0, 1, 1)
        RoomsLayout.addWidget(RoomsTextbox, 1, 0, 1, 1)
        RoomsButtonBox = QtWidgets.QDialogButtonBox()
        RoomsButtonBox.setOrientation(Qt.Horizontal)
        RoomsButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        RoomsButtonBox.accepted.connect(RoomsDialog.accept)
        RoomsButtonBox.rejected.connect(RoomsDialog.reject)
        RoomsLayout.addWidget(RoomsButtonBox, 2, 0, 1, 1)
        RoomsDialog.setLayout(RoomsLayout)
        RoomsDialog.setModal(True)
        RoomsDialog.setWindowFlags(RoomsDialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        RoomsDialog.show()
        result = RoomsDialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            newRooms = utils.convertMultilineStringToList(RoomsTextbox.toPlainText())
            newRooms = sorted(newRooms)
            self.relistRoomList(newRooms)
            self._syncplayClient.setRoomList(newRooms)

    def relistRoomList(self, newRooms):
        filteredNewRooms = [room for room in newRooms if room and not room.isspace()]
        self.config['roomList'] = filteredNewRooms
        self.fillRoomsCombobox()

    @needsClient
    def openEditPlaylistDialog(self):
        oldPlaylist = utils.getListAsMultilineString(self.getPlaylistState())
        editPlaylistDialog = QtWidgets.QDialog()
        editPlaylistDialog.setWindowTitle(getMessage("editplaylist-msgbox-label"))
        editPlaylistLayout = QtWidgets.QGridLayout()
        editPlaylistLabel = QtWidgets.QLabel(getMessage("editplaylist-msgbox-label"))
        editPlaylistLayout.addWidget(editPlaylistLabel, 0, 0, 1, 1)
        editPlaylistTextbox = QtWidgets.QPlainTextEdit(oldPlaylist)
        editPlaylistTextbox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        editPlaylistLayout.addWidget(editPlaylistTextbox, 1, 0, 1, 1)
        editPlaylistButtonBox = QtWidgets.QDialogButtonBox()
        editPlaylistButtonBox.setOrientation(Qt.Horizontal)
        editPlaylistButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        editPlaylistButtonBox.accepted.connect(editPlaylistDialog.accept)
        editPlaylistButtonBox.rejected.connect(editPlaylistDialog.reject)
        editPlaylistLayout.addWidget(editPlaylistButtonBox, 2, 0, 1, 1)
        editPlaylistDialog.setLayout(editPlaylistLayout)
        editPlaylistDialog.setModal(True)
        editPlaylistDialog.setMinimumWidth(600)
        editPlaylistDialog.setMinimumHeight(500)
        editPlaylistDialog.setWindowFlags(editPlaylistDialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        editPlaylistDialog.show()
        result = editPlaylistDialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            newPlaylist = utils.convertMultilineStringToList(editPlaylistTextbox.toPlainText())
            if newPlaylist != self.playlistState and self._syncplayClient and not self.updatingPlaylist:
                self.setPlaylist(newPlaylist)
                self._syncplayClient.playlist.changePlaylist(newPlaylist)
                self._syncplayClient.fileSwitch.updateInfo()

    @needsClient
    def openSetMediaDirectoriesDialog(self):
        MediaDirectoriesDialog = QtWidgets.QDialog()
        MediaDirectoriesDialog.setWindowTitle(getMessage("syncplay-mediasearchdirectories-title"))  # TODO: Move to messages_*.py
        MediaDirectoriesLayout = QtWidgets.QGridLayout()
        MediaDirectoriesLabel = QtWidgets.QLabel(getMessage("syncplay-mediasearchdirectories-label"))
        MediaDirectoriesLayout.addWidget(MediaDirectoriesLabel, 0, 0, 1, 2)
        MediaDirectoriesTextbox = QtWidgets.QPlainTextEdit()
        MediaDirectoriesTextbox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        MediaDirectoriesTextbox.setPlainText(utils.getListAsMultilineString(self.config["mediaSearchDirectories"]))
        MediaDirectoriesLayout.addWidget(MediaDirectoriesTextbox, 1, 0, 1, 1)
        MediaDirectoriesButtonBox = QtWidgets.QDialogButtonBox()
        MediaDirectoriesButtonBox.setOrientation(Qt.Horizontal)
        MediaDirectoriesButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        MediaDirectoriesButtonBox.accepted.connect(MediaDirectoriesDialog.accept)
        MediaDirectoriesButtonBox.rejected.connect(MediaDirectoriesDialog.reject)
        MediaDirectoriesLayout.addWidget(MediaDirectoriesButtonBox, 2, 0, 1, 1)
        MediaDirectoriesAddFolderButton = QtWidgets.QPushButton(getMessage("addfolder-label"))
        MediaDirectoriesAddFolderButton.pressed.connect(lambda: self.openAddMediaDirectoryDialog(MediaDirectoriesTextbox, MediaDirectoriesDialog))
        MediaDirectoriesLayout.addWidget(MediaDirectoriesAddFolderButton, 1, 1, 1, 1, Qt.AlignTop)
        MediaDirectoriesDialog.setLayout(MediaDirectoriesLayout)
        MediaDirectoriesDialog.setWindowFlags(MediaDirectoriesDialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        MediaDirectoriesDialog.setModal(True)
        MediaDirectoriesDialog.show()
        result = MediaDirectoriesDialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            newMediaDirectories = utils.convertMultilineStringToList(MediaDirectoriesTextbox.toPlainText())
            self._syncplayClient.fileSwitch.changeMediaDirectories(newMediaDirectories)

    @needsClient
    def openSetTrustedDomainsDialog(self):
        TrustedDomainsDialog = QtWidgets.QDialog()
        TrustedDomainsDialog.setWindowTitle(getMessage("syncplay-trusteddomains-title"))
        TrustedDomainsLayout = QtWidgets.QGridLayout()
        TrustedDomainsLabel = QtWidgets.QLabel(getMessage("trusteddomains-msgbox-label"))
        TrustedDomainsLayout.addWidget(TrustedDomainsLabel, 0, 0, 1, 1)
        TrustedDomainsTextbox = QtWidgets.QPlainTextEdit()
        TrustedDomainsTextbox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        TrustedDomainsTextbox.setPlainText(utils.getListAsMultilineString(self.config["trustedDomains"]))
        TrustedDomainsLayout.addWidget(TrustedDomainsTextbox, 1, 0, 1, 1)
        TrustedDomainsButtonBox = QtWidgets.QDialogButtonBox()
        TrustedDomainsButtonBox.setOrientation(Qt.Horizontal)
        TrustedDomainsButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        TrustedDomainsButtonBox.accepted.connect(TrustedDomainsDialog.accept)
        TrustedDomainsButtonBox.rejected.connect(TrustedDomainsDialog.reject)
        TrustedDomainsLayout.addWidget(TrustedDomainsButtonBox, 2, 0, 1, 1)
        TrustedDomainsDialog.setLayout(TrustedDomainsLayout)
        TrustedDomainsDialog.setWindowFlags(TrustedDomainsDialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        TrustedDomainsDialog.setModal(True)
        TrustedDomainsDialog.show()
        result = TrustedDomainsDialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            newTrustedDomains = utils.convertMultilineStringToList(TrustedDomainsTextbox.toPlainText())
            self._syncplayClient.setTrustedDomains(newTrustedDomains)

    @needsClient
    def addTrustedDomain(self, newDomain):
        trustedDomains = self.config["trustedDomains"][:]
        if newDomain:
            trustedDomains.append(newDomain)
            self._syncplayClient.setTrustedDomains(trustedDomains)

    @needsClient
    def openAddMediaDirectoryDialog(self, MediaDirectoriesTextbox, MediaDirectoriesDialog):
        if isMacOS() and IsPySide:
            options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontUseNativeDialog)
        else:
            options = QtWidgets.QFileDialog.Options(QtWidgets.QFileDialog.ShowDirsOnly)
        folderName = str(QtWidgets.QFileDialog.getExistingDirectory(
            self, None, self.getInitialMediaDirectory(includeUserSpecifiedDirectories=False), options))

        if folderName:
            existingMediaDirs = MediaDirectoriesTextbox.toPlainText()
            if existingMediaDirs == "":
                newMediaDirList = folderName
            else:
                newMediaDirList = existingMediaDirs + "\n" + folderName
            MediaDirectoriesTextbox.setPlainText(newMediaDirList)
        MediaDirectoriesDialog.raise_()
        MediaDirectoriesDialog.activateWindow()

    @needsClient
    def promptForStreamURL(self):
        streamURL, ok = QtWidgets.QInputDialog.getText(
            self, getMessage("promptforstreamurl-msgbox-label"),
            getMessage("promptforstreamurlinfo-msgbox-label"), QtWidgets.QLineEdit.Normal, "")
        if ok and streamURL != '':
            self._syncplayClient.openFile(streamURL, resetPosition=False, fromUser=True)

    @needsClient
    def createControlledRoom(self):
        controlroom, ok = QtWidgets.QInputDialog.getText(
            self, getMessage("createcontrolledroom-msgbox-label"),
            getMessage("controlledroominfo-msgbox-label"), QtWidgets.QLineEdit.Normal,
            utils.stripRoomName(self._syncplayClient.getRoom()))
        if ok and controlroom != '':
            self._syncplayClient.createControlledRoom(controlroom)

    @needsClient
    def identifyAsController(self):
        msgboxtitle = getMessage("identifyascontroller-msgbox-label")
        msgboxtext = getMessage("identifyinfo-msgbox-label")
        controlpassword, ok = QtWidgets.QInputDialog.getText(self, msgboxtitle, msgboxtext, QtWidgets.QLineEdit.Normal, "")
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

    @needsClient
    def setOffset(self):
        newoffset, ok = QtWidgets.QInputDialog.getText(
            self, getMessage("setoffset-msgbox-label"),
            getMessage("offsetinfo-msgbox-label"), QtWidgets.QLineEdit.Normal, "")
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
                self.showErrorMessage(getMessage("invalid-offset-value"))

    def openUserGuide(self):
        if isLinux():
            self.QtGui.QDesktopServices.openUrl(QUrl("https://syncplay.pl/guide/linux/"))
        elif isWindows():
            self.QtGui.QDesktopServices.openUrl(QUrl("https://syncplay.pl/guide/windows/"))
        else:
            self.QtGui.QDesktopServices.openUrl(QUrl("https://syncplay.pl/guide/"))

    def drop(self):
        self.close()

    def getPlaylistState(self):
        playlistItems = []
        for playlistItem in range(self.playlist.count()):
            playlistItemText = self.playlist.item(playlistItem).text()
            if playlistItemText != getMessage("playlist-instruction-item-message"):
                playlistItems.append(playlistItemText)
        return playlistItems

    def playlistChangeCheck(self):
        if self.updatingPlaylist:
            return
        newPlaylist = self.getPlaylistState()
        if newPlaylist != self.playlistState and self._syncplayClient and not self.updatingPlaylist:
            self.playlistState = newPlaylist
            self._syncplayClient.playlist.changePlaylist(newPlaylist)
            self._syncplayClient.fileSwitch.updateInfo()

    def executeCommand(self, command):
        self.showMessage("/{}".format(command))
        self.console.executeCommand(command)

    def sendChatMessage(self):
        chatText = self.chatInput.text()
        self.chatInput.setText("")
        if chatText != "":
            if chatText[:1] == "/" and chatText != "/":
                command = chatText[1:]
                if command and command[:1] == "/":
                    chatText = chatText[1:]
                else:
                    self.executeCommand(command)
                    return
            self._syncplayClient.sendChat(chatText)

    def addTopLayout(self, window):
        window.topSplit = self.topSplitter(Qt.Horizontal, self)

        window.outputLayout = QtWidgets.QVBoxLayout()
        window.outputbox = QtWidgets.QTextBrowser()
        if isDarkMode: window.outputbox.document().setDefaultStyleSheet(constants.STYLE_DARK_LINKS_COLOR);
        window.outputbox.setReadOnly(True)
        window.outputbox.setTextInteractionFlags(window.outputbox.textInteractionFlags() | Qt.TextSelectableByKeyboard)
        window.outputbox.setOpenExternalLinks(True)
        window.outputbox.unsetCursor()
        window.outputbox.moveCursor(QtGui.QTextCursor.End)
        window.outputbox.insertHtml(constants.STYLE_CONTACT_INFO.format(getMessage("contact-label")))
        window.outputbox.moveCursor(QtGui.QTextCursor.End)
        window.outputbox.setCursorWidth(0)
        if not isMacOS(): window.outputbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        window.outputlabel = QtWidgets.QLabel(getMessage("notifications-heading-label"))
        window.outputlabel.setMinimumHeight(27)
        window.chatInput = QtWidgets.QLineEdit()
        window.chatInput.setMaxLength(constants.MAX_CHAT_MESSAGE_LENGTH)
        window.chatInput.returnPressed.connect(self.sendChatMessage)
        window.chatButton = QtWidgets.QPushButton(
            QtGui.QPixmap(resourcespath + 'email_go.png'),
            getMessage("sendmessage-label"))
        window.chatButton.pressed.connect(self.sendChatMessage)
        window.chatLayout = QtWidgets.QHBoxLayout()
        window.chatFrame = QtWidgets.QFrame()
        window.chatFrame.setLayout(self.chatLayout)
        window.chatFrame.setContentsMargins(0, 0, 0, 0)
        window.chatFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        window.chatLayout.setContentsMargins(0, 0, 0, 0)
        self.chatButton.setToolTip(getMessage("sendmessage-tooltip"))
        window.chatLayout.addWidget(window.chatInput)
        window.chatLayout.addWidget(window.chatButton)
        window.chatFrame.setMaximumHeight(window.chatFrame.sizeHint().height())
        window.outputFrame = QtWidgets.QFrame()
        window.outputFrame.setLineWidth(0)
        window.outputFrame.setMidLineWidth(0)
        if isMacOS(): window.outputLayout.setSpacing(8)
        window.outputLayout.setContentsMargins(0, 0, 0, 0)
        window.outputLayout.addWidget(window.outputlabel)
        window.outputLayout.addWidget(window.outputbox)
        window.outputLayout.addWidget(window.chatFrame)
        window.outputFrame.setLayout(window.outputLayout)

        window.listLayout = QtWidgets.QVBoxLayout()
        window.listTreeModel = QtGui.QStandardItemModel()
        window.listTreeView = QtWidgets.QTreeView()
        window.listTreeView.setModel(window.listTreeModel)
        window.listTreeView.setIndentation(21)
        window.listTreeView.doubleClicked.connect(self.roomClicked)
        self.listTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listTreeView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listTreeView.customContextMenuRequested.connect(self.openRoomMenu)
        window.listlabel = QtWidgets.QLabel(getMessage("userlist-heading-label"))
        if isMacOS:
            window.listlabel.setMinimumHeight(21)
            window.sslButton = QtWidgets.QPushButton(QtGui.QPixmap(resourcespath + 'lock_green.png').scaled(14, 14),"")
            window.sslButton.setVisible(False)
            window.sslButton.setFixedHeight(21)
            window.sslButton.setFixedWidth(21)
            window.sslButton.setMinimumSize(21, 21)
            window.sslButton.setStyleSheet("QPushButton:!hover{border: 1px solid gray;} QPushButton:hover{border:2px solid black;}")
        else:
            window.listlabel.setMinimumHeight(27)
            window.sslButton = QtWidgets.QPushButton(QtGui.QPixmap(resourcespath + 'lock_green.png'),"")
            window.sslButton.setVisible(False)
            window.sslButton.setFixedHeight(27)
            window.sslButton.setFixedWidth(27)
        window.sslButton.pressed.connect(self.openSSLDetails)
        window.sslButton.setToolTip(getMessage("sslconnection-tooltip"))
        window.listFrame = QtWidgets.QFrame()
        window.listFrame.setLineWidth(0)
        window.listFrame.setMidLineWidth(0)
        window.listFrame.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        window.listLayout.setContentsMargins(0, 0, 0, 0)
        if isMacOS(): window.listLayout.setSpacing(8)

        window.userlistLayout = QtWidgets.QGridLayout()
        window.userlistFrame = QtWidgets.QFrame()
        window.userlistFrame.setLineWidth(0)
        window.userlistFrame.setMidLineWidth(0)
        window.userlistFrame.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        window.userlistLayout.setContentsMargins(0, 0, 0, 0)
        window.userlistFrame.setLayout(window.userlistLayout)
        window.userlistLayout.addWidget(window.listlabel, 0, 0, Qt.AlignLeft)
        window.userlistLayout.addWidget(window.sslButton, 0, 2,  Qt.AlignRight)
        window.userlistLayout.addWidget(window.listTreeView, 1, 0, 1, 3)
        if isMacOS(): window.userlistLayout.setContentsMargins(3, 0, 3, 0)

        window.listSplit = QtWidgets.QSplitter(Qt.Vertical, self)
        window.listSplit.addWidget(window.userlistFrame)
        window.listLayout.addWidget(window.listSplit)
        window.roomsCombobox = QtWidgets.QComboBox(self)
        window.roomsCombobox.setEditable(True)
        caseSensitiveCompleter = QtWidgets.QCompleter("", self)
        caseSensitiveCompleter.setCaseSensitivity(Qt.CaseSensitive)
        window.roomsCombobox.setCompleter(caseSensitiveCompleter)
        #window.roomsCombobox.setMaxLength(constants.MAX_ROOM_NAME_LENGTH)
        window.roomButton = QtWidgets.QPushButton(
            QtGui.QPixmap(resourcespath + 'door_in.png'),
            getMessage("joinroom-label"))
        window.roomButton.pressed.connect(self.joinRoom)
        window.roomButton.setFixedWidth(window.roomButton.sizeHint().width()+3)
        window.roomLayout = QtWidgets.QHBoxLayout()
        window.roomFrame = QtWidgets.QFrame()
        window.roomFrame.setLayout(self.roomLayout)
        window.roomFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        if isMacOS():
            window.roomLayout.setSpacing(8)
            window.roomLayout.setContentsMargins(3, 0, 0, 0)
        else:
            window.roomFrame.setContentsMargins(0, 0, 0, 0)
            window.roomLayout.setContentsMargins(0, 0, 0, 0)
        self.roomButton.setToolTip(getMessage("joinroom-tooltip"))
        window.roomLayout.addWidget(window.roomsCombobox)
        window.roomLayout.addWidget(window.roomButton)
        window.roomFrame.setMaximumHeight(window.roomFrame.sizeHint().height())
        window.listLayout.addWidget(window.roomFrame, Qt.AlignRight)

        window.listFrame.setLayout(window.listLayout)
        if isMacOS(): window.listFrame.setMinimumHeight(window.outputFrame.height())

        window.topSplit.addWidget(window.outputFrame)
        window.topSplit.addWidget(window.listFrame)
        window.topSplit.setStretchFactor(0, 4)
        window.topSplit.setStretchFactor(1, 5)
        window.mainLayout.addWidget(window.topSplit)
        window.topSplit.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

    def addBottomLayout(self, window):
        window.bottomLayout = QtWidgets.QHBoxLayout()
        window.bottomFrame = QtWidgets.QFrame()
        window.bottomFrame.setLayout(window.bottomLayout)
        window.bottomLayout.setContentsMargins(0, 0, 0, 0)
        if isMacOS(): window.bottomLayout.setSpacing(0)

        self.addPlaybackLayout(window)

        window.playlistGroup = self.PlaylistGroupBox(getMessage("sharedplaylistenabled-label"))
        window.playlistGroup.setCheckable(True)
        window.playlistGroup.toggled.connect(self.changePlaylistEnabledState)
        window.playlistLayout = QtWidgets.QHBoxLayout()
        window.playlistGroup.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        window.playlistGroup.setAcceptDrops(True)
        window.playlist = self.PlaylistWidget()
        window.playlist.setWindow(window)
        window.playlist.setItemDelegate(self.PlaylistItemDelegate())
        window.playlist.setDragEnabled(True)
        window.playlist.setAcceptDrops(True)
        window.playlist.setDropIndicatorShown(True)
        window.playlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        window.playlist.setDefaultDropAction(Qt.MoveAction)
        window.playlist.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        window.playlist.doubleClicked.connect(self.playlistItemClicked)
        window.playlist.setContextMenuPolicy(Qt.CustomContextMenu)
        window.playlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        window.playlist.customContextMenuRequested.connect(self.openPlaylistMenu)
        self.playlistUpdateTimer = task.LoopingCall(self.playlistChangeCheck)
        self.playlistUpdateTimer.start(0.1, True)
        noteFont = QtGui.QFont()
        noteFont.setItalic(True)
        playlistItem = QtWidgets.QListWidgetItem(getMessage("playlist-instruction-item-message"))
        playlistItem.setFont(noteFont)
        window.playlist.addItem(playlistItem)
        window.playlistLayout.addWidget(window.playlist)
        window.playlistLayout.setAlignment(Qt.AlignTop)
        window.playlistGroup.setLayout(window.playlistLayout)
        window.listSplit.addWidget(window.playlistGroup)

        window.readyPushButton = QtWidgets.QPushButton()
        readyFont = QtGui.QFont()
        readyFont.setWeight(QtGui.QFont.Bold)
        window.readyPushButton.setText(getMessage("ready-guipushbuttonlabel"))
        window.readyPushButton.setCheckable(True)
        window.readyPushButton.setAutoExclusive(False)
        window.readyPushButton.toggled.connect(self.changeReadyState)
        window.readyPushButton.setFont(readyFont)
        window.readyPushButton.setStyleSheet(constants.STYLE_READY_PUSHBUTTON)
        window.readyPushButton.setToolTip(getMessage("ready-tooltip"))
        window.listLayout.addWidget(window.readyPushButton, Qt.AlignRight)
        if isMacOS(): window.listLayout.setContentsMargins(0, 0, 0, 10)

        window.autoplayLayout = QtWidgets.QHBoxLayout()
        window.autoplayFrame = QtWidgets.QFrame()
        window.autoplayFrame.setVisible(False)

        window.autoplayFrame.setLayout(window.autoplayLayout)
        window.autoplayPushButton = QtWidgets.QPushButton()
        autoPlayFont = QtGui.QFont()
        autoPlayFont.setWeight(QtGui.QFont.Bold)
        window.autoplayPushButton.setText(getMessage("autoplay-guipushbuttonlabel"))
        window.autoplayPushButton.setCheckable(True)
        window.autoplayPushButton.setAutoExclusive(False)
        window.autoplayPushButton.toggled.connect(self.changeAutoplayState)
        window.autoplayPushButton.setFont(autoPlayFont)
        if isMacOS():
            window.autoplayFrame.setMinimumWidth(window.listFrame.sizeHint().width())
            window.autoplayLayout.setSpacing(15)
            window.autoplayLayout.setContentsMargins(0, 8, 3, 3)
            window.autoplayPushButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        else:
            window.autoplayLayout.setContentsMargins(0, 0, 0, 0)
            window.autoplayPushButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        window.autoplayPushButton.setStyleSheet(constants.STYLE_AUTO_PLAY_PUSHBUTTON)
        window.autoplayPushButton.setToolTip(getMessage("autoplay-tooltip"))
        window.autoplayLabel = QtWidgets.QLabel(getMessage("autoplay-minimum-label"))
        window.autoplayLabel.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        window.autoplayLabel.setMaximumWidth(window.autoplayLabel.minimumSizeHint().width())
        window.autoplayLabel.setToolTip(getMessage("autoplay-tooltip"))
        window.autoplayThresholdSpinbox = QtWidgets.QSpinBox()
        window.autoplayThresholdSpinbox.setMaximumWidth(window.autoplayThresholdSpinbox.minimumSizeHint().width())
        window.autoplayThresholdSpinbox.setMinimum(2)
        window.autoplayThresholdSpinbox.setMaximum(99)
        window.autoplayThresholdSpinbox.setToolTip(getMessage("autoplay-tooltip"))
        window.autoplayThresholdSpinbox.valueChanged.connect(self.changeAutoplayThreshold)
        window.autoplayLayout.addWidget(window.autoplayPushButton, Qt.AlignRight)
        window.autoplayLayout.addWidget(window.autoplayLabel, Qt.AlignRight)
        window.autoplayLayout.addWidget(window.autoplayThresholdSpinbox, Qt.AlignRight)

        window.listLayout.addWidget(window.autoplayFrame, Qt.AlignLeft)
        window.autoplayFrame.setMaximumHeight(window.autoplayFrame.sizeHint().height())
        window.mainLayout.addWidget(window.bottomFrame, Qt.AlignLeft)
        window.bottomFrame.setMaximumHeight(window.bottomFrame.minimumSizeHint().height())

    def addPlaybackLayout(self, window):
        window.playbackFrame = QtWidgets.QFrame()
        window.playbackFrame.setVisible(False)
        window.playbackFrame.setContentsMargins(0, 0, 0, 0)
        window.playbackLayout = QtWidgets.QHBoxLayout()
        window.playbackLayout.setAlignment(Qt.AlignLeft)
        window.playbackLayout.setContentsMargins(0, 0, 0, 0)
        window.playbackFrame.setLayout(window.playbackLayout)
        window.seekInput = QtWidgets.QLineEdit()
        window.seekInput.returnPressed.connect(self.seekFromButton)
        window.seekButton = QtWidgets.QPushButton(QtGui.QPixmap(resourcespath + 'clock_go.png'), "")
        window.seekButton.setToolTip(getMessage("seektime-menu-label"))
        window.seekButton.pressed.connect(self.seekFromButton)
        window.seekInput.setText("0:00")
        window.seekInput.setFixedWidth(60)
        window.playbackLayout.addWidget(window.seekInput)
        window.playbackLayout.addWidget(window.seekButton)
        window.unseekButton = QtWidgets.QPushButton(QtGui.QPixmap(resourcespath + 'arrow_undo.png'), "")
        window.unseekButton.setToolTip(getMessage("undoseek-menu-label"))
        window.unseekButton.pressed.connect(self.undoSeek)

        window.miscLayout = QtWidgets.QHBoxLayout()
        window.playbackLayout.addWidget(window.unseekButton)
        window.playButton = QtWidgets.QPushButton(QtGui.QPixmap(resourcespath + 'control_play_blue.png'), "")
        window.playButton.setToolTip(getMessage("play-menu-label"))
        window.playButton.pressed.connect(self.play)
        window.playbackLayout.addWidget(window.playButton)
        window.pauseButton = QtWidgets.QPushButton(QtGui.QPixmap(resourcespath + 'control_pause_blue.png'), "")
        window.pauseButton.setToolTip(getMessage("pause-menu-label"))
        window.pauseButton.pressed.connect(self.pause)
        window.playbackLayout.addWidget(window.pauseButton)
        window.playbackFrame.setMaximumHeight(window.playbackFrame.sizeHint().height())
        window.playbackFrame.setMaximumWidth(window.playbackFrame.sizeHint().width())
        window.outputLayout.addWidget(window.playbackFrame)

    def loadMenubar(self, window, passedBar):
        if passedBar is not None:
            window.menuBar = passedBar['bar']
            window.editMenu = passedBar['editMenu']
        else:
            window.menuBar = QtWidgets.QMenuBar()
            window.editMenu = None

    def populateMenubar(self, window):
        # File menu

        window.fileMenu = QtWidgets.QMenu(getMessage("file-menu-label"), self)
        window.openAction = window.fileMenu.addAction(QtGui.QPixmap(resourcespath + 'folder_explore.png'),
                                                      getMessage("openmedia-menu-label"))
        window.openAction.triggered.connect(self.browseMediapath)
        window.openAction = window.fileMenu.addAction(QtGui.QPixmap(resourcespath + 'world_explore.png'),
                                                      getMessage("openstreamurl-menu-label"))
        window.openAction.triggered.connect(self.promptForStreamURL)
        window.openAction = window.fileMenu.addAction(QtGui.QPixmap(resourcespath + 'film_folder_edit.png'),
                                                      getMessage("setmediadirectories-menu-label"))
        window.openAction.triggered.connect(self.openSetMediaDirectoriesDialog)

        window.exitAction = window.fileMenu.addAction(getMessage("exit-menu-label"))
        if isMacOS():
            window.exitAction.setMenuRole(QtWidgets.QAction.QuitRole)
        else:
            window.exitAction.setIcon(QtGui.QPixmap(resourcespath + 'cross.png'))
        window.exitAction.triggered.connect(self.exitSyncplay)

        if(window.editMenu is not None):
            window.menuBar.insertMenu(window.editMenu.menuAction(), window.fileMenu)
        else:
            window.menuBar.addMenu(window.fileMenu)

        # Playback menu

        window.playbackMenu = QtWidgets.QMenu(getMessage("playback-menu-label"), self)
        window.playAction = window.playbackMenu.addAction(
            QtGui.QPixmap(resourcespath + 'control_play_blue.png'),
            getMessage("play-menu-label"))
        window.playAction.triggered.connect(self.play)
        window.pauseAction = window.playbackMenu.addAction(
            QtGui.QPixmap(resourcespath + 'control_pause_blue.png'),
            getMessage("pause-menu-label"))
        window.pauseAction.triggered.connect(self.pause)
        window.seekAction = window.playbackMenu.addAction(
            QtGui.QPixmap(resourcespath + 'clock_go.png'),
            getMessage("seektime-menu-label"))
        window.seekAction.triggered.connect(self.seekPositionDialog)
        window.unseekAction = window.playbackMenu.addAction(
            QtGui.QPixmap(resourcespath + 'arrow_undo.png'),
            getMessage("undoseek-menu-label"))
        window.unseekAction.triggered.connect(self.undoSeek)

        window.menuBar.addMenu(window.playbackMenu)

        # Advanced menu

        window.advancedMenu = QtWidgets.QMenu(getMessage("advanced-menu-label"), self)
        window.setoffsetAction = window.advancedMenu.addAction(
            QtGui.QPixmap(resourcespath + 'timeline_marker.png'),
            getMessage("setoffset-menu-label"))
        window.setoffsetAction.triggered.connect(self.setOffset)
        window.setTrustedDomainsAction = window.advancedMenu.addAction(
            QtGui.QPixmap(resourcespath + 'shield_edit.png'),
            getMessage("settrusteddomains-menu-label"))
        window.setTrustedDomainsAction.triggered.connect(self.openSetTrustedDomainsDialog)
        window.createcontrolledroomAction = window.advancedMenu.addAction(
            QtGui.QPixmap(resourcespath + 'page_white_key.png'), getMessage("createcontrolledroom-menu-label"))
        window.createcontrolledroomAction.triggered.connect(self.createControlledRoom)
        window.identifyascontroller = window.advancedMenu.addAction(QtGui.QPixmap(resourcespath + 'key_go.png'),
                                                                    getMessage("identifyascontroller-menu-label"))
        window.identifyascontroller.triggered.connect(self.identifyAsController)

        window.menuBar.addMenu(window.advancedMenu)

        # Window menu

        window.windowMenu = QtWidgets.QMenu(getMessage("window-menu-label"), self)

        window.editroomsAction = window.windowMenu.addAction(QtGui.QPixmap(resourcespath + 'door_open_edit.png'), getMessage("roomlist-msgbox-label"))
        window.editroomsAction.triggered.connect(self.openEditRoomsDialog)
        window.menuBar.addMenu(window.windowMenu)

        window.playbackAction = window.windowMenu.addAction(getMessage("playbackbuttons-menu-label"))
        window.playbackAction.setCheckable(True)
        window.playbackAction.triggered.connect(self.updatePlaybackFrameVisibility)

        window.autoplayAction = window.windowMenu.addAction(getMessage("autoplay-menu-label"))
        window.autoplayAction.setCheckable(True)
        window.autoplayAction.triggered.connect(self.updateAutoplayVisibility)

        window.hideEmptyRoomsAction = window.windowMenu.addAction(getMessage("hideemptyrooms-menu-label"))
        window.hideEmptyRoomsAction.setCheckable(True)
        window.hideEmptyRoomsAction.triggered.connect(self.updateEmptyRoomVisiblity)

        # Help menu

        window.helpMenu = QtWidgets.QMenu(getMessage("help-menu-label"), self)

        window.userguideAction = window.helpMenu.addAction(
            QtGui.QPixmap(resourcespath + 'help.png'),
            getMessage("userguide-menu-label"))
        window.userguideAction.triggered.connect(self.openUserGuide)
        window.updateAction = window.helpMenu.addAction(
            QtGui.QPixmap(resourcespath + 'application_get.png'),
            getMessage("update-menu-label"))
        window.updateAction.triggered.connect(self.userCheckForUpdates)

        if not isMacOS():
            window.helpMenu.addSeparator()
            window.about = window.helpMenu.addAction(
                QtGui.QPixmap(resourcespath + 'syncplay.png'),
                getMessage("about-menu-label"))
        else:
            window.about = window.helpMenu.addAction("&About")
            window.about.setMenuRole(QtWidgets.QAction.AboutRole)
        window.about.triggered.connect(self.openAbout)

        window.menuBar.addMenu(window.helpMenu)
        window.mainLayout.setMenuBar(window.menuBar)

    @needsClient
    def openSSLDetails(self):
        sslDetailsBox = CertificateDialog(self.getSSLInformation())
        sslDetailsBox.exec_()
        self.sslButton.setDown(False)

    def openAbout(self):
        aboutMsgBox = AboutDialog()
        aboutMsgBox.exec_()

    def addMainFrame(self, window):
        window.mainFrame = QtWidgets.QFrame()
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

    def updatePlaybackFrameVisibility(self):
        self.playbackFrame.setVisible(self.playbackAction.isChecked())

    def updateAutoplayVisibility(self):
        self.autoplayFrame.setVisible(self.autoplayAction.isChecked())

    def updateEmptyRoomVisiblity(self):
        self.hideEmptyRooms = self.hideEmptyRoomsAction.isChecked()
        if self._syncplayClient:
            self._syncplayClient.getUserList()

    def changeReadyState(self):
        self.updateReadyIcon()
        if self._syncplayClient:
            self._syncplayClient.changeReadyState(self.readyPushButton.isChecked())
        else:
            self.showDebugMessage("Tried to change ready state too soon.")

    def changePlaylistEnabledState(self):
        self._syncplayClient.changePlaylistEnabledState(self.playlistGroup.isChecked())

    @needsClient
    def changeAutoplayThreshold(self, source=None):
        self._syncplayClient.changeAutoPlayThrehsold(self.autoplayThresholdSpinbox.value())

    def updateAutoPlayState(self, newState):
        oldState = self.autoplayPushButton.isChecked()
        if newState != oldState and newState is not None:
            self.autoplayPushButton.blockSignals(True)
            self.autoplayPushButton.setChecked(newState)
            self.autoplayPushButton.blockSignals(False)
        self.updateAutoPlayIcon()

    @needsClient
    def changeAutoplayState(self, source=None):
        self.updateAutoPlayIcon()
        if self._syncplayClient:
            self._syncplayClient.changeAutoplayState(self.autoplayPushButton.isChecked())
        else:
            self.showDebugMessage("Tried to set AutoplayState too soon")

    def updateReadyIcon(self):
        ready = self.readyPushButton.isChecked()
        if ready:
            self.readyPushButton.setIcon(QtGui.QPixmap(resourcespath + 'tick_checkbox.png'))
        else:
            self.readyPushButton.setIcon(QtGui.QPixmap(resourcespath + 'empty_checkbox.png'))

    def updateAutoPlayIcon(self):
        ready = self.autoplayPushButton.isChecked()
        if ready:
            self.autoplayPushButton.setIcon(QtGui.QPixmap(resourcespath + 'tick_checkbox.png'))
        else:
            self.autoplayPushButton.setIcon(QtGui.QPixmap(resourcespath + 'empty_checkbox.png'))

    def automaticUpdateCheck(self):
        currentDateTimeValue = QDateTime.currentDateTime()
        if not self.config['checkForUpdatesAutomatically']:
            return
        try:
            if self.config['lastCheckedForUpdates']:
                configLastChecked = datetime.strptime(self.config["lastCheckedForUpdates"], "%Y-%m-%d %H:%M:%S.%f")
                if self.lastCheckedForUpdates is None or configLastChecked > self.lastCheckedForUpdates.toPython():
                    self.lastCheckedForUpdates = QDateTime.fromString(self.config["lastCheckedForUpdates"], 'yyyy-MM-dd HH-mm-ss')
            if self.lastCheckedForUpdates is None:
                self.checkForUpdates()
            else:
                timeDelta = currentDateTimeValue.toPython() - self.lastCheckedForUpdates.toPython()
                if timeDelta.total_seconds() > constants.AUTOMATIC_UPDATE_CHECK_FREQUENCY:
                    self.checkForUpdates()
        except:
            self.showDebugMessage("Automatic check for updates failed. An update check was manually trigggered.")
            self.checkForUpdates()

    def userCheckForUpdates(self):
        self.checkForUpdates(userInitiated=True)

    @needsClient
    def checkForUpdates(self, userInitiated=False):
        self.lastCheckedForUpdates = QDateTime.currentDateTime()
        updateStatus, updateMessage, updateURL, self.publicServerList = self._syncplayClient.checkForUpdate(userInitiated)

        if updateMessage is None:
            if updateStatus == "uptodate":
                updateMessage = getMessage("syncplay-uptodate-notification")
            elif updateStatus == "updateavailale":
                updateMessage = getMessage("syncplay-updateavailable-notification")
            else:
                import syncplay
                updateMessage = getMessage("update-check-failed-notification").format(syncplay.version)
                if userInitiated == True:
                    updateURL = constants.SYNCPLAY_DOWNLOAD_URL
        if updateURL is not None:
            reply = QtWidgets.QMessageBox.question(
                self, "Syncplay",
                updateMessage, QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.QtGui.QDesktopServices.openUrl(QUrl(updateURL))
        elif userInitiated:
            QtWidgets.QMessageBox.information(self, "Syncplay", updateMessage)
        else:
            self.showMessage(updateMessage)

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
            url = event.mimeData().urls()[0]
            if isMacOS() and IsPySide:
                macURL = NSString.alloc().initWithString_(str(url.toString()))
                pathString = macURL.stringByAddingPercentEscapesUsingEncoding_(NSUTF8StringEncoding)
                dropfilepath = os.path.abspath(NSURL.URLWithString_(pathString).filePathURL().path())
            else:
                dropfilepath = os.path.abspath(str(url.toLocalFile()))
            if rewindFile == False:
                self._syncplayClient.openFile(dropfilepath, resetPosition=False, fromUser=True)
            else:
                self._syncplayClient.setPosition(0)
                self._syncplayClient.openFile(dropfilepath, resetPosition=True, fromUser=True)
                self._syncplayClient.setPosition(0)

    def setPlaylist(self, newPlaylist, newIndexFilename=None):
        if self.updatingPlaylist:
            self.ui.showDebugMessage("Trying to set playlist while it is already being updated")
        if newPlaylist == self.playlistState:
            if newIndexFilename:
                self.playlist.setPlaylistIndexFilename(newIndexFilename)
            self.updatingPlaylist = False
            return
        self.updatingPlaylist = True
        if newPlaylist and len(newPlaylist) > 0:
            self.clearedPlaylistNote = True
        self.playlistState = newPlaylist
        self.playlist.updatePlaylist(newPlaylist)
        if newIndexFilename:
            self.playlist.setPlaylistIndexFilename(newIndexFilename)
        self.updatingPlaylist = False
        self._syncplayClient.fileSwitch.updateInfo()

    def setPlaylistIndexFilename(self, filename):
        self.playlist.setPlaylistIndexFilename(filename)

    def addFileToPlaylist(self, filePath, index=-1):
        if not isURL(filePath):
            self.removePlaylistNote()
            filename = os.path.basename(filePath)
            if self.noPlaylistDuplicates(filename):
                if self.playlist == -1 or index == -1:
                    self.playlist.addItem(filename)
                else:
                    self.playlist.insertItem(index, filename)
                self._syncplayClient.fileSwitch.notifyUserIfFileNotInMediaDirectory(filename, filePath)
        else:
            self.removePlaylistNote()
            if self.noPlaylistDuplicates(filePath):
                if self.playlist == -1 or index == -1:
                    self.playlist.addItem(filePath)
                else:
                    self.playlist.insertItem(index, filePath)

    def openFile(self, filePath, resetPosition=False, fromUser=False):
        self._syncplayClient.openFile(filePath, resetPosition, fromUser=fromUser)

    def noPlaylistDuplicates(self, filename):
        if self.isItemInPlaylist(filename):
            self.showErrorMessage(getMessage("cannot-add-duplicate-error").format(filename))
            return False
        else:
            return True

    def isItemInPlaylist(self, filename):
        for playlistindex in range(self.playlist.count()):
            if self.playlist.item(playlistindex).text() == filename:
                return True
        return False

    def addStreamToPlaylist(self, streamURI):
        self.removePlaylistNote()
        if self.noPlaylistDuplicates(streamURI):
            self.playlist.addItem(streamURI)

    def removePlaylistNote(self):
        if not self.clearedPlaylistNote:
            for index in range(self.playlist.count()):
                self.playlist.takeItem(0)
            self.clearedPlaylistNote = True

    def addFolderToPlaylist(self, folderPath):
        self.showErrorMessage("You tried to add the folder '{}' to the playlist. Syncplay only currently supports adding files to the playlist.".format(folderPath))  # TODO: Implement "add folder to playlist"

    def deleteSelectedPlaylistItems(self):
        self.playlist.remove_selected_items()

    def saveSettings(self):
        settings = QSettings("Syncplay", "MainWindow")
        settings.beginGroup("MainWindow")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.setValue("showPlaybackButtons", self.playbackAction.isChecked())
        settings.setValue("showAutoPlayButton", self.autoplayAction.isChecked())
        settings.setValue("hideEmptyRooms", self.hideEmptyRoomsAction.isChecked())
        settings.setValue("autoplayChecked", self.autoplayPushButton.isChecked())
        settings.setValue("autoplayMinUsers", self.autoplayThresholdSpinbox.value())
        settings.endGroup()
        settings = QSettings("Syncplay", "Interface")
        settings.beginGroup("Update")
        settings.setValue("lastCheckedQt", self.lastCheckedForUpdates)
        settings.endGroup()
        settings.beginGroup("PublicServerList")
        if self.publicServerList:
            settings.setValue("publicServers", self.publicServerList)
        settings.endGroup()

    def loadSettings(self):
        settings = QSettings("Syncplay", "MainWindow")
        settings.beginGroup("MainWindow")
        self.resize(settings.value("size", QSize(700, 500)))
        movePos = settings.value("pos", QPoint(200, 200))
        if not IsPySide6:
            windowGeometry = QtWidgets.QApplication.desktop().availableGeometry(self)
        else:
            windowGeometry = QtWidgets.QApplication.primaryScreen().geometry()
        posIsOnScreen = windowGeometry.contains(QtCore.QRect(movePos.x(), movePos.y(), 1, 1))
        if not posIsOnScreen:
            movePos = QPoint(200,200)
        self.move(movePos)
        if settings.value("showPlaybackButtons", "false") == "true":
            self.playbackAction.setChecked(True)
            self.updatePlaybackFrameVisibility()
        if settings.value("showAutoPlayButton", "false") == "true":
            self.autoplayAction.setChecked(True)
            self.updateAutoplayVisibility()
        if settings.value("hideEmptyRooms", "false") == "true":
            self.hideEmptyRooms = True
            self.hideEmptyRoomsAction.setChecked(True)
        if settings.value("autoplayChecked", "false") == "true":
            self.updateAutoPlayState(True)
            self.autoplayPushButton.setChecked(True)
        self.autoplayThresholdSpinbox.blockSignals(True)
        self.autoplayThresholdSpinbox.setValue(int(settings.value("autoplayMinUsers", 2)))
        self.autoplayThresholdSpinbox.blockSignals(False)
        settings.endGroup()
        settings = QSettings("Syncplay", "Interface")
        settings.beginGroup("Update")
        self.lastCheckedForUpdates = settings.value("lastCheckedQt", None)
        settings.endGroup()
        settings.beginGroup("PublicServerList")
        self.publicServerList = settings.value("publicServers", None)

    def __init__(self, passedBar=None):
        super(MainWindow, self).__init__()
        self.console = ConsoleInGUI()
        self.console.setDaemon(True)
        self.newWatchlist = []
        self.publicServerList = []
        self.lastCheckedForUpdates = None
        self._syncplayClient = None
        self.folderSearchEnabled = True
        self.hideEmptyRooms = False
        self.currentRooms = []
        self.QtGui = QtGui
        if isMacOS():
            self.setWindowFlags(self.windowFlags())
        else:
            self.setWindowFlags(self.windowFlags() & Qt.AA_DontUseNativeMenuBar)
        self.setWindowTitle("Syncplay v" + version + revision)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.addTopLayout(self)
        self.addBottomLayout(self)
        self.loadMenubar(self, passedBar)
        self.populateMenubar(self)
        self.addMainFrame(self)
        self.loadSettings()
        self.setWindowIcon(QtGui.QPixmap(resourcespath + "syncplay.png"))
        self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint & Qt.WindowMinimizeButtonHint & ~Qt.WindowContextHelpButtonHint)
        self.show()
        self.setAcceptDrops(True)
        self.clearedPlaylistNote = False
        self.uiMode = constants.GRAPHICAL_UI_MODE
