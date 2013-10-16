from PySide import QtCore, QtGui
from PySide.QtCore import QSettings, Qt, QCoreApplication
from PySide.QtGui import QApplication, QLineEdit, QCursor, QLabel, QCheckBox, QDesktopServices, QIcon, QImage
from syncplay.players.playerFactory import PlayerFactory

import os
import sys
from syncplay.messages import getMessage
from syncplay import constants

class GuiConfiguration:
    def __init__(self, config, error = None):
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
    malToggling = False
    
    def malToggled(self):
        if self.malToggling == False:
            self.malToggling = True
            
            if self.malenabledCheckbox.isChecked() and self.malenabledCheckbox.isVisible():
                self.malenabledCheckbox.setChecked(False)
                self.malSettingsGroup.setChecked(True)
                self.malSettingsGroup.show()
                self.malpasswordLabel.show()
                self.malpasswordTextbox.show()
                self.malusernameLabel.show()
                self.malusernameTextbox.show()
                self.malenabledCheckbox.hide()
            else:
                self.malSettingsGroup.setChecked(False)
                self.malSettingsGroup.hide()
                self.malpasswordLabel.hide()
                self.malpasswordTextbox.hide()
                self.malusernameLabel.hide()
                self.malusernameTextbox.hide()
                self.malenabledCheckbox.show()
                
            self.malToggling = False
            self.adjustSize()
            self.setFixedSize(self.sizeHint())
            
    def runButtonTextUpdate(self):
        if (self.donotstoreCheckbox.isChecked()):
            self.runButton.setText(getMessage("en", "run-label"))
        else:
            self.runButton.setText(getMessage("en", "storeandrun-label"))
            
    def openHelp(self):
        if sys.platform.startswith('linux'):
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/linux/")
        elif sys.platform.startswith('win'):
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/windows/")
        else:
            self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/")

    def _tryToFillPlayerPath(self, playerpath, playerpathlist):
        settings = QSettings("Syncplay", "PlayerList")
        settings.beginGroup("PlayerList")
        savedPlayers = settings.value("PlayerList", [])
        playerpathlist = list(set([os.path.normcase(os.path.normpath(path)) for path in set(playerpathlist + savedPlayers)]))
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
            if(os.path.isfile(path) and os.path.normcase(os.path.normpath(path)) != os.path.normcase(os.path.normpath(foundpath))):
                self.executablepathCombobox.addItem(path)
                if foundpath == "":
                    foundpath = path

        if foundpath != "":
            settings.beginGroup("PlayerList")
            playerpathlist.append(os.path.normcase(os.path.normpath(foundpath)))
            settings.setValue("PlayerList",  list(set([os.path.normcase(os.path.normpath(path)) for path in set(playerpathlist)])))
            settings.endGroup()
        return(foundpath)
    
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
            browserfilter =  "Executable files (*.exe);;All files (*)"
            if "PROGRAMFILES(X86)" in os.environ: 
                defaultdirectory = os.environ["ProgramFiles(x86)"]
            elif "PROGRAMFILES" in os.environ:
                defaultdirectory = os.environ["ProgramFiles"]
            elif "PROGRAMW6432" in os.environ:
                defaultdirectory = os.environ["ProgramW6432"]
        elif sys.platform.startswith('linux'):
            defaultdirectory = "/usr/bin"
        
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
        
    def browseMediapath(self):
        self.loadMediaBrowseSettings()
        options = QtGui.QFileDialog.Options()
        if (os.path.isdir(self.mediadirectory)):
            defaultdirectory = self.mediadirectory
        elif (os.path.isdir(QDesktopServices.storageLocation(QDesktopServices.MoviesLocation))):
            defaultdirectory = QDesktopServices.storageLocation(QDesktopServices.MoviesLocation)
        elif (os.path.isdir(QDesktopServices.storageLocation(QDesktopServices.HomeLocation))):
            defaultdirectory = QDesktopServices.storageLocation(QDesktopServices.HomeLocation)
        else:
            defaultdirectory = ""
        browserfilter = "All files (*)"       
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self,"Browse for media files",defaultdirectory,
                browserfilter, "", options)
        if fileName:
            self.mediapathTextbox.setText(os.path.normpath(fileName))
            self.mediadirectory = os.path.dirname(fileName)
            self.saveMediaBrowseSettings()
        
    def _saveDataAndLeave(self):
        self.config['host'] = self.hostTextbox.text()
        self.config['name'] = self.usernameTextbox.text()
        self.config['room'] = self.defaultroomTextbox.text()
        self.config['password'] = self.serverpassTextbox.text()
        self.config['playerPath'] = unicode(self.executablepathCombobox.currentText())
        if self.mediapathTextbox.text() == "":
            self.config['file'] = None
        elif os.path.isfile(os.path.abspath(self.mediapathTextbox.text())):
            self.config['file'] = os.path.abspath(self.mediapathTextbox.text())
        else:
            self.config['file'] = unicode(self.mediapathTextbox.text()) 
        if self.alwaysshowCheckbox.isChecked() == True:
            self.config['forceGuiPrompt'] = True
        else:
            self.config['forceGuiPrompt'] = False
        if self.donotstoreCheckbox.isChecked() == True:
            self.config['noStore'] = True
        else:
            self.config['noStore'] = False
        if self.slowdownCheckbox.isChecked() == True:
            self.config['slowOnDesync'] = True
        else:
            self.config['slowOnDesync'] = False
        if constants.SHOW_REWIND_ON_DESYNC_CHECKBOX == True:
            if self.rewindCheckbox.isChecked() == True:
                self.config['rewindOnDesync'] = True
            else:
                self.config['rewindOnDesync'] = False
        self.config['malUsername'] = self.malusernameTextbox.text()
        if self.malSettingsGroup.isChecked():
            self.config['malPassword'] = self.malpasswordTextbox.text()
        else:
            self.config['malPassword'] = ""
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
        if (urls and urls[0].scheme() == 'file'):
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            if sys.platform.startswith('linux'):
                dropfilepath = unicode(urls[0].path())
            else:
                dropfilepath = unicode(urls[0].path())[1:] # Removes starting slash 
            if dropfilepath[-4:].lower() == ".exe":
                self.executablepathCombobox.setEditText(dropfilepath)
            else:
                self.mediapathTextbox.setText(dropfilepath)

    def __init__(self, config, playerpaths, error):
        
        from syncplay import utils
        self.config = config
        self.datacleared = False
        if config['clearGUIData'] == True:
            settings = QSettings("Syncplay","PlayerList")
            settings.clear()
            settings = QSettings("Syncplay","MediaBrowseDialog")
            settings.clear()
            settings = QSettings("Syncplay","MainWindow")
            settings.clear()
            self.datacleared = True
        self.QtGui = QtGui
        self.error = error
        if sys.platform.startswith('linux'):
            resourcespath = utils.findWorkingDir() + "/resources/"
        else:
            resourcespath = utils.findWorkingDir() + "\\resources\\"
        self.resourcespath = resourcespath

        super(ConfigDialog, self).__init__()
        
        self.setWindowTitle(getMessage("en", "config-window-title"))
        self.setWindowFlags(self.windowFlags() & Qt.WindowCloseButtonHint & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QtGui.QIcon(resourcespath + "syncplay.png"))
              
        if(config['host'] == None):
            host = ""
        elif(":" in config['host']):
            host = config['host']
        else:
            host = config['host']+":"+str(config['port'])
            
        self.connectionSettingsGroup = QtGui.QGroupBox(getMessage("en", "connection-group-title"))
        self.hostTextbox = QLineEdit(host, self)
        self.hostLabel = QLabel(getMessage("en", "host-label"), self)
        self.usernameTextbox = QLineEdit(config['name'],self)
        self.serverpassLabel = QLabel(getMessage("en", "password-label"), self)
        self.defaultroomTextbox = QLineEdit(config['room'],self)
        self.usernameLabel = QLabel(getMessage("en", "username-label"), self)
        self.serverpassTextbox = QLineEdit(config['password'],self)
        self.defaultroomLabel = QLabel(getMessage("en", "room-label"), self)
        
        if (constants.SHOW_TOOLTIPS == True):
            self.hostLabel.setToolTip(getMessage("en", "host-tooltip"))
            self.hostTextbox.setToolTip(getMessage("en", "host-tooltip"))
            self.usernameLabel.setToolTip(getMessage("en", "username-tooltip"))
            self.usernameTextbox.setToolTip(getMessage("en", "username-tooltip"))
            self.serverpassLabel.setToolTip(getMessage("en", "password-tooltip"))
            self.serverpassTextbox.setToolTip(getMessage("en", "password-tooltip"))
            self.defaultroomLabel.setToolTip(getMessage("en", "room-tooltip"))
            self.defaultroomTextbox.setToolTip(getMessage("en", "room-tooltip"))
            
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
        
        self.mediaplayerSettingsGroup = QtGui.QGroupBox(getMessage("en", "media-setting-title"))
        self.executableiconImage = QtGui.QImage()
        self.executableiconLabel = QLabel(self)
        self.executableiconLabel.setMinimumWidth(16)
        self.executablepathCombobox = QtGui.QComboBox(self)
        self.executablepathCombobox.setEditable(True)
        self.executablepathCombobox.currentIndexChanged.connect(self.updateExecutableIcon)
        self.executablepathCombobox.setEditText(self._tryToFillPlayerPath(config['playerPath'],playerpaths))
        self.executablepathCombobox.setMinimumWidth(200)
        self.executablepathCombobox.setMaximumWidth(200)
        self.executablepathCombobox.editTextChanged.connect(self.updateExecutableIcon)
        
        self.executablepathLabel = QLabel(getMessage("en", "executable-path-label"), self)
        self.executablebrowseButton = QtGui.QPushButton(QtGui.QIcon(resourcespath + 'folder_explore.png'),getMessage("en", "browse-label"))
        self.executablebrowseButton.clicked.connect(self.browsePlayerpath)
        self.mediapathTextbox = QLineEdit(config['file'], self)
        self.mediapathLabel = QLabel(getMessage("en", "media-path-label"), self)
        self.mediabrowseButton = QtGui.QPushButton(QtGui.QIcon(resourcespath + 'folder_explore.png'),getMessage("en", "browse-label"))
        self.mediabrowseButton.clicked.connect(self.browseMediapath)
        self.slowdownCheckbox = QCheckBox(getMessage("en", "slowdown-label"))
        if (constants.SHOW_TOOLTIPS == True):
            self.executablepathLabel.setToolTip(getMessage("en", "executable-path-tooltip"))
            self.executablepathCombobox.setToolTip(getMessage("en", "executable-path-tooltip"))
            self.mediapathLabel.setToolTip(getMessage("en", "media-path-tooltip"))
            self.mediapathTextbox.setToolTip(getMessage("en", "media-path-tooltip"))
            self.slowdownCheckbox.setToolTip(getMessage("en", "slowdown-tooltip"))
        
        if constants.SHOW_REWIND_ON_DESYNC_CHECKBOX == True:
            self.rewindCheckbox = QCheckBox(getMessage("en", "rewind-label"))
            if (constants.SHOW_TOOLTIPS == True):
                self.rewindCheckbox.setToolTip(getMessage("en", "rewind-tooltip"))
        self.mediaplayerSettingsLayout = QtGui.QGridLayout()
        self.mediaplayerSettingsLayout.addWidget(self.executablepathLabel, 0, 0)
        self.mediaplayerSettingsLayout.addWidget(self.executableiconLabel, 0, 1)
        self.mediaplayerSettingsLayout.addWidget(self.executablepathCombobox, 0, 2)
        self.mediaplayerSettingsLayout.addWidget(self.executablebrowseButton, 0, 3)
        self.mediaplayerSettingsLayout.addWidget(self.mediapathLabel, 1, 0)
        self.mediaplayerSettingsLayout.addWidget(self.mediapathTextbox , 1, 2)
        self.mediaplayerSettingsLayout.addWidget(self.mediabrowseButton , 1, 3)
        self.mediaplayerSettingsLayout.addWidget(self.slowdownCheckbox, 2, 0,1,3)
        if constants.SHOW_REWIND_ON_DESYNC_CHECKBOX == True:
            self.mediaplayerSettingsLayout.addWidget(self.rewindCheckbox, 3, 0,1,3)
        self.mediaplayerSettingsGroup.setLayout(self.mediaplayerSettingsLayout)
        if config['slowOnDesync'] == True:
            self.slowdownCheckbox.setChecked(True)
        if constants.SHOW_REWIND_ON_DESYNC_CHECKBOX == True and config['rewindOnDesync'] == True:
            self.rewindCheckbox.setChecked(True)

        self.malSettingsGroup = QtGui.QGroupBox(getMessage("en", "mal-title"))
        self.malSettingsGroup.setCheckable(True)
        self.malSettingsGroup.toggled.connect(self.malToggled)
        self.malSettingsSplit = QtGui.QSplitter(self)
        self.malusernameTextbox = QLineEdit(config['malUsername'],self)
        self.malusernameLabel = QLabel(getMessage("en", "mal-username-label"), self)
        
        self.malpasswordTextbox = QLineEdit(config['malPassword'],self)
        self.malpasswordTextbox.setEchoMode(QtGui.QLineEdit.Password)
        self.malpasswordLabel = QLabel(getMessage("en", "mal-password-label"), self)
        if (constants.SHOW_TOOLTIPS == True):
            self.malusernameLabel.setToolTip(getMessage("en", "mal-username-tooltip"))
            self.malusernameTextbox.setToolTip(getMessage("en", "mal-username-tooltip"))
            self.malpasswordLabel.setToolTip(getMessage("en", "mal-password-tooltip"))
            self.malpasswordTextbox.setToolTip(getMessage("en", "mal-password-tooltip"))
        self.malSettingsLayout = QtGui.QGridLayout()
        self.malSettingsLayout.addWidget(self.malusernameLabel , 0, 0)
        self.malSettingsLayout.addWidget(self.malusernameTextbox, 0, 1)
        self.malSettingsLayout.addWidget(self.malpasswordLabel , 1, 0)
        self.malSettingsLayout.addWidget(self.malpasswordTextbox, 1, 1)
        self.malSettingsGroup.setLayout(self.malSettingsLayout)
        
        self.malenabledCheckbox = QCheckBox(getMessage("en", "mal-title"))
        self.malenabledCheckbox.toggled.connect(self.malToggled) 
        if config['malPassword'] == None or config['malPassword'] == "":
            self.malenabledCheckbox.setChecked(False)
            self.malSettingsGroup.hide()
        else:
            self.malenabledCheckbox.hide()
        
        self.alwaysshowCheckbox = QCheckBox(getMessage("en", "alwayshow-label"))
        
        if config['forceGuiPrompt'] == True:
            self.alwaysshowCheckbox.setChecked(True)
        
        self.donotstoreCheckbox = QCheckBox(getMessage("en", "donotstore-label"))
        if (constants.SHOW_TOOLTIPS == True):
            self.malenabledCheckbox.setToolTip(getMessage("en", "mal-tooltip"))
            self.alwaysshowCheckbox.setToolTip(getMessage("en", "alwayshow-tooltip"))
            self.donotstoreCheckbox.setToolTip(getMessage("en", "donotstore-tooltip"))
               
        self.donotstoreCheckbox.toggled.connect(self.runButtonTextUpdate)
                      
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
        self.mainLayout.addWidget(self.malenabledCheckbox)
        self.mainLayout.addWidget(self.malSettingsGroup)
        
        self.topLayout = QtGui.QHBoxLayout()
        self.helpButton = QtGui.QPushButton(QtGui.QIcon(resourcespath + 'help.png'),getMessage("en", "help-label"))
        if (constants.SHOW_TOOLTIPS == True):
            self.helpButton.setToolTip(getMessage("en", "help-tooltip"))
        self.helpButton.setMaximumSize(self.helpButton.sizeHint())
        self.helpButton.pressed.connect(self.openHelp)
        self.runButton = QtGui.QPushButton(QtGui.QIcon(resourcespath + 'accept.png'),getMessage("en", "storeandrun-label"))
        self.runButton.pressed.connect(self._saveDataAndLeave)
        if config['noStore'] == True:
            self.donotstoreCheckbox.setChecked(True)
            self.runButton.setText(getMessage("en", "run-label"))
        self.topLayout.addWidget(self.helpButton, Qt.AlignLeft)
        self.topLayout.addWidget(self.runButton, Qt.AlignRight)
        self.mainLayout.addWidget(self.alwaysshowCheckbox)
        self.mainLayout.addWidget(self.donotstoreCheckbox)
        self.mainLayout.addLayout(self.topLayout)
        
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)
        self.runButton.setFocus()        
        self.setFixedSize(self.sizeHint())
        self.setAcceptDrops(True)
        
        if self.datacleared == True:
            QtGui.QMessageBox.information(self,"Syncplay", getMessage("en", "gui-data-cleared-notification"))
