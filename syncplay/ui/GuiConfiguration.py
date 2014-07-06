from PySide import QtCore, QtGui
from PySide.QtCore import QSettings, Qt, QCoreApplication
from PySide.QtGui import QApplication, QLineEdit, QCursor, QLabel, QCheckBox, QDesktopServices, QIcon, QImage, QButtonGroup, QRadioButton, QDoubleSpinBox
from syncplay.players.playerFactory import PlayerFactory

import os
import sys
from syncplay.messages import getMessage
from syncplay import constants

class GuiConfiguration:
    def __init__(self, config, error=None):
        self.config = config
        self._availablePlayerPaths = []
        self.error = error


    def run(self):
        if QCoreApplication.instance() is None:
            self.app = QtGui.QApplication(sys.argv)
        dialog = ConfigDialog(self.config, self._availablePlayerPaths, self.error)
        dialog.exec_()

    def setAvailablePaths(self, paths):
        self._availablePlayerPaths = paths

    def getProcessedConfiguration(self):
        return self.config

    class WindowClosed(Exception):
        pass

class ConfigDialog(QtGui.QDialog):

    pressedclosebutton = False
    moreToggling = False

    def moreToggled(self):
        if self.moreToggling == False:
            self.moreToggling = True

            if self.showmoreCheckbox.isChecked() and self.showmoreCheckbox.isVisible():
                self.showmoreCheckbox.setChecked(False)
                self.moreSettingsGroup.setChecked(True)
                self.moreSettingsGroup.show()
                self.showmoreCheckbox.hide()
                self.saveMoreState(True)
            else:
                self.moreSettingsGroup.setChecked(False)
                self.moreSettingsGroup.hide()
                self.showmoreCheckbox.show()
                self.saveMoreState(False)

            self.moreToggling = False
            self.adjustSize()
            self.setFixedSize(self.sizeHint())

    def runButtonTextUpdate(self):
        if self.nostoreCheckbox.isChecked():
            self.runButton.setText(getMessage("run-label"))
        else:
            self.runButton.setText(getMessage("storeandrun-label"))

    def openHelp(self):
        self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/client/")

    def _tryToFillPlayerPath(self, playerpath, playerpathlist):
        settings = QSettings("Syncplay", "PlayerList")
        settings.beginGroup("PlayerList")
        savedPlayers = settings.value("PlayerList", [])
        if not isinstance(savedPlayers, list):
            savedPlayers = []
        playerpathlist = list(set(os.path.normcase(os.path.normpath(path)) for path in set(playerpathlist + savedPlayers)))
        settings.endGroup()
        foundpath = ""

        if playerpath != None and playerpath != "":
            if not os.path.isfile(playerpath):
                expandedpath = PlayerFactory().getExpandedPlayerPathByPath(playerpath)
                if expandedpath != None and os.path.isfile(expandedpath):
                    playerpath = expandedpath

            if os.path.isfile(playerpath):
                foundpath = playerpath
                self.executablepathCombobox.addItem(foundpath)

        for path in playerpathlist:
            if os.path.isfile(path) and os.path.normcase(os.path.normpath(path)) != os.path.normcase(os.path.normpath(foundpath)):
                self.executablepathCombobox.addItem(path)
                if foundpath == "":
                    foundpath = path

        if foundpath != "":
            settings.beginGroup("PlayerList")
            playerpathlist.append(os.path.normcase(os.path.normpath(foundpath)))
            settings.setValue("PlayerList", list(set(os.path.normcase(os.path.normpath(path)) for path in set(playerpathlist))))
            settings.endGroup()
        return foundpath

    def updateExecutableIcon(self):
        currentplayerpath = unicode(self.executablepathCombobox.currentText())
        iconpath = PlayerFactory().getPlayerIconByPath(currentplayerpath)
        if iconpath != None and iconpath != "":
            self.executableiconImage.load(self.resourcespath + iconpath)
            self.executableiconLabel.setPixmap(QtGui.QPixmap.fromImage(self.executableiconImage))
        else:
            self.executableiconLabel.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage()))


    def browsePlayerpath(self):
        options = QtGui.QFileDialog.Options()
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
        elif sys.platform.startswith('linux'):
            defaultdirectory = "/usr/bin"
        elif sys.platform.startswith('darwin'):
            defaultdirectory = "/Applications/"

        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self,
                "Browse for media player executable",
                defaultdirectory,
                browserfilter, "", options)
        if fileName:
            self.executablepathCombobox.setEditText(os.path.normpath(fileName))

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
        morestate = unicode.lower(unicode(settings.value("ShowMoreSettings", "false")))
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

    def browseMediapath(self):
        self.loadMediaBrowseSettings()
        options = QtGui.QFileDialog.Options()
        if os.path.isdir(self.mediadirectory):
            defaultdirectory = self.mediadirectory
        elif os.path.isdir(QDesktopServices.storageLocation(QDesktopServices.MoviesLocation)):
            defaultdirectory = QDesktopServices.storageLocation(QDesktopServices.MoviesLocation)
        elif os.path.isdir(QDesktopServices.storageLocation(QDesktopServices.HomeLocation)):
            defaultdirectory = QDesktopServices.storageLocation(QDesktopServices.HomeLocation)
        else:
            defaultdirectory = ""
        browserfilter = "All files (*)"
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self, "Browse for media files", defaultdirectory,
                browserfilter, "", options)
        if fileName:
            self.mediapathTextbox.setText(os.path.normpath(fileName))
            self.mediadirectory = os.path.dirname(fileName)
            self.saveMediaBrowseSettings()

    def _saveDataAndLeave(self):
        self.processWidget(self, lambda w: self.saveValues(w))
        self.config['host'] = self.hostTextbox.text() if ":" in self.hostTextbox.text() else self.hostTextbox.text() + ":" + unicode(constants.DEFAULT_PORT)
        self.config['playerPath'] = unicode(self.executablepathCombobox.currentText())
        if self.mediapathTextbox.text() == "":
            self.config['file'] = None
        elif os.path.isfile(os.path.abspath(self.mediapathTextbox.text())):
            self.config['file'] = os.path.abspath(self.mediapathTextbox.text())
        else:
            self.config['file'] = unicode(self.mediapathTextbox.text())

        if not self.slowdownThresholdSpinbox.text:
            self.slowdownThresholdSpinbox.value = constants.DEFAULT_SLOWDOWN_KICKIN_THRESHOLD
        if not self.rewindThresholdSpinbox.text:
            self.rewindThresholdSpinbox.value = constants.DEFAULT_REWIND_THRESHOLD
        self.config['slowdownThreshold'] = self.slowdownThresholdSpinbox.value()
        self.config['rewindThreshold'] = self.rewindThresholdSpinbox.value()

        self.pressedclosebutton = True
        self.close()
        return

    def closeEvent(self, event):
        if self.pressedclosebutton == False:
            sys.exit()
            raise GuiConfiguration.WindowClosed
            event.accept()

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            if sys.platform.startswith('windows'):
                dropfilepath = unicode(urls[0].path())[1:]  # Removes starting slash
            else:
                dropfilepath = unicode(urls[0].path())
            if dropfilepath[-4:].lower() == ".exe":
                self.executablepathCombobox.setEditText(dropfilepath)
            else:
                self.mediapathTextbox.setText(dropfilepath)

    def processWidget(self, container, torun):
        for widget in container.children():
            self.processWidget(widget, torun)
            if hasattr(widget, 'objectName') and widget.objectName() and widget.objectName()[:3] != "qt_":
                torun(widget)

    def loadTooltips(self, widget):
        tooltipName = widget.objectName().lower().split(":")[0] + "-tooltip"
        if tooltipName[:1] == "*" or tooltipName[:1] == "!":
            tooltipName = tooltipName[1:]
        widget.setToolTip(getMessage(tooltipName))

    def loadValues(self, widget):
        valueName = str(widget.objectName())
        if valueName[:1] == "!":
            return

        if isinstance(widget, QCheckBox) and widget.objectName():
            if valueName[:1] == "*":
                valueName = valueName[1:]
                inverted = True
            else:
                inverted = False
            widget.setChecked(self.config[valueName] != inverted)
        elif isinstance(widget, QRadioButton):
            radioName, radioValue  = valueName.split(":")[1].split("=")
            if self.config[radioName] == radioValue:
                widget.setChecked(True)
        elif isinstance(widget, QLineEdit):
            widget.setText(self.config[valueName])

    def saveValues(self, widget):
        valueName = str(widget.objectName())
        if valueName[:1] == "!":
            return

        if isinstance(widget, QCheckBox) and widget.objectName():
            if valueName[:1] == "*":
                valueName = valueName[1:]
                inverted = True
            else:
                inverted = False
            self.config[valueName] = widget.isChecked() != inverted
        elif isinstance(widget, QRadioButton):
            radioName, radioValue  = valueName.split(":")[1].split("=")
            if widget.isChecked():
                self.config[radioName] = radioValue
        elif isinstance(widget, QLineEdit):
            self.config[valueName] = widget.text()

    def __init__(self, config, playerpaths, error):

        from syncplay import utils
        self.config = config
        self.datacleared = False

        if config['clearGUIData'] == True:
            settings = QSettings("Syncplay", "PlayerList")
            settings.clear()
            settings = QSettings("Syncplay", "MediaBrowseDialog")
            settings.clear()
            settings = QSettings("Syncplay", "MainWindow")
            settings.clear()
            settings = QSettings("Syncplay", "MoreSettings")
            settings.clear()
            self.datacleared = True
        self.QtGui = QtGui
        self.error = error
        if sys.platform.startswith('windows'):
            resourcespath = utils.findWorkingDir() + "\\resources\\"
        else:
            resourcespath = utils.findWorkingDir() + "/resources/"
        self.resourcespath = resourcespath

        super(ConfigDialog, self).__init__()

        self.setWindowTitle(getMessage("config-window-title"))
        self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QtGui.QIcon(resourcespath + "syncplay.png"))

        if config['host'] == None:
            host = ""
        elif ":" in config['host']:
            host = config['host']
        else:
            host = config['host'] + ":" + str(config['port'])

        ''' objectName notation:
        "!A": Do not load/save config in main loop
        (Radiobox) "A:B=C": Use A for label/tooltip, but B and C for config name and value'''

        self.connectionSettingsGroup = QtGui.QGroupBox(getMessage("connection-group-title"))
        self.hostTextbox = QLineEdit(host, self)
        self.hostLabel = QLabel(getMessage("host-label"), self)
        self.usernameTextbox = QLineEdit(self)
        self.usernameTextbox.setObjectName("name")
        self.serverpassLabel = QLabel(getMessage("password-label"), self)
        self.defaultroomTextbox = QLineEdit(self)
        self.usernameLabel = QLabel(getMessage("name-label"), self)
        self.serverpassTextbox = QLineEdit(self)
        self.defaultroomLabel = QLabel(getMessage("room-label"), self)

        self.hostLabel.setObjectName("host")
        self.hostTextbox.setObjectName("!host")
        self.usernameLabel.setObjectName("name")
        self.usernameTextbox.setObjectName("name")
        self.serverpassLabel.setObjectName("password")
        self.serverpassTextbox.setObjectName("password")
        self.defaultroomLabel.setObjectName("room")
        self.defaultroomTextbox.setObjectName("room")

        self.connectionSettingsLayout = QtGui.QGridLayout()
        self.connectionSettingsLayout.addWidget(self.hostLabel, 0, 0)
        self.connectionSettingsLayout.addWidget(self.hostTextbox, 0, 1)
        self.connectionSettingsLayout.addWidget(self.serverpassLabel, 1, 0)
        self.connectionSettingsLayout.addWidget(self.serverpassTextbox, 1, 1)
        self.connectionSettingsLayout.addWidget(self.usernameLabel, 2, 0)
        self.connectionSettingsLayout.addWidget(self.usernameTextbox, 2, 1)
        self.connectionSettingsLayout.addWidget(self.defaultroomLabel, 3, 0)
        self.connectionSettingsLayout.addWidget(self.defaultroomTextbox, 3, 1)
        self.connectionSettingsGroup.setLayout(self.connectionSettingsLayout)

        self.mediaplayerSettingsGroup = QtGui.QGroupBox(getMessage("media-setting-title"))
        self.executableiconImage = QtGui.QImage()
        self.executableiconLabel = QLabel(self)
        self.executableiconLabel.setMinimumWidth(16)
        self.executablepathCombobox = QtGui.QComboBox(self)
        self.executablepathCombobox.setEditable(True)
        self.executablepathCombobox.currentIndexChanged.connect(self.updateExecutableIcon)
        self.executablepathCombobox.setEditText(self._tryToFillPlayerPath(config['playerPath'], playerpaths))
        self.executablepathCombobox.setMinimumWidth(200)
        self.executablepathCombobox.setMaximumWidth(200)
        self.executablepathCombobox.editTextChanged.connect(self.updateExecutableIcon)

        self.executablepathLabel = QLabel(getMessage("executable-path-label"), self)
        self.executablebrowseButton = QtGui.QPushButton(QtGui.QIcon(resourcespath + 'folder_explore.png'), getMessage("browse-label"))
        self.executablebrowseButton.clicked.connect(self.browsePlayerpath)
        self.mediapathTextbox = QLineEdit(config['file'], self)
        self.mediapathLabel = QLabel(getMessage("media-path-label"), self)
        self.mediabrowseButton = QtGui.QPushButton(QtGui.QIcon(resourcespath + 'folder_explore.png'), getMessage("browse-label"))
        self.mediabrowseButton.clicked.connect(self.browseMediapath)

        self.executablepathLabel.setObjectName("executable-path")
        self.executablepathCombobox.setObjectName("executable-path")
        self.mediapathLabel.setObjectName("media-path")
        self.mediapathTextbox.setObjectName("!media-path")

        self.mediaplayerSettingsLayout = QtGui.QGridLayout()
        self.mediaplayerSettingsLayout.addWidget(self.executablepathLabel, 0, 0)
        self.mediaplayerSettingsLayout.addWidget(self.executableiconLabel, 0, 1)
        self.mediaplayerSettingsLayout.addWidget(self.executablepathCombobox, 0, 2)
        self.mediaplayerSettingsLayout.addWidget(self.executablebrowseButton, 0, 3)
        self.mediaplayerSettingsLayout.addWidget(self.mediapathLabel, 1, 0)
        self.mediaplayerSettingsLayout.addWidget(self.mediapathTextbox , 1, 2)
        self.mediaplayerSettingsLayout.addWidget(self.mediabrowseButton , 1, 3)
        self.mediaplayerSettingsGroup.setLayout(self.mediaplayerSettingsLayout)

        self.moreSettingsGroup = QtGui.QGroupBox(getMessage("more-title"))

        self.moreSettingsGroup.setCheckable(True)

        self.slowdownThresholdLabel = QLabel(getMessage("slowdown-threshold-label"), self)
        self.slowdownThresholdSpinbox = QDoubleSpinBox()
        try:
            self.slowdownThresholdSpinbox.setValue(float(config['slowdownThreshold']))
        except ValueError:
            self.slowdownThresholdSpinbox.setValue(constants.DEFAULT_SLOWDOWN_KICKIN_THRESHOLD)
        self.slowdownThresholdSpinbox.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.slowdownThresholdSpinbox.setMinimumWidth(80)
        self.slowdownThresholdSpinbox.setMaximumWidth(80)
        self.slowdownThresholdSpinbox.setMinimum(constants.MINIMUM_SLOWDOWN_THRESHOLD)
        self.slowdownThresholdSpinbox.setSingleStep(0.1)
        self.slowdownThresholdSpinbox.setSuffix(getMessage("seconds-suffix"))
        self.slowdownThresholdSpinbox.adjustSize()

        self.rewindThresholdLabel = QLabel(getMessage("rewind-threshold-label"), self)
        self.rewindThresholdSpinbox = QDoubleSpinBox()
        try:
            self.rewindThresholdSpinbox.setValue(float(config['rewindThreshold']))
        except ValueError:
            self.rewindThresholdSpinbox.setValue(constants.DEFAULT_REWIND_THRESHOLD)
        self.rewindThresholdSpinbox.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.rewindThresholdSpinbox.setMinimumWidth(80)
        self.rewindThresholdSpinbox.setMaximumWidth(80)
        self.rewindThresholdSpinbox.setMinimum(0)
        self.rewindThresholdSpinbox.setSingleStep(0.1)
        self.rewindThresholdSpinbox.setSpecialValueText(getMessage("never-rewind-value"))
        self.rewindThresholdSpinbox.setSuffix(getMessage("seconds-suffix"))
        self.rewindThresholdSpinbox.adjustSize()

        self.slowdownThresholdLabel.setObjectName("slowdown-threshold")
        self.slowdownThresholdSpinbox.setObjectName("slowdown-threshold")
        self.rewindThresholdLabel.setObjectName("rewind-threshold")
        self.rewindThresholdSpinbox.setObjectName("rewind-threshold")

        self.slowdownLabel = QLabel(getMessage("slowdown-label"), self)
        self.slowdownButtonGroup = QButtonGroup()
        self.slowdownAutoOption = QRadioButton(getMessage("slowdown-auto-option"))
        self.slowdownAlwaysOption = QRadioButton(getMessage("slowdown-always-option"))
        self.slowdownNeverOption = QRadioButton(getMessage("slowdown-never-option"))
        self.slowdownButtonGroup.addButton(self.slowdownAutoOption)
        self.slowdownButtonGroup.addButton(self.slowdownAlwaysOption)
        self.slowdownButtonGroup.addButton(self.slowdownNeverOption)

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

        self.dontslowwithmeCheckbox = QCheckBox(getMessage("dontslowdownwithme-label"))
        self.pauseonleaveCheckbox = QCheckBox(getMessage("pauseonleave-label"))
        self.alwaysshowCheckbox = QCheckBox(getMessage("forceguiprompt-label"))
        self.nostoreCheckbox = QCheckBox(getMessage("nostore-label"))

        self.filenameprivacyLabel.setObjectName("filename-privacy")
        self.filenameprivacySendRawOption.setObjectName("privacy-sendraw:filenamePrivacyMode="+ constants.PRIVACY_SENDRAW_MODE)
        self.filenameprivacySendHashedOption.setObjectName("privacy-sendhashed:filenamePrivacyMode=" + constants.PRIVACY_SENDHASHED_MODE)
        self.filenameprivacyDontSendOption.setObjectName("privacy-dontsend:filenamePrivacyMode=" + constants.PRIVACY_DONTSEND_MODE)
        self.filesizeprivacyLabel.setObjectName("filesize-privacy")
        self.filesizeprivacySendRawOption.setObjectName("privacy-sendraw:filesizePrivacyMode=" + constants.PRIVACY_SENDRAW_MODE)
        self.filesizeprivacySendHashedOption.setObjectName("privacy-sendhashed:filesizePrivacyMode=" + constants.PRIVACY_SENDHASHED_MODE)
        self.filesizeprivacyDontSendOption.setObjectName("privacy-dontsend:filesizePrivacyMode=" + constants.PRIVACY_DONTSEND_MODE)


        self.slowdownLabel.setObjectName("slowdown")
        self.slowdownAutoOption.setObjectName("slowdown-auto:slowMeOnDesync=" + constants.OPTION_AUTO)
        self.slowdownAlwaysOption.setObjectName("slowdown-always:slowMeOnDesync=" + constants.OPTION_ALWAYS)
        self.slowdownNeverOption.setObjectName("slowdown-never:slowMeOnDesync=" + constants.OPTION_NEVER)

        self.dontslowwithmeCheckbox.setObjectName("dontSlowDownWithMe")
        self.pauseonleaveCheckbox.setObjectName("pauseOnLeave")
        self.alwaysshowCheckbox.setObjectName("*forceGuiPrompt")
        self.nostoreCheckbox.setObjectName("noStore")

        self.moreSettingsLayout = QtGui.QGridLayout()

        self.thresholdSettingsLayout = QtGui.QGridLayout()
        self.thresholdFrame = QtGui.QFrame()
        self.thresholdFrame.setLineWidth(0)
        self.thresholdFrame.setMidLineWidth(0)
        self.thresholdSettingsLayout.setContentsMargins(0, 0, 0, 0)
        self.thresholdSettingsLayout.addWidget(self.slowdownThresholdLabel, 0, 0, Qt.AlignLeft)
        self.thresholdSettingsLayout.addWidget(self.slowdownThresholdSpinbox, 0, 1, Qt.AlignLeft)
        self.thresholdSettingsLayout.addWidget(self.rewindThresholdLabel, 0, 2, Qt.AlignLeft)
        self.thresholdSettingsLayout.addWidget(self.rewindThresholdSpinbox, 0, 3, Qt.AlignLeft)
        self.thresholdFrame.setLayout(self.thresholdSettingsLayout)
        self.moreSettingsLayout.addWidget(self.thresholdFrame, 0, 0, 1, 4, Qt.AlignLeft)

        self.privacySettingsLayout = QtGui.QGridLayout()
        self.radioFrame = QtGui.QFrame()
        self.radioFrame.setLineWidth(0)
        self.radioFrame.setMidLineWidth(0)
        self.privacySettingsLayout.setContentsMargins(0, 0, 0, 0)
        self.privacySettingsLayout.addWidget(self.slowdownLabel, 0, 0)
        self.privacySettingsLayout.addWidget(self.slowdownAutoOption, 0, 1, Qt.AlignLeft)
        self.privacySettingsLayout.addWidget(self.slowdownAlwaysOption, 0, 2, Qt.AlignLeft)
        self.privacySettingsLayout.addWidget(self.slowdownNeverOption, 0, 3, Qt.AlignLeft)
        self.privacySettingsLayout.addWidget(self.filenameprivacyLabel, 1, 0)
        self.privacySettingsLayout.addWidget(self.filenameprivacySendRawOption, 1, 1, Qt.AlignLeft)
        self.privacySettingsLayout.addWidget(self.filenameprivacySendHashedOption, 1, 2, Qt.AlignLeft)
        self.privacySettingsLayout.addWidget(self.filenameprivacyDontSendOption, 1, 3, Qt.AlignLeft)
        self.privacySettingsLayout.addWidget(self.filesizeprivacyLabel, 2, 0)
        self.privacySettingsLayout.addWidget(self.filesizeprivacySendRawOption, 2, 1, Qt.AlignLeft)
        self.privacySettingsLayout.addWidget(self.filesizeprivacySendHashedOption, 2, 2, Qt.AlignLeft)
        self.privacySettingsLayout.addWidget(self.filesizeprivacyDontSendOption, 2, 3, Qt.AlignLeft)
        self.radioFrame.setLayout(self.privacySettingsLayout)

        self.moreSettingsLayout.addWidget(self.radioFrame, 1, 0, 1, 4)

        self.moreSettingsLayout.addWidget(self.dontslowwithmeCheckbox, 4, 0, 1, 2)
        self.moreSettingsLayout.addWidget(self.pauseonleaveCheckbox, 5, 0, 1, 2)
        self.moreSettingsLayout.addWidget(self.alwaysshowCheckbox, 4, 2, 1, 2)
        self.moreSettingsLayout.addWidget(self.nostoreCheckbox, 5, 2, 1, 2)


        self.moreSettingsGroup.setLayout(self.moreSettingsLayout)

        self.showmoreCheckbox = QCheckBox(getMessage("more-title"))

        if self.getMoreState() == False:
            self.showmoreCheckbox.setChecked(False)
            self.moreSettingsGroup.hide()
        else:
            self.showmoreCheckbox.hide()
        self.showmoreCheckbox.toggled.connect(self.moreToggled)
        self.moreSettingsGroup.toggled.connect(self.moreToggled)

        self.showmoreCheckbox.setObjectName("!more")


        self.nostoreCheckbox.toggled.connect(self.runButtonTextUpdate)

        self.mainLayout = QtGui.QVBoxLayout()
        if error:
            self.errorLabel = QLabel(error, self)
            self.errorLabel.setAlignment(Qt.AlignCenter)
            self.errorLabel.setStyleSheet("QLabel { color : red; }")
            self.mainLayout.addWidget(self.errorLabel)
        self.mainLayout.addWidget(self.connectionSettingsGroup)
        self.mainLayout.addSpacing(12)
        self.mainLayout.addWidget(self.mediaplayerSettingsGroup)
        self.mainLayout.addSpacing(12)
        self.mainLayout.addWidget(self.showmoreCheckbox)
        self.mainLayout.addWidget(self.moreSettingsGroup)
        self.mainLayout.addSpacing(12)

        self.topLayout = QtGui.QHBoxLayout()
        self.helpButton = QtGui.QPushButton(QtGui.QIcon(resourcespath + 'help.png'), getMessage("help-label"))
        self.helpButton.setObjectName("help")
        self.helpButton.setMaximumSize(self.helpButton.sizeHint())
        self.helpButton.pressed.connect(self.openHelp)
        self.runButton = QtGui.QPushButton(QtGui.QIcon(resourcespath + 'accept.png'), getMessage("storeandrun-label"))
        self.runButton.pressed.connect(self._saveDataAndLeave)
        if config['noStore'] == True:
            self.runButton.setText(getMessage("run-label"))
        self.topLayout.addWidget(self.helpButton, Qt.AlignLeft)
        self.topLayout.addWidget(self.runButton, Qt.AlignRight)
        self.mainLayout.addLayout(self.topLayout)

        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)
        self.runButton.setFocus()
        self.setFixedSize(self.sizeHint())
        self.setAcceptDrops(True)

        if constants.SHOW_TOOLTIPS:
            self.processWidget(self, lambda w: self.loadTooltips(w))
        self.processWidget(self, lambda w: self.loadValues(w))

        if self.datacleared == True:
            QtGui.QMessageBox.information(self, "Syncplay", getMessage("gui-data-cleared-notification"))