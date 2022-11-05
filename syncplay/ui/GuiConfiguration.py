
import os
import sys
import threading
from datetime import datetime

from syncplay import constants
from syncplay import utils
from syncplay.messages import getMessage, getLanguages, setLanguage, getInitialLanguage
from syncplay.players.playerFactory import PlayerFactory
from syncplay.utils import isBSD, isLinux, isMacOS, isWindows
from syncplay.utils import resourcespath, posixresourcespath, playerPathExists

from syncplay.vendor.Qt import QtCore, QtWidgets, QtGui, __binding__, IsPySide, IsPySide2, IsPySide6
from syncplay.vendor.Qt.QtCore import Qt, QSettings, QCoreApplication, QSize, QPoint, QUrl, QLine, QEventLoop, Signal
from syncplay.vendor.Qt.QtWidgets import QApplication, QLineEdit, QLabel, QCheckBox, QButtonGroup, QRadioButton, QDoubleSpinBox, QPlainTextEdit
from syncplay.vendor.Qt.QtGui import QCursor, QIcon, QImage, QDesktopServices
try:
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
except AttributeError:
    pass  # To ignore error "Attribute Qt::AA_EnableHighDpiScaling must be set before QCoreApplication is created"
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
if IsPySide6:
    from PySide6.QtCore import QStandardPaths
elif IsPySide2:
    from PySide2.QtCore import QStandardPaths


class GuiConfiguration:
    def __init__(self, config, error=None, defaultConfig=None):
        self.defaultConfig = defaultConfig
        self.config = config
        self._availablePlayerPaths = []
        self.error = error
        constants.DEBUG_MODE = config['debug']

    def run(self):
        if QCoreApplication.instance() is None:
            self.app = QtWidgets.QApplication(sys.argv)
        dialog = ConfigDialog(self.config, self._availablePlayerPaths, self.error, self.defaultConfig)
        configLoop = QEventLoop()
        dialog.show()
        dialog.closed.connect(configLoop.quit)
        configLoop.exec_()

    def setAvailablePaths(self, paths):
        self._availablePlayerPaths = paths

    def getProcessedConfiguration(self):
        return self.config

    class WindowClosed(Exception):
        pass


class GetPlayerIconThread(threading.Thread, QtCore.QObject):
    daemon = True
    done = QtCore.Signal(str, str)

    def __init__(self):
        threading.Thread.__init__(self, name='GetPlayerIcon')
        QtCore.QObject.__init__(self)
        self.condvar = threading.Condition()
        self.playerpath = None

    def setPlayerPath(self, playerpath):
        self.condvar.acquire()
        was_none = self.playerpath is None
        self.playerpath = playerpath
        if was_none:
            self.condvar.notify()
        self.condvar.release()

    def run(self):
        while True:
            self.condvar.acquire()
            if self.playerpath is None:
                self.condvar.wait()
            playerpath = self.playerpath
            self.playerpath = None
            self.condvar.release()

            self.done.emit('spinner.mng', '')
            iconpath = PlayerFactory().getPlayerIconByPath(playerpath)
            self.done.emit(iconpath, playerpath)


class ConfigDialog(QtWidgets.QDialog):

    pressedclosebutton = True
    moreToggling = False

    closed = Signal()

    def automaticUpdatePromptCheck(self):
        if self.automaticupdatesCheckbox.checkState() == Qt.PartiallyChecked:
            reply = QtWidgets.QMessageBox.question(
                self, "Syncplay",
                getMessage("promptforupdate-label"),
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.automaticupdatesCheckbox.setChecked(True)
            else:
                self.automaticupdatesCheckbox.setChecked(False)

    def moreToggled(self):
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        if self.moreToggling is False:
            self.moreToggling = True

            if self.showmoreCheckbox.isChecked():
                self.tabListFrame.show()
                self.resetButton.show()
                self.playerargsTextbox.show()
                self.playerargsLabel.show()
                self.mediapathTextbox.show()
                self.mediapathLabel.show()
                self.mediabrowseButton.show()
                self.runButton.show()
                self.saveMoreState(True)
                self.tabListWidget.setCurrentRow(0)
                self.ensureTabListIsVisible()
                if isMacOS(): self.mediaplayerSettingsGroup.setFixedHeight(self.mediaplayerSettingsGroup.minimumSizeHint().height())
                self.stackedFrame.setFixedHeight(self.stackedFrame.minimumSizeHint().height())
            else:
                self.tabListFrame.hide()
                self.resetButton.hide()
                self.playerargsTextbox.hide()
                self.playerargsLabel.hide()
                self.runButton.hide()
                if self.mediapathTextbox.text() == "":
                    self.mediapathTextbox.hide()
                    self.mediapathLabel.hide()
                    self.mediabrowseButton.hide()
                else:
                    self.mediapathTextbox.show()
                    self.mediapathLabel.show()
                    self.mediabrowseButton.show()
                self.saveMoreState(False)
                self.stackedLayout.setCurrentIndex(0)
                if isMacOS():
                    self.mediaplayerSettingsGroup.setFixedHeight(self.mediaplayerSettingsGroup.minimumSizeHint().height())
                    newHeight = self.connectionSettingsGroup.minimumSizeHint().height()+self.mediaplayerSettingsGroup.minimumSizeHint().height()+self.bottomButtonFrame.minimumSizeHint().height()+50
                else:
                    newHeight = self.connectionSettingsGroup.minimumSizeHint().height()+self.mediaplayerSettingsGroup.minimumSizeHint().height()+self.bottomButtonFrame.minimumSizeHint().height()+13
                if self.error:
                    newHeight += self.errorLabel.height()+3
                self.stackedFrame.setFixedHeight(newHeight)
            self.adjustSize()
            if isMacOS():
                newHeight = self.connectionSettingsGroup.minimumSizeHint().height()+self.mediaplayerSettingsGroup.minimumSizeHint().height()+self.bottomButtonFrame.minimumSizeHint().height()+50+16
                self.setFixedWidth(self.sizeHint().width())
                self.setFixedHeight(newHeight)
            else:
                self.setFixedSize(self.sizeHint())
        self.moreToggling = False
        self.setFixedWidth(self.minimumSizeHint().width())

    def openHelp(self):
        self.QtGui.QDesktopServices.openUrl(QUrl("https://syncplay.pl/guide/client/"))

    def openRoomsDialog(self):
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

    def safenormcaseandpath(self, path):
        if utils.isURL(path):
            return path
        else:
            return os.path.normcase(os.path.normpath(path))

    def _tryToFillPlayerPath(self, playerpath, playerpathlist):
        settings = QSettings("Syncplay", "PlayerList")
        settings.beginGroup("PlayerList")
        savedPlayers = settings.value("PlayerList", [])
        if not isinstance(savedPlayers, list):
            savedPlayers = []
        else:
            for i, savedPlayer in enumerate(savedPlayers):
                savedPlayers[i] = self.safenormcaseandpath(savedPlayer)
        playerpathlist = list(set(playerpathlist + savedPlayers))
        settings.endGroup()
        foundpath = ""

        if playerpath is not None and playerpath != "":
            if utils.isURL(playerpath):
                foundpath = playerpath
                self.executablepathCombobox.addItem(foundpath)

            else:
                if not playerPathExists(playerpath):
                    expandedpath = PlayerFactory().getExpandedPlayerPathByPath(playerpath)
                    if expandedpath is not None and playerPathExists(expandedpath):
                        playerpath = expandedpath
                    elif "mpvnet.exe" in playerpath and playerPathExists(playerpath.replace("mpvnet.exe","mpvnet.com")):
                        self.executablepathCombobox.addItem(playerpath)

                if playerPathExists(playerpath):
                    foundpath = playerpath
                    self.executablepathCombobox.addItem(foundpath)

        for path in playerpathlist:
            if utils.isURL(path):
                if foundpath == "":
                    foundpath = path
                if path != playerpath:
                    self.executablepathCombobox.addItem(path)

            elif playerPathExists(path) and os.path.normcase(os.path.normpath(path)) != os.path.normcase(os.path.normpath(foundpath)):
                self.executablepathCombobox.addItem(path)
                if foundpath == "":
                    foundpath = path

        if foundpath != "":
            settings.beginGroup("PlayerList")
            playerpathlist.append(self.safenormcaseandpath(foundpath))
            settings.setValue("PlayerList", list(set(playerpathlist)))
            settings.endGroup()
        return foundpath

    @QtCore.Slot(str, str)
    def _updateExecutableIcon(self, iconpath, playerpath):
        if iconpath is not None and iconpath != "":
            if iconpath.endswith('.mng'):
                movie = QtGui.QMovie(resourcespath + iconpath)
                movie.setCacheMode(QtGui.QMovie.CacheMode.CacheAll)
                self.executableiconLabel.setMovie(movie)
                movie.start()
            else:
                self.executableiconImage.load(resourcespath + iconpath)
                self.executableiconLabel.setPixmap(QtGui.QPixmap.fromImage(self.executableiconImage))
        else:
            self.executableiconLabel.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage()))
        self.updatePlayerArguments(playerpath)

    def updateExecutableIcon(self):
        """
        Start getting the icon path in another thread, which will set the GUI
        icon if valid.

        This is performed outside the main thread because networked players may
        take a long time to perform their checks and hang the GUI while doing
        so.
        """
        currentplayerpath = str(self.executablepathCombobox.currentText())
        self._playerProbeThread.setPlayerPath(currentplayerpath)

    def updatePlayerArguments(self, currentplayerpath):
        argumentsForPath = utils.getPlayerArgumentsByPathAsText(self.perPlayerArgs, currentplayerpath)
        self.playerargsTextbox.blockSignals(True)
        self.playerargsTextbox.setText(argumentsForPath)
        self.playerargsTextbox.blockSignals(False)

    def changedPlayerArgs(self):
        currentplayerpath = self.executablepathCombobox.currentText()

        if currentplayerpath:
            NewPlayerArgs = self.playerargsTextbox.text().split(" ") if self.playerargsTextbox.text() else ""
            self.perPlayerArgs[self.executablepathCombobox.currentText()] = NewPlayerArgs

    def languageChanged(self):
        setLanguage(str(self.languageCombobox.itemData(self.languageCombobox.currentIndex())))
        QtWidgets.QMessageBox.information(self, "Syncplay", getMessage("language-changed-msgbox-label"))

    def browsePlayerpath(self):
        options = QtWidgets.QFileDialog.Options()
        defaultdirectory = ""
        browserfilter = "All files (*)"

        if os.name == 'nt':
            browserfilter = "Executable files (*.exe);;All files (*)"
            if "PROGRAMFILES(X86)" in os.environ:
                defaultdirectory = os.environ["ProgramFiles(x86)"]
            elif "PROGRAMFILES" in os.environ:
                defaultdirectory = os.environ["ProgramFiles"]
            elif "PROGRAMW6432" in os.environ:
                defaultdirectory = os.environ["ProgramW6432"]
        elif isLinux():
            defaultdirectory = "/usr/bin"
        elif isMacOS():
            defaultdirectory = "/Applications/"
        elif isBSD():
            defaultdirectory = "/usr/local/bin"

        fileName, filtr = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Browse for media player executable",
            defaultdirectory,
            browserfilter, "", options)
        if fileName:
            if isMacOS() and fileName.endswith('.app'):  # see GitHub issue #91
                # Mac OS X application bundles contain a Info.plist in the Contents subdirectory of the .app.
                # This plist file includes the 'CFBundleExecutable' key, which specifies the name of the
                # executable.  I would have used plistlib here, but since the version of this library in
                # py < 3.4 can't read from binary plist files it's pretty much useless.  Therefore, let's
                # play a game of "Guess my executable!"

                # Step 1: get all the executable files.  In a Mac OS X Application bundle, executables are stored
                # inside <bundle root>/Contents/MacOS.
                execPath = os.path.join(os.path.normpath(fileName), 'Contents', 'MacOS')
                execFiles = []
                for fn in os.listdir(execPath):
                    fn = os.path.join(execPath, fn)
                    if os.path.isfile(fn) and os.access(fn, os.X_OK):
                        execFiles.append(fn)

                # Step 2: figure out which file name looks like the application name
                baseAppName = os.path.basename(fileName).replace('.app', '').lower()
                foundExe = False
                for fn in execFiles:
                    baseExecName = os.path.basename(fn).lower()
                    if baseAppName == baseExecName:
                        fileName = fn
                        foundExe = True
                        break

                # Step 3: use the first executable in the list if no executable was found
                try:
                    if not foundExe:
                        fileName = execFiles[0]
                except IndexError:  # whoops, looks like this .app doesn't contain a executable file at all
                    pass

            self.executablepathCombobox.setEditText(os.path.normpath(fileName))

    def loadLastUpdateCheckDate(self):
        settings = QSettings("Syncplay", "Interface")
        settings.beginGroup("Update")
        try:
            self.lastCheckedForUpdates = settings.value("lastCheckedQt", None)
            if self.lastCheckedForUpdates:
                if self.config["lastCheckedForUpdates"] != None and self.config["lastCheckedForUpdates"] != "":
                    if self.lastCheckedForUpdates.toPython() > datetime.strptime(self.config["lastCheckedForUpdates"], "%Y-%m-%d %H:%M:%S.%f"):
                        self.config["lastCheckedForUpdates"] = self.lastCheckedForUpdates.toString("yyyy-MM-d HH:mm:ss.z")
                else:
                    self.config["lastCheckedForUpdates"] = self.lastCheckedForUpdates.toString("yyyy-MM-d HH:mm:ss.z")
        except:
            self.config["lastCheckedForUpdates"] = None

    def loadSavedPublicServerList(self):
        settings = QSettings("Syncplay", "Interface")
        settings.beginGroup("PublicServerList")
        self.publicServers = settings.value("publicServers", None)

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

    def getMoreState(self):
        settings = QSettings("Syncplay", "MoreSettings")
        settings.beginGroup("MoreSettings")
        morestate = str.lower(str(settings.value("ShowMoreSettings", "false")))
        settings.endGroup()
        if morestate == "true":
            return True
        else:
            return False

    def saveMoreState(self, morestate):
        settings = QSettings("Syncplay", "MoreSettings")
        settings.beginGroup("MoreSettings")
        settings.setValue("ShowMoreSettings", morestate)
        settings.endGroup()

    def updateServerList(self):
        try:
            servers = utils.getListOfPublicServers()
        except IOError as e:
            self.showErrorMessage(e.args[0])
            return
        currentServer = self.hostCombobox.currentText()
        self.hostCombobox.clear()
        if servers:
            i = 0
            for server in servers:
                self.hostCombobox.addItem(server[1])
                self.hostCombobox.setItemData(i, server[0], Qt.ToolTipRole)
                i += 1
            settings = QSettings("Syncplay", "Interface")
            settings.beginGroup("PublicServerList")
            settings.setValue("publicServers", servers)
        self.hostCombobox.setEditText(currentServer)

    def fillRoomsCombobox(self):
        previousRoomSelection = self.roomsCombobox.currentText()
        self.roomsCombobox.clear()
        for roomListValue in self.config['roomList']:
            self.roomsCombobox.addItem(roomListValue)
        self.roomsCombobox.setEditText(previousRoomSelection)

    def relistRoomList(self, newRooms):
        filteredNewRooms = [room for room in newRooms if room and not room.isspace()]
        self.config['roomList'] = filteredNewRooms
        self.fillRoomsCombobox()

    def addRoomToList(self, newRoom=None):
        if newRoom is None:
            newRoom = self.roomsCombobox.currentText()
        if not newRoom:
            return
        roomList = self.config['roomList']
        if newRoom not in roomList:
            roomList.append(newRoom)
        roomList = sorted(roomList)
        self.config['roomList'] = roomList

    def showErrorMessage(self, errorMessage):
        QtWidgets.QMessageBox.warning(self, "Syncplay", errorMessage)

    def browseMediapath(self):
        self.loadMediaBrowseSettings()
        options = QtWidgets.QFileDialog.Options()
        if IsPySide:
            if self.config["mediaSearchDirectories"] and os.path.isdir(self.config["mediaSearchDirectories"][0]):
                defaultdirectory = self.config["mediaSearchDirectories"][0]
            elif os.path.isdir(self.mediadirectory):
                defaultdirectory = self.mediadirectory
            elif os.path.isdir(QDesktopServices.storageLocation(QDesktopServices.MoviesLocation)):
                defaultdirectory = QDesktopServices.storageLocation(QDesktopServices.MoviesLocation)
            elif os.path.isdir(QDesktopServices.storageLocation(QDesktopServices.HomeLocation)):
                defaultdirectory = QDesktopServices.storageLocation(QDesktopServices.HomeLocation)
            else:
                defaultdirectory = ""
        elif IsPySide6 or IsPySide2:
            if self.config["mediaSearchDirectories"] and os.path.isdir(self.config["mediaSearchDirectories"][0]):
                defaultdirectory = self.config["mediaSearchDirectories"][0]
            elif os.path.isdir(self.mediadirectory):
                defaultdirectory = self.mediadirectory
            elif os.path.isdir(QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)[0]):
                defaultdirectory = QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)[0]
            elif os.path.isdir(QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]):
                defaultdirectory = QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]
            else:
                defaultdirectory = ""
        browserfilter = "All files (*)"
        fileName, filtr = QtWidgets.QFileDialog.getOpenFileName(
            self, "Browse for media files", defaultdirectory,
            browserfilter, "", options)
        if fileName:
            self.mediapathTextbox.setText(os.path.normpath(fileName))
            self.mediadirectory = os.path.dirname(fileName)
            self.saveMediaBrowseSettings()

    def _runWithoutStoringConfig(self):
        self._saveDataAndLeave(False)

    def _saveDataAndLeave(self, storeConfiguration=True):
        self.config['noStore'] = not storeConfiguration
        if storeConfiguration:
            self.automaticUpdatePromptCheck()
        self.loadLastUpdateCheckDate()

        self.config["perPlayerArguments"] = self.perPlayerArgs
        self.config["mediaSearchDirectories"] = utils.convertMultilineStringToList(self.mediasearchTextEdit.toPlainText())
        self.config["trustedDomains"] = utils.convertMultilineStringToList(self.trusteddomainsTextEdit.toPlainText())

        if self.serverpassTextbox.isEnabled():
            self.config['password'] = self.serverpassTextbox.text()
        self.processWidget(self, lambda w: self.saveValues(w))
        if self.hostCombobox.currentText():
            self.config['host'] = self.hostCombobox.currentText() if ":" in self.hostCombobox.currentText() else self.hostCombobox.currentText() + ":" + str(constants.DEFAULT_PORT)
            self.config['host'] = self.config['host'].replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        else:
            self.config['host'] = None
        self.config['playerPath'] = str(self.safenormcaseandpath(self.executablepathCombobox.currentText()))
        self.config['language'] = str(self.languageCombobox.itemData(self.languageCombobox.currentIndex()))
        if self.mediapathTextbox.text() == "":
            self.config['file'] = None
        elif os.path.isfile(os.path.abspath(self.mediapathTextbox.text())):
            self.config['file'] = os.path.abspath(self.mediapathTextbox.text())
        else:
            self.config['file'] = str(self.mediapathTextbox.text())
        self.config['publicServers'] = self.publicServerAddresses
        self.config['room'] = self.roomsCombobox.currentText()
        if self.config['autosaveJoinsToList']:
            self.addRoomToList(self.config['room'])

        self.pressedclosebutton = False
        self.close()
        self.closed.emit()

    def closeEvent(self, event):
        if self.pressedclosebutton:
            super(ConfigDialog, self).closeEvent(event)
            self.closed.emit()
            sys.exit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            sys.exit()

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            dropfilepath = os.path.abspath(str(event.mimeData().urls()[0].toLocalFile()))
            if dropfilepath[-4:].lower() == ".exe":
                self.executablepathCombobox.setEditText(dropfilepath)
            else:
                self.mediapathTextbox.setText(dropfilepath)
                self.mediapathTextbox.show()
                self.mediapathLabel.show()
                self.mediabrowseButton.show()
                if not self.showmoreCheckbox.isChecked():
                    newHeight = self.connectionSettingsGroup.minimumSizeHint().height() + self.mediaplayerSettingsGroup.minimumSizeHint().height() + self.bottomButtonFrame.minimumSizeHint().height() + 3
                    if self.error:
                        newHeight += self.errorLabel.height() + 3
                    self.stackedFrame.setFixedHeight(newHeight)
                    self.adjustSize()
                    self.setFixedSize(self.sizeHint())

    def processWidget(self, container, torun):
        for widget in container.children():
            self.processWidget(widget, torun)
            if hasattr(widget, 'objectName') and widget.objectName() and widget.objectName()[:3] != "qt_":
                torun(widget)

    def loadTooltips(self, widget):
        tooltipName = widget.objectName().lower().split(constants.CONFIG_NAME_MARKER)[0] + "-tooltip"
        if tooltipName[:1] == constants.INVERTED_STATE_MARKER or tooltipName[:1] == constants.LOAD_SAVE_MANUALLY_MARKER:
            tooltipName = tooltipName[1:]
        widget.setToolTip(getMessage(tooltipName))

    def loadValues(self, widget):
        valueName = str(widget.objectName())
        if valueName[:1] == constants.LOAD_SAVE_MANUALLY_MARKER:
            return

        if isinstance(widget, QCheckBox) and widget.objectName():
            if valueName[:1] == constants.INVERTED_STATE_MARKER:
                valueName = valueName[1:]
                inverted = True
            else:
                inverted = False
            if self.config[valueName] is None:
                widget.setTristate(True)
                widget.setCheckState(Qt.PartiallyChecked)
                widget.stateChanged.connect(lambda: widget.setTristate(False))
            else:
                widget.setChecked(self.config[valueName] != inverted)
        elif isinstance(widget, QRadioButton):
            radioName, radioValue = valueName.split(constants.CONFIG_NAME_MARKER)[1].split(constants.CONFIG_VALUE_MARKER)
            if self.config[radioName] == radioValue:
                widget.setChecked(True)
        elif isinstance(widget, QLineEdit):
            widget.setText(self.config[valueName])

    def saveValues(self, widget):
        valueName = str(widget.objectName())
        if valueName[:1] == constants.LOAD_SAVE_MANUALLY_MARKER:
            return

        if isinstance(widget, QCheckBox) and widget.objectName():
            if widget.checkState() == Qt.PartiallyChecked:
                self.config[valueName] = None
            else:
                if valueName[:1] == constants.INVERTED_STATE_MARKER:
                    valueName = valueName[1:]
                    inverted = True
                else:
                    inverted = False
                self.config[valueName] = widget.isChecked() != inverted
        elif isinstance(widget, QRadioButton):
            radioName, radioValue = valueName.split(constants.CONFIG_NAME_MARKER)[1].split(constants.CONFIG_VALUE_MARKER)
            if widget.isChecked():
                self.config[radioName] = radioValue
        elif isinstance(widget, QLineEdit):
            self.config[valueName] = widget.text()

    def connectChildren(self, widget):
        widgetName = str(widget.objectName())
        if widgetName in self.subitems:
            widget.stateChanged.connect(lambda: self.updateSubwidgets(self, widget))
            self.updateSubwidgets(self, widget)

    def updateSubwidgets(self, container, parentwidget, subwidgets=None):
        widgetName = parentwidget.objectName()
        if not subwidgets:
            subwidgets = self.subitems[widgetName]
        for widget in container.children():
            self.updateSubwidgets(widget, parentwidget, subwidgets)
            if hasattr(widget, 'objectName') and widget.objectName() and widget.objectName() in subwidgets:
                widget.setDisabled(not parentwidget.isChecked())

    def addBasicTab(self):
        config = self.config
        playerpaths = self.playerpaths
        error = self.error
        if self.datacleared == True:
            error = constants.ERROR_MESSAGE_MARKER + "{}".format(getMessage("gui-data-cleared-notification"))
            self.error = error
        if config['host'] is None:
            host = ""
        elif ":" in config['host'] and '[' not in config['host']:
            host = config['host']
        else:
            host = config['host'] + ":" + str(config['port'])

        self.perPlayerArgs = self.config["perPlayerArguments"]
        self.mediaSearchDirectories = self.config["mediaSearchDirectories"]
        self.trustedDomains = self.config["trustedDomains"]

        self.connectionSettingsGroup = QtWidgets.QGroupBox(getMessage("connection-group-title"))
        self.loadSavedPublicServerList()
        self.hostCombobox = QtWidgets.QComboBox(self)
        if self.publicServers:
            i = 0
            for publicServer in self.publicServers:
                serverTitle = publicServer[0]
                serverAddressPort = publicServer[1]
                self.hostCombobox.addItem(serverAddressPort)
                self.hostCombobox.setItemData(i, serverTitle, Qt.ToolTipRole)
                if serverAddressPort not in self.publicServerAddresses:
                    self.publicServerAddresses.append(serverAddressPort)
                i += 1
        self.hostCombobox.setEditable(True)
        self.hostCombobox.setEditText(host)
        self.hostLabel = QLabel(getMessage("host-label"), self)
        self.usernameTextbox = QLineEdit(self)

        self.usernameTextbox.setObjectName("name")
        self.serverpassLabel = QLabel(getMessage("password-label"), self)
        self.roomsCombobox = QtWidgets.QComboBox(self)
        self.roomsCombobox.setEditable(True)
        caseSensitiveCompleter = QtWidgets.QCompleter("", self)
        caseSensitiveCompleter.setCaseSensitivity(Qt.CaseSensitive)
        self.roomsCombobox.setCompleter(caseSensitiveCompleter)
        self.fillRoomsCombobox()
        self.roomsCombobox.setEditText(config['room'])
        self.usernameLabel = QLabel(getMessage("name-label"), self)
        self.serverpassTextbox = QLineEdit(self)
        self.serverpassTextbox.setText(self.storedPassword)
        self.defaultroomLabel = QLabel(getMessage("room-label"), self)
        self.editRoomsButton = QtWidgets.QToolButton()
        self.editRoomsButton.setIcon(QtGui.QIcon(resourcespath + 'bullet_edit_centered.png'))
        self.editRoomsButton.setObjectName(constants.LOAD_SAVE_MANUALLY_MARKER + "edit-rooms")
        self.editRoomsButton.released.connect(self.openRoomsDialog)
        self.hostLabel.setObjectName("host")
        self.hostCombobox.setObjectName(constants.LOAD_SAVE_MANUALLY_MARKER + "host")
        self.usernameLabel.setObjectName("name")
        self.usernameTextbox.setObjectName("name")
        self.serverpassLabel.setObjectName("password")
        self.serverpassTextbox.setObjectName(constants.LOAD_SAVE_MANUALLY_MARKER + "password")
        self.hostCombobox.editTextChanged.connect(self.updatePasswordVisibilty)
        self.hostCombobox.currentIndexChanged.connect(self.updatePasswordVisibilty)
        self.defaultroomLabel.setObjectName("room")
        self.roomsCombobox.setObjectName("room")

        self.connectionSettingsLayout = QtWidgets.QGridLayout()
        self.connectionSettingsLayout.addWidget(self.hostLabel, 0, 0)
        self.connectionSettingsLayout.addWidget(self.hostCombobox, 0, 1)
        self.connectionSettingsLayout.addWidget(self.serverpassLabel, 1, 0)
        self.connectionSettingsLayout.addWidget(self.serverpassTextbox, 1, 1)
        self.connectionSettingsLayout.addWidget(self.usernameLabel, 2, 0)
        self.connectionSettingsLayout.addWidget(self.usernameTextbox, 2, 1)
        self.connectionSettingsLayout.addWidget(self.defaultroomLabel, 3, 0)
        self.connectionSettingsLayout.addWidget(self.editRoomsButton, 3, 2, Qt.AlignRight)
        self.connectionSettingsLayout.addWidget(self.roomsCombobox, 3, 1)
        self.connectionSettingsLayout.setSpacing(10)
        self.connectionSettingsGroup.setLayout(self.connectionSettingsLayout)
        if isMacOS():
            self.connectionSettingsGroup.setFixedHeight(self.connectionSettingsGroup.minimumSizeHint().height())
        else:
            self.connectionSettingsGroup.setMaximumHeight(self.connectionSettingsGroup.minimumSizeHint().height())

        self.playerargsTextbox = QLineEdit("", self)
        self.playerargsTextbox.textEdited.connect(self.changedPlayerArgs)
        self.playerargsLabel = QLabel(getMessage("player-arguments-label"), self)

        self.mediaplayerSettingsGroup = QtWidgets.QGroupBox(getMessage("media-setting-title"))
        self.executableiconImage = QtGui.QImage()
        self.executableiconLabel = QLabel(self)
        self.executableiconLabel.setFixedWidth(16)
        self.executableiconLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.executablepathCombobox = QtWidgets.QComboBox(self)
        self.executablepathCombobox.setEditable(True)
        self.executablepathCombobox.currentIndexChanged.connect(self.updateExecutableIcon)
        self.executablepathCombobox.setEditText(self._tryToFillPlayerPath(config['playerPath'], playerpaths))
        self.executablepathCombobox.editTextChanged.connect(self.updateExecutableIcon)

        self.executablepathLabel = QLabel(getMessage("executable-path-label"), self)
        self.executablebrowseButton = QtWidgets.QPushButton(QtGui.QIcon(resourcespath + 'folder_explore.png'), getMessage("browse-label"))
        self.executablebrowseButton.clicked.connect(self.browsePlayerpath)
        self.mediapathTextbox = QLineEdit(config['file'], self)
        self.mediapathLabel = QLabel(getMessage("media-path-label"), self)
        self.mediabrowseButton = QtWidgets.QPushButton(QtGui.QIcon(resourcespath + 'folder_explore.png'), getMessage("browse-label"))
        self.mediabrowseButton.clicked.connect(self.browseMediapath)

        self.executablepathLabel.setObjectName("executable-path")
        self.executablepathCombobox.setObjectName("executable-path")
        self.executablepathCombobox.setMinimumContentsLength(constants.EXECUTABLE_COMBOBOX_MINIMUM_LENGTH)
        if not IsPySide6:
            self.executablepathCombobox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        else:
            self.executablepathCombobox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.mediapathLabel.setObjectName("media-path")
        self.mediapathTextbox.setObjectName(constants.LOAD_SAVE_MANUALLY_MARKER + "media-path")
        self.playerargsLabel.setObjectName("player-arguments")
        self.playerargsTextbox.setObjectName(constants.LOAD_SAVE_MANUALLY_MARKER + "player-arguments")

        self.mediaplayerSettingsLayout = QtWidgets.QGridLayout()
        self.mediaplayerSettingsLayout.addWidget(self.executablepathLabel, 0, 0, 1, 1)
        self.mediaplayerSettingsLayout.addWidget(self.executableiconLabel, 0, 1, 1, 1)
        self.mediaplayerSettingsLayout.addWidget(self.executablepathCombobox, 0, 2, 1, 1)
        self.mediaplayerSettingsLayout.addWidget(self.executablebrowseButton, 0, 3, 1, 1)
        self.mediaplayerSettingsLayout.addWidget(self.mediapathLabel, 1, 0, 1, 2)
        self.mediaplayerSettingsLayout.addWidget(self.mediapathTextbox, 1, 2, 1, 1)
        self.mediaplayerSettingsLayout.addWidget(self.mediabrowseButton, 1, 3, 1, 1)
        self.mediaplayerSettingsLayout.addWidget(self.playerargsLabel, 2, 0, 1, 2)
        self.mediaplayerSettingsLayout.addWidget(self.playerargsTextbox, 2, 2, 1, 2)
        self.mediaplayerSettingsLayout.setSpacing(10)
        self.mediaplayerSettingsGroup.setLayout(self.mediaplayerSettingsLayout)

        iconWidth = self.executableiconLabel.minimumSize().width()+self.mediaplayerSettingsLayout.spacing()
        maxWidth = max(
            self.hostLabel.minimumSizeHint().width(),
            self.usernameLabel.minimumSizeHint().width(),
            self.serverpassLabel.minimumSizeHint().width(),
            self.defaultroomLabel.minimumSizeHint().width(),
            self.executablepathLabel.minimumSizeHint().width(),
            self.mediapathLabel.minimumSizeHint().width(),
            self.playerargsLabel.minimumSizeHint().width()
        )

        self.hostLabel.setMinimumWidth(maxWidth+iconWidth)
        self.usernameLabel.setMinimumWidth(maxWidth+iconWidth)
        self.serverpassLabel.setMinimumWidth(maxWidth+iconWidth)
        self.defaultroomLabel.setMinimumWidth(maxWidth+iconWidth)
        self.executablepathLabel.setMinimumWidth(maxWidth)
        self.mediapathLabel.setMinimumWidth(maxWidth+iconWidth)
        self.playerargsLabel.setMinimumWidth(maxWidth+iconWidth)

        self.showmoreCheckbox = QCheckBox(getMessage("more-title"))
        self.showmoreCheckbox.setObjectName(constants.LOAD_SAVE_MANUALLY_MARKER + "more")

        self.basicOptionsFrame = QtWidgets.QFrame()
        self.basicOptionsLayout = QtWidgets.QVBoxLayout()
        if error:
            error = str(error)
            self.errorLabel = QLabel(self)
            if error[:1] != constants.ERROR_MESSAGE_MARKER:
                self.errorLabel.setStyleSheet(constants.STYLE_ERRORLABEL)
            else:
                error = error[1:]
                self.errorLabel.setStyleSheet(constants.STYLE_SUCCESSLABEL)
            self.errorLabel.setText(error)
            self.errorLabel.setAlignment(Qt.AlignCenter)
            self.basicOptionsLayout.addWidget(self.errorLabel)
        self.connectionSettingsGroup.setMaximumHeight(self.connectionSettingsGroup.minimumSizeHint().height())
        self.basicOptionsLayout.setAlignment(Qt.AlignTop)
        self.basicOptionsLayout.addWidget(self.connectionSettingsGroup)
        self.basicOptionsLayout.addSpacing(5)
        self.basicOptionsLayout.addWidget(self.mediaplayerSettingsGroup)
        self.basicOptionsFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.basicOptionsFrame.setLayout(self.basicOptionsLayout)
        self.stackedLayout.addWidget(self.basicOptionsFrame)

    def addReadinessTab(self):
        self.readyFrame = QtWidgets.QFrame()
        self.readyLayout = QtWidgets.QVBoxLayout()
        self.readyFrame.setLayout(self.readyLayout)

        # Initial state

        self.readyInitialGroup = QtWidgets.QGroupBox(getMessage("readiness-title"))
        self.readyInitialLayout = QtWidgets.QVBoxLayout()
        self.readyInitialGroup.setLayout(self.readyInitialLayout)
        self.readyatstartCheckbox = QCheckBox(getMessage("readyatstart-label"))
        self.readyatstartCheckbox.setObjectName("readyAtStart")
        self.readyInitialLayout.addWidget(self.readyatstartCheckbox)
        self.readyLayout.addWidget(self.readyInitialGroup)

        # Automatically pausing
        self.readyPauseGroup = QtWidgets.QGroupBox(getMessage("pausing-title"))
        self.readyPauseLayout = QtWidgets.QVBoxLayout()
        self.readyPauseGroup.setLayout(self.readyPauseLayout)
        self.pauseonleaveCheckbox = QCheckBox(getMessage("pauseonleave-label"))
        self.pauseonleaveCheckbox.setObjectName("pauseOnLeave")
        self.readyPauseLayout.addWidget(self.pauseonleaveCheckbox)
        self.readyLayout.addWidget(self.readyPauseGroup)

        # Unpausing
        self.readyUnpauseGroup = QtWidgets.QGroupBox(getMessage("unpause-title"))
        self.readyUnpauseLayout = QtWidgets.QVBoxLayout()
        self.readyUnpauseGroup.setLayout(self.readyUnpauseLayout)
        self.readyUnpauseButtonGroup = QButtonGroup()
        self.unpauseIfAlreadyReadyOption = QRadioButton(getMessage("unpause-ifalreadyready-option"))
        self.readyUnpauseButtonGroup.addButton(self.unpauseIfAlreadyReadyOption)
        self.unpauseIfAlreadyReadyOption.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.unpauseIfAlreadyReadyOption.setObjectName("unpause-ifalreadyready" + constants.CONFIG_NAME_MARKER + "unpauseAction" + constants.CONFIG_VALUE_MARKER + constants.UNPAUSE_IFALREADYREADY_MODE)
        self.readyUnpauseLayout.addWidget(self.unpauseIfAlreadyReadyOption)
        self.unpauseIfOthersReadyOption = QRadioButton(getMessage("unpause-ifothersready-option"))
        self.readyUnpauseButtonGroup.addButton(self.unpauseIfOthersReadyOption)
        self.unpauseIfOthersReadyOption.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.unpauseIfOthersReadyOption.setObjectName("unpause-ifothersready" + constants.CONFIG_NAME_MARKER + "unpauseAction" + constants.CONFIG_VALUE_MARKER + constants.UNPAUSE_IFOTHERSREADY_MODE)
        self.readyUnpauseLayout.addWidget(self.unpauseIfOthersReadyOption)
        self.unpauseIfMinUsersReadyOption = QRadioButton(getMessage("unpause-ifminusersready-option"))
        self.readyUnpauseButtonGroup.addButton(self.unpauseIfMinUsersReadyOption)
        self.unpauseIfMinUsersReadyOption.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.unpauseIfMinUsersReadyOption.setObjectName("unpause-ifminusersready" + constants.CONFIG_NAME_MARKER + "unpauseAction" + constants.CONFIG_VALUE_MARKER + constants.UNPAUSE_IFMINUSERSREADY_MODE)
        self.readyUnpauseLayout.addWidget(self.unpauseIfMinUsersReadyOption)
        self.unpauseAlwaysUnpauseOption = QRadioButton(getMessage("unpause-always"))
        self.readyUnpauseButtonGroup.addButton(self.unpauseAlwaysUnpauseOption)
        self.unpauseAlwaysUnpauseOption.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.unpauseAlwaysUnpauseOption.setObjectName("unpause-always" + constants.CONFIG_NAME_MARKER + "unpauseAction" + constants.CONFIG_VALUE_MARKER + constants.UNPAUSE_ALWAYS_MODE)
        self.readyUnpauseLayout.addWidget(self.unpauseAlwaysUnpauseOption)
        self.readyLayout.addWidget(self.readyUnpauseGroup)

        self.readyLayout.setAlignment(Qt.AlignTop)
        self.stackedLayout.addWidget(self.readyFrame)

    def addMiscTab(self):
        self.miscFrame = QtWidgets.QFrame()
        self.miscLayout = QtWidgets.QVBoxLayout()
        self.miscFrame.setLayout(self.miscLayout)

        self.coreSettingsGroup = QtWidgets.QGroupBox(getMessage("core-behaviour-title"))
        self.coreSettingsLayout = QtWidgets.QGridLayout()
        self.coreSettingsGroup.setLayout(self.coreSettingsLayout)

        ### Privacy:

        self.filenameprivacyLabel = QLabel(getMessage("filename-privacy-label"), self)
        self.filenameprivacyButtonGroup = QButtonGroup()
        self.filenameprivacySendRawOption = QRadioButton(getMessage("privacy-sendraw-option"))
        self.filenameprivacySendHashedOption = QRadioButton(getMessage("privacy-sendhashed-option"))
        self.filenameprivacyDontSendOption = QRadioButton(getMessage("privacy-dontsend-option"))
        self.filenameprivacyButtonGroup.addButton(self.filenameprivacySendRawOption)
        self.filenameprivacyButtonGroup.addButton(self.filenameprivacySendHashedOption)
        self.filenameprivacyButtonGroup.addButton(self.filenameprivacyDontSendOption)

        self.filesizeprivacyLabel = QLabel(getMessage("filesize-privacy-label"), self)
        self.filesizeprivacyButtonGroup = QButtonGroup()
        self.filesizeprivacySendRawOption = QRadioButton(getMessage("privacy-sendraw-option"))
        self.filesizeprivacySendHashedOption = QRadioButton(getMessage("privacy-sendhashed-option"))
        self.filesizeprivacyDontSendOption = QRadioButton(getMessage("privacy-dontsend-option"))
        self.filesizeprivacyButtonGroup.addButton(self.filesizeprivacySendRawOption)
        self.filesizeprivacyButtonGroup.addButton(self.filesizeprivacySendHashedOption)
        self.filesizeprivacyButtonGroup.addButton(self.filesizeprivacyDontSendOption)

        self.filenameprivacyLabel.setObjectName("filename-privacy")
        self.filenameprivacySendRawOption.setObjectName("privacy-sendraw" + constants.CONFIG_NAME_MARKER + "filenamePrivacyMode" + constants.CONFIG_VALUE_MARKER + constants.PRIVACY_SENDRAW_MODE)
        self.filenameprivacySendHashedOption.setObjectName("privacy-sendhashed" + constants.CONFIG_NAME_MARKER + "filenamePrivacyMode" + constants.CONFIG_VALUE_MARKER + constants.PRIVACY_SENDHASHED_MODE)
        self.filenameprivacyDontSendOption.setObjectName("privacy-dontsend" + constants.CONFIG_NAME_MARKER + "filenamePrivacyMode" + constants.CONFIG_VALUE_MARKER + constants.PRIVACY_DONTSEND_MODE)
        self.filesizeprivacyLabel.setObjectName("filesize-privacy")
        self.filesizeprivacySendRawOption.setObjectName("privacy-sendraw" + constants.CONFIG_NAME_MARKER + "filesizePrivacyMode" + constants.CONFIG_VALUE_MARKER + constants.PRIVACY_SENDRAW_MODE)
        self.filesizeprivacySendHashedOption.setObjectName("privacy-sendhashed" + constants.CONFIG_NAME_MARKER + "filesizePrivacyMode" + constants.CONFIG_VALUE_MARKER + constants.PRIVACY_SENDHASHED_MODE)
        self.filesizeprivacyDontSendOption.setObjectName("privacy-dontsend" + constants.CONFIG_NAME_MARKER + "filesizePrivacyMode" + constants.CONFIG_VALUE_MARKER + constants.PRIVACY_DONTSEND_MODE)

        self.coreSettingsLayout.addWidget(self.filenameprivacyLabel, 3, 0)
        self.coreSettingsLayout.addWidget(self.filenameprivacySendRawOption, 3, 1, Qt.AlignLeft)
        self.coreSettingsLayout.addWidget(self.filenameprivacySendHashedOption, 3, 2, Qt.AlignLeft)
        self.coreSettingsLayout.addWidget(self.filenameprivacyDontSendOption, 3, 3, Qt.AlignLeft)
        self.coreSettingsLayout.addWidget(self.filesizeprivacyLabel, 4, 0)
        self.coreSettingsLayout.addWidget(self.filesizeprivacySendRawOption, 4, 1, Qt.AlignLeft)
        self.coreSettingsLayout.addWidget(self.filesizeprivacySendHashedOption, 4, 2, Qt.AlignLeft)
        self.coreSettingsLayout.addWidget(self.filesizeprivacyDontSendOption, 4, 3, Qt.AlignLeft)

        ## Syncplay internals

        self.internalSettingsGroup = QtWidgets.QGroupBox(getMessage("syncplay-internals-title"))
        self.internalSettingsLayout = QtWidgets.QVBoxLayout()
        self.internalSettingsGroup.setLayout(self.internalSettingsLayout)

        self.alwaysshowCheckbox = QCheckBox(getMessage("forceguiprompt-label"))
        self.alwaysshowCheckbox.setObjectName(constants.INVERTED_STATE_MARKER + "forceGuiPrompt")
        self.internalSettingsLayout.addWidget(self.alwaysshowCheckbox)

        self.automaticupdatesCheckbox = QCheckBox(getMessage("checkforupdatesautomatically-label"))
        self.automaticupdatesCheckbox.setObjectName("checkForUpdatesAutomatically")
        self.internalSettingsLayout.addWidget(self.automaticupdatesCheckbox)

        self.autosaveJoinsToListCheckbox = QCheckBox(getMessage("autosavejoinstolist-label"))
        self.autosaveJoinsToListCheckbox.setObjectName("autosaveJoinsToList")
        self.internalSettingsLayout.addWidget(self.autosaveJoinsToListCheckbox)

        ## Media path directories

        self.mediasearchSettingsGroup = QtWidgets.QGroupBox(getMessage("syncplay-mediasearchdirectories-title"))
        self.mediasearchSettingsLayout = QtWidgets.QVBoxLayout()
        self.mediasearchSettingsGroup.setLayout(self.mediasearchSettingsLayout)

        self.mediasearchTextEdit = QPlainTextEdit(utils.getListAsMultilineString(self.mediaSearchDirectories))
        self.mediasearchTextEdit.setObjectName(constants.LOAD_SAVE_MANUALLY_MARKER + "mediasearcdirectories-arguments")
        self.mediasearchTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.mediasearchSettingsLayout.addWidget(self.mediasearchTextEdit)
        self.mediasearchSettingsGroup.setMaximumHeight(self.mediasearchSettingsGroup.minimumSizeHint().height())

        self.miscLayout.addWidget(self.coreSettingsGroup)
        self.miscLayout.addWidget(self.internalSettingsGroup)
        self.miscLayout.addWidget(self.mediasearchSettingsGroup)
        self.miscLayout.setAlignment(Qt.AlignTop)
        self.stackedLayout.addWidget(self.miscFrame)

    def addSyncTab(self):
        self.syncSettingsFrame = QtWidgets.QFrame()
        self.syncSettingsLayout = QtWidgets.QVBoxLayout()

        self.desyncSettingsGroup = QtWidgets.QGroupBox(getMessage("sync-otherslagging-title"))
        self.desyncOptionsFrame = QtWidgets.QFrame()
        self.desyncSettingsOptionsLayout = QtWidgets.QHBoxLayout()
        config = self.config

        self.slowdownCheckbox = QCheckBox(getMessage("slowondesync-label"))
        self.slowdownCheckbox.setObjectName("slowOnDesync")
        self.rewindCheckbox = QCheckBox(getMessage("rewindondesync-label"))
        self.rewindCheckbox.setObjectName("rewindOnDesync")
        self.fastforwardCheckbox = QCheckBox(getMessage("fastforwardondesync-label"))
        self.fastforwardCheckbox.setObjectName("fastforwardOnDesync")

        self.desyncSettingsLayout = QtWidgets.QGridLayout()
        self.desyncSettingsLayout.setSpacing(2)
        self.desyncFrame = QtWidgets.QFrame()
        self.desyncFrame.setLineWidth(0)
        self.desyncFrame.setMidLineWidth(0)

        self.desyncSettingsLayout.addWidget(self.slowdownCheckbox, 0, 0, 1, 2, Qt.AlignLeft)
        self.desyncSettingsLayout.addWidget(self.rewindCheckbox, 1, 0, 1, 2, Qt.AlignLeft)

        self.desyncSettingsLayout.setAlignment(Qt.AlignLeft)
        self.desyncSettingsGroup.setLayout(self.desyncSettingsLayout)
        self.desyncSettingsOptionsLayout.addWidget(self.desyncFrame)

        self.desyncFrame.setLayout(self.syncSettingsLayout)

        self.othersyncSettingsGroup = QtWidgets.QGroupBox(getMessage("sync-youlaggging-title"))
        self.othersyncOptionsFrame = QtWidgets.QFrame()
        self.othersyncSettingsLayout = QtWidgets.QGridLayout()

        self.dontslowwithmeCheckbox = QCheckBox(getMessage("dontslowdownwithme-label"))
        self.dontslowwithmeCheckbox.setObjectName("dontSlowDownWithMe")

        self.othersyncSettingsLayout.addWidget(self.dontslowwithmeCheckbox, 2, 0, 1, 2, Qt.AlignLeft)

        self.othersyncSettingsLayout.setAlignment(Qt.AlignLeft)
        self.othersyncSettingsLayout.addWidget(self.fastforwardCheckbox, 3, 0, 1, 2, Qt.AlignLeft)

        ## Trusted domains

        self.trusteddomainsSettingsGroup = QtWidgets.QGroupBox(getMessage("syncplay-trusteddomains-title"))
        self.trusteddomainsSettingsLayout = QtWidgets.QVBoxLayout()
        self.trusteddomainsSettingsGroup.setLayout(self.trusteddomainsSettingsLayout)

        self.trusteddomainsTextEdit = QPlainTextEdit(utils.getListAsMultilineString(self.trustedDomains))
        self.trusteddomainsTextEdit.setObjectName(constants.LOAD_SAVE_MANUALLY_MARKER + "trusteddomains-arguments")
        self.trusteddomainsTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.trusteddomainsSettingsLayout.addWidget(self.trusteddomainsTextEdit)
        self.trusteddomainsSettingsGroup.setMaximumHeight(self.trusteddomainsSettingsGroup.minimumSizeHint().height())

        self.othersyncSettingsGroup.setLayout(self.othersyncSettingsLayout)
        self.othersyncSettingsGroup.setMaximumHeight(self.othersyncSettingsGroup.minimumSizeHint().height())
        self.syncSettingsLayout.addWidget(self.othersyncSettingsGroup)
        self.syncSettingsLayout.addWidget(self.desyncSettingsGroup)
        self.syncSettingsLayout.addWidget(self.trusteddomainsSettingsGroup)
        self.syncSettingsFrame.setLayout(self.syncSettingsLayout)
        self.desyncSettingsGroup.setMaximumHeight(self.desyncSettingsGroup.minimumSizeHint().height())
        self.syncSettingsLayout.setAlignment(Qt.AlignTop)
        self.stackedLayout.addWidget(self.syncSettingsFrame)

    def addChatTab(self):
        self.chatFrame = QtWidgets.QFrame()
        self.chatLayout = QtWidgets.QVBoxLayout()
        self.chatLayout.setAlignment(Qt.AlignTop)

        # Input
        self.chatInputGroup = QtWidgets.QGroupBox(getMessage("chat-title"))
        self.chatInputLayout = QtWidgets.QGridLayout()
        self.chatLayout.addWidget(self.chatInputGroup)
        self.chatInputGroup.setLayout(self.chatInputLayout)
        self.chatInputEnabledCheckbox = QCheckBox(getMessage("chatinputenabled-label"))
        self.chatInputEnabledCheckbox.setObjectName("chatInputEnabled")
        self.chatInputLayout.addWidget(self.chatInputEnabledCheckbox, 1, 0, 1, 1, Qt.AlignLeft)

        self.chatDirectInputCheckbox = QCheckBox(getMessage("chatdirectinput-label"))
        self.chatDirectInputCheckbox.setObjectName("chatDirectInput")
        self.chatDirectInputCheckbox.setStyleSheet(
            constants.STYLE_SUBCHECKBOX.format(self.posixresourcespath + "chevrons_right.png"))
        self.chatInputLayout.addWidget(self.chatDirectInputCheckbox, 2, 0, 1, 1, Qt.AlignLeft)

        self.inputFontLayout = QtWidgets.QHBoxLayout()
        self.inputFontLayout.setContentsMargins(0, 0, 0, 0)
        self.inputFontFrame = QtWidgets.QFrame()
        self.inputFontFrame.setLayout(self.inputFontLayout)
        self.inputFontFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.chatFontLabel = QLabel(getMessage("chatinputfont-label"), self)
        self.chatFontLabel.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(self.posixresourcespath + "chevrons_right.png"))
        self.chatFontLabel.setObjectName("font-label")
        self.chatInputFontButton = QtWidgets.QPushButton(getMessage("chatfont-label"))
        self.chatInputFontButton.setObjectName("set-input-font")
        self.chatInputFontButtonGroup = QtWidgets.QButtonGroup()
        self.chatInputFontButtonGroup.addButton(self.chatInputFontButton)
        self.chatInputFontButton.released.connect(lambda: self.fontDialog("chatInput"))
        self.chatInputColourButton = QtWidgets.QPushButton(getMessage("chatcolour-label"))
        self.chatInputColourButton.setObjectName("set-input-colour")
        self.chatInputColourButtonGroup = QtWidgets.QButtonGroup()
        self.chatInputColourButtonGroup.addButton(self.chatInputColourButton)
        self.chatInputColourButton.released.connect(lambda: self.colourDialog("chatInput"))
        self.inputFontLayout.addWidget(self.chatFontLabel, Qt.AlignLeft)
        self.inputFontLayout.addWidget(self.chatInputFontButton, Qt.AlignLeft)
        self.inputFontLayout.addWidget(self.chatInputColourButton, Qt.AlignLeft)
        self.chatInputLayout.addWidget(self.inputFontFrame, 3, 0, 1, 3, Qt.AlignLeft)

        self.chatInputPositionFrame = QtWidgets.QFrame()
        self.chatInputPositionLayout = QtWidgets.QHBoxLayout()
        self.chatInputPositionLayout.setContentsMargins(0, 0, 0, 0)
        self.chatInputPositionFrame.setLayout(self.chatInputPositionLayout)
        self.chatInputPositionFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.chatInputPositionLabel = QLabel(getMessage("chatinputposition-label"), self)
        self.chatInputPositionLabel.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(self.posixresourcespath + "chevrons_right.png"))
        self.chatInputPositionGroup = QButtonGroup()
        self.chatInputTopOption = QRadioButton(getMessage("chat-top-option"))
        self.chatInputMiddleOption = QRadioButton(getMessage("chat-middle-option"))
        self.chatInputBottomOption = QRadioButton(getMessage("chat-bottom-option"))
        self.chatInputPositionGroup.addButton(self.chatInputTopOption)
        self.chatInputPositionGroup.addButton(self.chatInputMiddleOption)
        self.chatInputPositionGroup.addButton(self.chatInputBottomOption)

        self.chatInputPositionLabel.setObjectName("chatinputposition")
        self.chatInputTopOption.setObjectName("chatinputposition-top" + constants.CONFIG_NAME_MARKER + "chatInputPosition" + constants.CONFIG_VALUE_MARKER + constants.INPUT_POSITION_TOP)
        self.chatInputMiddleOption.setObjectName("chatinputposition-middle" + constants.CONFIG_NAME_MARKER + "chatInputPosition" + constants.CONFIG_VALUE_MARKER + constants.INPUT_POSITION_MIDDLE)
        self.chatInputBottomOption.setObjectName("chatinputposition-bottom" + constants.CONFIG_NAME_MARKER + "chatInputPosition" + constants.CONFIG_VALUE_MARKER + constants.INPUT_POSITION_BOTTOM)

        self.chatInputPositionLayout.addWidget(self.chatInputPositionLabel)
        self.chatInputPositionLayout.addWidget(self.chatInputTopOption)
        self.chatInputPositionLayout.addWidget(self.chatInputMiddleOption)
        self.chatInputPositionLayout.addWidget(self.chatInputBottomOption)
        self.chatInputLayout.addWidget(self.chatInputPositionFrame)

        self.subitems['chatInputEnabled'] = [self.chatInputPositionLabel.objectName(), self.chatInputTopOption.objectName(),
                                             self.chatInputMiddleOption.objectName(), self.chatInputBottomOption.objectName(),
                                             self.chatInputFontButton.objectName(), self.chatFontLabel.objectName(),
                                             self.chatInputColourButton.objectName(), self.chatDirectInputCheckbox.objectName()]
        # Output
        self.chatOutputGroup = QtWidgets.QGroupBox(getMessage("chatoutputheader-label"))
        self.chatOutputLayout = QtWidgets.QGridLayout()
        self.chatLayout.addWidget(self.chatOutputGroup)
        self.chatOutputGroup.setLayout(self.chatOutputLayout)
        self.chatOutputEnabledCheckbox = QCheckBox(getMessage("chatoutputenabled-label"))
        self.chatOutputEnabledCheckbox.setObjectName("chatOutputEnabled")
        self.chatOutputLayout.addWidget(self.chatOutputEnabledCheckbox, 1, 0, 1, 1, Qt.AlignLeft)

        self.outputFontLayout = QtWidgets.QHBoxLayout()
        self.outputFontLayout.setContentsMargins(0, 0, 0, 0)
        self.outputFontFrame = QtWidgets.QFrame()
        self.outputFontFrame.setLayout(self.outputFontLayout)
        self.outputFontFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.chatOutputFontLabel = QLabel(getMessage("chatoutputfont-label"), self)
        self.chatOutputFontLabel.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(self.posixresourcespath + "chevrons_right.png"))
        self.chatOutputFontLabel.setObjectName("font-output-label")
        self.chatOutputFontButton = QtWidgets.QPushButton(getMessage("chatfont-label"))
        self.chatOutputFontButton.setObjectName("set-output-font")
        self.chatOutputFontButtonGroup = QtWidgets.QButtonGroup()
        self.chatOutputFontButtonGroup.addButton(self.chatOutputFontButton)
        self.chatOutputFontButton.released.connect(lambda: self.fontDialog("chatOutput"))
        self.chatOutputColourButton = QtWidgets.QPushButton(getMessage("chatcolour-label"))
        self.outputFontLayout.addWidget(self.chatOutputFontLabel, Qt.AlignLeft)
        self.outputFontLayout.addWidget(self.chatOutputFontButton, Qt.AlignLeft)
        self.chatOutputLayout.addWidget(self.outputFontFrame, 2, 0, 1, 3, Qt.AlignLeft)

        self.chatOutputModeLabel = QLabel(getMessage("chatoutputposition-label"), self)
        self.chatOutputModeLabel.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(self.posixresourcespath + "chevrons_right.png"))
        self.chatOutputModeGroup = QButtonGroup()
        self.chatOutputChatroomOption = QRadioButton(getMessage("chat-chatroom-option"))
        self.chatOutputScrollingOption = QRadioButton(getMessage("chat-scrolling-option"))
        self.chatOutputModeGroup.addButton(self.chatOutputChatroomOption)
        self.chatOutputModeGroup.addButton(self.chatOutputScrollingOption)

        self.chatOutputModeLabel.setObjectName("chatoutputmode")
        self.chatOutputChatroomOption.setObjectName("chatoutputmode-chatroom" + constants.CONFIG_NAME_MARKER + "chatOutputMode" + constants.CONFIG_VALUE_MARKER + constants.CHATROOM_MODE)
        self.chatOutputScrollingOption.setObjectName("chatoutputmode-scrolling" + constants.CONFIG_NAME_MARKER + "chatOutputMode" + constants.CONFIG_VALUE_MARKER + constants.SCROLLING_MODE)

        self.chatOutputModeFrame = QtWidgets.QFrame()
        self.chatOutputModeLayout = QtWidgets.QHBoxLayout()
        self.chatOutputModeLayout.setContentsMargins(0, 0, 0, 0)
        self.chatOutputModeFrame.setLayout(self.chatOutputModeLayout)
        self.chatOutputModeFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.chatOutputModeLayout.addWidget(self.chatOutputModeLabel)
        self.chatOutputModeLayout.addWidget(self.chatOutputChatroomOption)
        self.chatOutputModeLayout.addWidget(self.chatOutputScrollingOption)
        self.chatOutputLayout.addWidget(self.chatOutputModeFrame)

        self.subitems['chatOutputEnabled'] = [self.chatOutputModeLabel.objectName(), self.chatOutputChatroomOption.objectName(),
                                              self.chatOutputScrollingOption.objectName(), self.chatOutputFontButton.objectName(),
                                              self.chatOutputFontLabel.objectName()]
        # chatFrame
        self.chatFrame.setLayout(self.chatLayout)
        self.stackedLayout.addWidget(self.chatFrame)

    def fontDialog(self, configName):
            font = QtGui.QFont()
            font.setFamily(self.config[configName + "FontFamily"])
            font.setPointSize(self.config[configName + "RelativeFontSize"])
            font.setWeight(self.config[configName + "FontWeight"])
            font.setUnderline(self.config[configName + "FontUnderline"])
            ok, value = QtWidgets.QFontDialog.getFont(font)
            if ok:
                self.config[configName + "FontFamily"] = value.family()
                self.config[configName + "RelativeFontSize"] = value.pointSize()
                self.config[configName + "FontWeight"] = value.weight()
                self.config[configName + "FontUnderline"] = value.underline()

    def colourDialog(self, configName):
            oldColour = QtGui.QColor()
            oldColour.setNamedColor(self.config[configName + "FontColor"])
            colour = QtWidgets.QColorDialog.getColor(oldColour, self)
            if colour.isValid():
                self.config[configName + "FontColor"] = colour.name()

    def addMessageTab(self):
        self.messageFrame = QtWidgets.QFrame()
        self.messageLayout = QtWidgets.QVBoxLayout()
        self.messageLayout.setAlignment(Qt.AlignTop)

        # OSD
        self.osdSettingsGroup = QtWidgets.QGroupBox(getMessage("messages-osd-title"))
        self.osdSettingsLayout = QtWidgets.QVBoxLayout()
        self.osdSettingsFrame = QtWidgets.QFrame()

        self.showOSDCheckbox = QCheckBox(getMessage("showosd-label"))
        self.showOSDCheckbox.setObjectName("showOSD")
        self.osdSettingsLayout.addWidget(self.showOSDCheckbox)

        self.showSameRoomOSDCheckbox = QCheckBox(getMessage("showsameroomosd-label"))
        self.showSameRoomOSDCheckbox.setObjectName("showSameRoomOSD")
        self.showSameRoomOSDCheckbox.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.osdSettingsLayout.addWidget(self.showSameRoomOSDCheckbox)

        self.showNonControllerOSDCheckbox = QCheckBox(getMessage("shownoncontrollerosd-label"))
        self.showNonControllerOSDCheckbox.setObjectName("showNonControllerOSD")
        self.showNonControllerOSDCheckbox.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.osdSettingsLayout.addWidget(self.showNonControllerOSDCheckbox)

        self.showDifferentRoomOSDCheckbox = QCheckBox(getMessage("showdifferentroomosd-label"))
        self.showDifferentRoomOSDCheckbox.setObjectName("showDifferentRoomOSD")
        self.showDifferentRoomOSDCheckbox.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.osdSettingsLayout.addWidget(self.showDifferentRoomOSDCheckbox)

        self.slowdownOSDCheckbox = QCheckBox(getMessage("showslowdownosd-label"))
        self.slowdownOSDCheckbox.setObjectName("showSlowdownOSD")
        self.slowdownOSDCheckbox.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.osdSettingsLayout.addWidget(self.slowdownOSDCheckbox)

        self.showOSDWarningsCheckbox = QCheckBox(getMessage("showosdwarnings-label"))
        self.showOSDWarningsCheckbox.setObjectName("showOSDWarnings")
        self.showOSDWarningsCheckbox.setStyleSheet(constants.STYLE_SUBCHECKBOX.format(posixresourcespath + "chevrons_right.png"))
        self.osdSettingsLayout.addWidget(self.showOSDWarningsCheckbox)

        self.subitems['showOSD'] = ["showSameRoomOSD", "showDifferentRoomOSD", "showSlowdownOSD", "showOSDWarnings", "showNonControllerOSD"]

        self.osdSettingsGroup.setLayout(self.osdSettingsLayout)
        self.osdSettingsGroup.setMaximumHeight(self.osdSettingsGroup.minimumSizeHint().height())
        self.osdSettingsLayout.setAlignment(Qt.AlignTop)
        self.messageLayout.addWidget(self.osdSettingsGroup)

        # Other display

        self.displaySettingsGroup = QtWidgets.QGroupBox(getMessage("messages-other-title"))
        self.displaySettingsLayout = QtWidgets.QVBoxLayout()
        self.displaySettingsLayout.setAlignment(Qt.AlignTop & Qt.AlignLeft)
        self.displaySettingsFrame = QtWidgets.QFrame()

        self.showDurationNotificationCheckbox = QCheckBox(getMessage("showdurationnotification-label"))
        self.showDurationNotificationCheckbox.setObjectName("showDurationNotification")
        self.displaySettingsLayout.addWidget(self.showDurationNotificationCheckbox)

        self.languageFrame = QtWidgets.QFrame()
        self.languageLayout = QtWidgets.QHBoxLayout()
        self.languageLayout.setContentsMargins(0, 0, 0, 0)
        self.languageFrame.setLayout(self.languageLayout)
        self.languageFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.languageLayout.setAlignment(Qt.AlignTop & Qt.AlignLeft)
        self.languageLabel = QLabel(getMessage("language-label"), self)
        self.languageCombobox = QtWidgets.QComboBox(self)
        self.languageCombobox.addItem(getMessage("automatic-language").format(getMessage("LANGUAGE", getInitialLanguage())))

        self.languages = getLanguages()
        for lang in self.languages:
            self.languageCombobox.addItem(self.languages[lang], lang)
            if lang == self.config['language']:
                self.languageCombobox.setCurrentIndex(self.languageCombobox.count()-1)
        self.languageCombobox.currentIndexChanged.connect(self.languageChanged)
        self.languageLayout.addWidget(self.languageLabel, 1, Qt.AlignLeft)
        self.languageLayout.addWidget(self.languageCombobox, 1, Qt.AlignLeft)
        self.displaySettingsLayout.addWidget(self.languageFrame)

        self.languageLabel.setObjectName("language")
        self.languageCombobox.setObjectName("language")
        self.languageFrame.setMaximumWidth(self.languageFrame.minimumSizeHint().width())

        self.displaySettingsGroup.setLayout(self.displaySettingsLayout)
        self.displaySettingsGroup.setMaximumHeight(self.displaySettingsGroup.minimumSizeHint().height())
        self.displaySettingsLayout.setAlignment(Qt.AlignTop & Qt.AlignLeft)
        self.messageLayout.addWidget(self.displaySettingsGroup)

        # messageFrame
        self.messageFrame.setLayout(self.messageLayout)
        self.stackedLayout.addWidget(self.messageFrame)

    def addBottomLayout(self):
        config = self.config

        self.bottomButtonFrame = QtWidgets.QFrame()
        self.bottomButtonLayout = QtWidgets.QHBoxLayout()
        self.helpButton = QtWidgets.QPushButton(QtGui.QIcon(resourcespath + 'help.png'), getMessage("help-label"))
        self.helpButton.setObjectName("help")
        self.helpButton.setMaximumSize(self.helpButton.sizeHint())
        self.helpButton.released.connect(self.openHelp)

        self.resetButton = QtWidgets.QPushButton(QtGui.QIcon(resourcespath + 'cog_delete.png'), getMessage("reset-label"))
        self.resetButton.setMaximumSize(self.resetButton.sizeHint())
        self.resetButton.setObjectName("reset")
        self.resetButton.released.connect(self.resetSettings)

        self.runButton = QtWidgets.QPushButton(QtGui.QIcon(resourcespath + 'accept.png'), getMessage("run-label"))
        self.runButton.released.connect(self._runWithoutStoringConfig)
        self.runButton = QtWidgets.QPushButton(QtGui.QIcon(resourcespath + 'accept.png'), getMessage("run-label"))
        self.runButton.pressed.connect(self._runWithoutStoringConfig)
        self.runButton.setToolTip(getMessage("nostore-tooltip"))
        self.storeAndRunButton = QtWidgets.QPushButton(QtGui.QIcon(resourcespath + 'accept.png'), getMessage("storeandrun-label"))
        self.storeAndRunButton.released.connect(self._saveDataAndLeave)
        self.bottomButtonLayout.addWidget(self.helpButton)
        self.bottomButtonLayout.addWidget(self.resetButton)
        self.bottomButtonLayout.addWidget(self.runButton)
        self.bottomButtonLayout.addWidget(self.storeAndRunButton)
        self.bottomButtonFrame.setLayout(self.bottomButtonLayout)
        if isMacOS():
            self.bottomButtonLayout.setContentsMargins(15, 0, 15, 0)
        else:
            self.bottomButtonLayout.setContentsMargins(5, 0, 5, 0)
        self.mainLayout.addWidget(self.bottomButtonFrame, 1, 0, 1, 2)

        self.bottomCheckboxFrame = QtWidgets.QFrame()
        if isMacOS():
            self.bottomCheckboxFrame.setContentsMargins(3, 0, 6, 0)
        else:
            self.bottomCheckboxFrame.setContentsMargins(0, 0, 0, 0)
        self.bottomCheckboxLayout = QtWidgets.QGridLayout()
        self.alwaysshowCheckbox = QCheckBox(getMessage("forceguiprompt-label"))

        self.enableplaylistsCheckbox = QCheckBox(getMessage("sharedplaylistenabled-label"))
        self.bottomCheckboxLayout.addWidget(self.showmoreCheckbox)
        self.bottomCheckboxLayout.addWidget(self.enableplaylistsCheckbox, 0, 2, Qt.AlignRight)
        self.alwaysshowCheckbox.setObjectName(constants.INVERTED_STATE_MARKER + "forceGuiPrompt")
        self.enableplaylistsCheckbox.setObjectName("sharedPlaylistEnabled")
        self.bottomCheckboxFrame.setLayout(self.bottomCheckboxLayout)

        self.mainLayout.addWidget(self.bottomCheckboxFrame, 2, 0, 1, 2)

    def tabList(self):
        self.tabListLayout = QtWidgets.QHBoxLayout()
        self.tabListFrame = QtWidgets.QFrame()
        self.tabListWidget = QtWidgets.QListWidget()
        self.tabListWidget.addItem(QtWidgets.QListWidgetItem(QtGui.QIcon(resourcespath + "house.png"), getMessage("basics-label")))
        self.tabListWidget.addItem(QtWidgets.QListWidgetItem(QtGui.QIcon(resourcespath + "control_pause_blue.png"), getMessage("readiness-label")))
        self.tabListWidget.addItem(QtWidgets.QListWidgetItem(QtGui.QIcon(resourcespath + "film_link.png"), getMessage("sync-label")))
        self.tabListWidget.addItem(QtWidgets.QListWidgetItem(QtGui.QIcon(resourcespath + "user_comment.png"), getMessage("chat-label")))
        self.tabListWidget.addItem(QtWidgets.QListWidgetItem(QtGui.QIcon(resourcespath + "error.png"), getMessage("messages-label")))
        self.tabListWidget.addItem(QtWidgets.QListWidgetItem(QtGui.QIcon(resourcespath + "cog.png"), getMessage("misc-label")))
        self.tabListLayout.addWidget(self.tabListWidget)
        self.tabListFrame.setLayout(self.tabListLayout)
        self.tabListFrame.setFixedWidth(self.tabListFrame.minimumSizeHint().width() + constants.TAB_PADDING)
        self.tabListWidget.setStyleSheet(constants.STYLE_TABLIST)

        self.tabListWidget.currentItemChanged.connect(self.tabChange)
        self.tabListWidget.itemClicked.connect(self.tabChange)
        self.tabListWidget.itemPressed.connect(self.tabChange)
        self.mainLayout.addWidget(self.tabListFrame, 0, 0, 1, 1)

    def ensureTabListIsVisible(self):
        self.stackedFrame.setFixedWidth(self.stackedFrame.width())
        while self.tabListWidget.horizontalScrollBar().isVisible() and self.tabListFrame.width() < constants.MAXIMUM_TAB_WIDTH:
            self.tabListFrame.setFixedWidth(self.tabListFrame.width()+1)

    def tabChange(self):
        self.setFocus()
        self.stackedLayout.setCurrentIndex(self.tabListWidget.currentRow())

    def resetSettings(self):
        self.clearGUIData(leaveMore=True)
        self.config['resetConfig'] = True
        self.pressedclosebutton = False
        self.close()
        self.closed.emit()

    def showEvent(self, *args, **kwargs):
        self.ensureTabListIsVisible()
        self.setFixedWidth(self.minimumSizeHint().width())

    def clearGUIData(self, leaveMore=False):
        settings = QSettings("Syncplay", "PlayerList")
        settings.clear()
        settings = QSettings("Syncplay", "MediaBrowseDialog")
        settings.clear()
        settings = QSettings("Syncplay", "MainWindow")
        settings.clear()
        settings = QSettings("Syncplay", "Interface")
        settings.beginGroup("Update")
        settings.setValue("lastChecked", None)
        settings.setValue("lastCheckedQt", None)
        settings.endGroup()
        settings.beginGroup("PublicServerList")
        settings.setValue("publicServers", None)
        settings.endGroup()
        if not leaveMore:
            settings = QSettings("Syncplay", "MoreSettings")
            settings.clear()
        self.datacleared = True

    def populateEmptyServerList(self):
        if self.publicServers is None:
            if self.config["checkForUpdatesAutomatically"] == True:
                self.updateServerList()
            else:
                currentServer = self.hostCombobox.currentText()
                self.publicServers = constants.FALLBACK_PUBLIC_SYNCPLAY_SERVERS
                i = 0
                for server in self.publicServers:
                    self.hostCombobox.addItem(server[1])
                    self.hostCombobox.setItemData(i, server[0], Qt.ToolTipRole)
                    if not server[1] in self.publicServerAddresses:
                        self.publicServerAddresses.append(server[1])
                    i += 1
                self.hostCombobox.setEditText(currentServer)

    def updatePasswordVisibilty(self):
        if (self.hostCombobox.currentText() == "" and self.serverpassTextbox.text() == "") or str(self.hostCombobox.currentText()) in self.publicServerAddresses:
            self.serverpassTextbox.setDisabled(True)
            self.serverpassTextbox.setReadOnly(True)
            if self.serverpassTextbox.text() != "":
                self.storedPassword = self.serverpassTextbox.text()
            self.serverpassTextbox.setText("")
        else:
            self.serverpassTextbox.setEnabled(True)
            self.serverpassTextbox.setReadOnly(False)
            self.serverpassTextbox.setText(self.storedPassword)

    def createMenubar(self):
        self.menuBar = QtWidgets.QMenuBar()

        # Edit menu
        self.editMenu = QtWidgets.QMenu(getMessage("edit-menu-label"), self)

        self.cutAction = self.editMenu.addAction(getMessage("cut-menu-label"))
        self.cutAction.setShortcuts(QtGui.QKeySequence.Cut)

        self.copyAction = self.editMenu.addAction(getMessage("copy-menu-label"))
        self.copyAction.setShortcuts(QtGui.QKeySequence.Copy)

        self.pasteAction = self.editMenu.addAction(getMessage("paste-menu-label"))
        self.pasteAction.setShortcuts(QtGui.QKeySequence.Paste)

        self.selectAction = self.editMenu.addAction(getMessage("selectall-menu-label"))
        self.selectAction.setShortcuts(QtGui.QKeySequence.SelectAll)

        self.editMenu.addSeparator()

        self.menuBar.addMenu(self.editMenu)

        self.mainLayout.setMenuBar(self.menuBar)

    def __init__(self, config, playerpaths, error, defaultConfig):
        self.config = config
        self.defaultConfig = defaultConfig
        self.playerpaths = playerpaths
        self.datacleared = False
        self.config['resetConfig'] = False
        self.subitems = {}
        self.publicServers = None
        self.publicServerAddresses = []

        self._playerProbeThread = GetPlayerIconThread()
        self._playerProbeThread.done.connect(self._updateExecutableIcon)
        self._playerProbeThread.start()

        if self.config['clearGUIData'] == True:
            self.config['clearGUIData'] = False
            self.clearGUIData()

        self.QtWidgets = QtWidgets
        self.QtGui = QtGui
        self.error = error
        if isWindows():
            resourcespath = utils.findWorkingDir() + "\\resources\\"
        else:
            resourcespath = utils.findWorkingDir() + "/resources/"
        self.posixresourcespath = utils.findWorkingDir().replace("\\", "/") + "/resources/"
        self.resourcespath = resourcespath

        super(ConfigDialog, self).__init__()

        self.setWindowTitle(getMessage("config-window-title"))
        self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QtGui.QIcon(resourcespath + "syncplay.png"))

        self.stackedLayout = QtWidgets.QStackedLayout()
        self.stackedFrame = QtWidgets.QFrame()
        self.stackedFrame.setLayout(self.stackedLayout)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.storedPassword = self.config['password']
        self.addBasicTab()
        self.addReadinessTab()
        self.addSyncTab()
        self.addChatTab()
        self.addMessageTab()
        self.addMiscTab()
        self.tabList()

        if isMacOS():
            self.createMenubar()
            self.config['menuBar'] = dict()
            self.config['menuBar']['bar'] = self.menuBar
            self.config['menuBar']['editMenu'] = self.editMenu
        else:
            self.config['menuBar'] = None

        self.mainLayout.addWidget(self.stackedFrame, 0, 1)
        self.addBottomLayout()
        self.updatePasswordVisibilty()

        if self.getMoreState() == False:
            self.tabListFrame.hide()
            self.resetButton.hide()
            self.playerargsTextbox.hide()
            self.playerargsLabel.hide()
            self.runButton.hide()
            if self.mediapathTextbox.text() == "":
                self.mediapathTextbox.hide()
                self.mediapathLabel.hide()
                self.mediabrowseButton.hide()
            else:
                self.mediapathTextbox.show()
                self.mediapathLabel.show()
                self.mediabrowseButton.show()
            if isMacOS():
                newHeight = self.connectionSettingsGroup.minimumSizeHint().height()+self.mediaplayerSettingsGroup.minimumSizeHint().height()+self.bottomButtonFrame.minimumSizeHint().height()+50
            else:
                newHeight = self.connectionSettingsGroup.minimumSizeHint().height()+self.mediaplayerSettingsGroup.minimumSizeHint().height()+self.bottomButtonFrame.minimumSizeHint().height()+13
            if self.error:
                newHeight += self.errorLabel.height() + 3
            self.stackedFrame.setFixedHeight(newHeight)
        else:
            self.showmoreCheckbox.setChecked(True)
            self.tabListWidget.setCurrentRow(0)
            self.stackedFrame.setFixedHeight(self.stackedFrame.minimumSizeHint().height())


        self.showmoreCheckbox.toggled.connect(self.moreToggled)

        self.setLayout(self.mainLayout)
        if self.config['noStore']:
            self.runButton.setFocus()
        else:
            self.storeAndRunButton.setFocus()
        if isMacOS():
            initialHeight = self.connectionSettingsGroup.minimumSizeHint().height()+self.mediaplayerSettingsGroup.minimumSizeHint().height()+self.bottomButtonFrame.minimumSizeHint().height()+50
            if self.error:
                initialHeight += 40
            self.setFixedWidth(self.sizeHint().width())
            self.setFixedHeight(initialHeight)
        else:
            self.setFixedSize(self.sizeHint())
        self.setAcceptDrops(True)

        if constants.SHOW_TOOLTIPS:
            self.processWidget(self, lambda w: self.loadTooltips(w))
        self.processWidget(self, lambda w: self.loadValues(w))
        self.processWidget(self, lambda w: self.connectChildren(w))
        self.populateEmptyServerList()
