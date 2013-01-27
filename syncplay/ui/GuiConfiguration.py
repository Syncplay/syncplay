import pygtk
import os
pygtk.require('2.0')
import gtk
gtk.set_interactive(False)
import webbrowser
from syncplay.messages import getMessage

class GuiConfiguration:
    def __init__(self, config):
        self.config = config
        self._availablePlayerPaths = []
        self.closedAndNotSaved = False
        
    def run(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(getMessage("en", "config-window-title"))
        self.window.connect("delete_event", lambda w, e: self._windowClosed())
        vbox = gtk.VBox(False, 0)
        self.window.add(vbox)
        vbox.show()
        self._addLabeledEntries(self.config, vbox)
        self._addCheckboxEntries(self.config, vbox)
        self._addMalPanel(vbox)
        self.hostEntry.select_region(0, len(self.hostEntry.get_text()))
        if self.config['noStore'] == True:
            self.button = gtk.Button("Run Syncplay")
        else:
            self.button = gtk.Button("Save and Run Syncplay")
        self.button.connect("clicked", lambda w: self._saveDataAndLeave())
        guideLink = gtk.Button("Configuration Guide")
        guideLink.connect("clicked", lambda w: webbrowser.open("http://syncplay.pl/guide/"))
        guideLink.show()
        vbox.add(guideLink)
        vbox.pack_start(self.button, True, True, 0)
        self.button.set_flags(gtk.CAN_DEFAULT)
        self.button.grab_default()
        self.button.show()
        self.window.show()
        gtk.main()
     
    def _windowClosed(self):
        self.window.destroy()
        gtk.main_quit()
        self.closedAndNotSaved = True
        
    def _addLabeledEntries(self, config, vbox):  
        if(config['host'] == None):
            host = ""
        elif(":" in config['host']):
            host = config['host']
        else:
            host = config['host']+":"+str(config['port'])
 
        self.hostEntry = self._addLabeledEntryToVbox(getMessage("en", "host-label"), host, vbox, lambda __, _: self._saveDataAndLeave())
        self.userEntry = self._addLabeledEntryToVbox(getMessage("en", "username-label"), config['name'], vbox, lambda __, _: self._saveDataAndLeave())
        self.roomEntry = self._addLabeledEntryToVbox(getMessage("en", "room-label"), config['room'], vbox, lambda __, _: self._saveDataAndLeave())
        self.passEntry = self._addLabeledEntryToVbox(getMessage("en", "password-label"), config['password'], vbox, lambda __, _: self._saveDataAndLeave())
        self.mpcEntry = self._addLabeledEntryToVbox(getMessage("en", "path-label"), self._tryToFillPlayerPath(), vbox, lambda __, _: self._saveDataAndLeave())
        self.fileEntry = self._addLabeledEntryToVbox(getMessage("en", "file-label"), config['file'], vbox, lambda __, w: self._saveDataAndLeave())

    def _tryToFillPlayerPath(self):
        for path in self._availablePlayerPaths:
            if(os.path.isfile(path)):
                return path
        return self.config["playerPath"]
                 
    def getProcessedConfiguration(self):
        if(self.closedAndNotSaved):
            raise self.WindowClosed
        return self.config
                    
    def _saveDataAndLeave(self):
        self.config['host'] = self.hostEntry.get_text()
        self.config['name'] = self.userEntry.get_text()
        self.config['room'] = self.roomEntry.get_text()
        self.config['password'] = self.passEntry.get_text()
        if self.alwaysShowCheck.get_active() == True:
            self.config['forceGuiPrompt'] = True
        else:
            self.config['forceGuiPrompt'] = False
        if self.storeConfigCheck.get_active() == True:
            self.config['noStore'] = True
        else:
            self.config['noStore'] = False
        if self.slowOnDesyncCheck.get_active() == True:
            self.config['slowOnDesync'] = True
        else:
            self.config['slowOnDesync'] = False
        self.window.destroy()
        gtk.main_quit()

    def _addLabeledEntryToVbox(self, label, initialEntryValue, vbox, callback):
        hbox = gtk.HBox(False, 0)
        hbox.set_border_width(3)
        vbox.pack_start(hbox, False, False, 0)
        hbox.show()
        label_ = gtk.Label()
        label_.set_text(label)
        label_.set_alignment(xalign=0, yalign=0.5) 
        hbox.pack_start(label_, False, False, 0)
        label_.show()
        entry = gtk.Entry()
        entry.connect("activate", callback, entry)
        if(initialEntryValue == None):
            initialEntryValue = ""
        entry.set_text(initialEntryValue)
        if(label == getMessage("en", "path-label")):
            self.playerPathButton = gtk.Button("Browse")
            self.playerPathButton.connect("clicked", lambda w: self._showPlayerFileDialog())
            self.playerPathButton.show()
            hbox.add(entry)
            hbox.pack_end(self.playerPathButton, False, False, 0)
        elif(label == getMessage("en", "file-label")):
            self.mediaPathButton = gtk.Button("Browse")
            self.mediaPathButton.connect("clicked", lambda w: self._showMediaFileDialog())
            self.mediaPathButton.show()
            hbox.add(entry)
            hbox.pack_end(self.mediaPathButton, False, False, 0)
        else:
            hbox.pack_end(entry, False, False, 0)
        entry.set_usize(200, -1)
        entry.show()
        return entry
    
    def _addCheckboxEntries(self, config, vbox):
        CheckVbox = gtk.VBox(False, 0)
        vbox.pack_start(CheckVbox, False, False, 0)
        self.alwaysShowCheck = gtk.CheckButton("Always Show This Dialog When Opening A File With Syncplay")
        if self.config['forceGuiPrompt'] == True:
            self.alwaysShowCheck.set_active(True)
        self.alwaysShowCheck.show()
        self.storeConfigCheck = gtk.CheckButton("Do Not Store This Configuration")
        self.storeConfigCheck.connect("toggled", lambda w: self._changeSaveLabel())
        if self.config['noStore'] == True:
            self.storeConfigCheck.set_active(True)
        self.storeConfigCheck.show()
        self.slowOnDesyncCheck = gtk.CheckButton("Slow Down On Desync")
        if self.config['slowOnDesync'] == True:
            self.slowOnDesyncCheck.set_active(True)
        self.slowOnDesyncCheck.show()
        CheckVbox.pack_start(self.alwaysShowCheck, False, False, 0)
        CheckVbox.add(self.storeConfigCheck)
        CheckVbox.add(self.slowOnDesyncCheck)
        CheckVbox.show()

    def _changeSaveLabel(self):
        if self.config['noStore'] == True:
            self.button.set_label("Save and Run Syncplay")
            self.config['noStore'] = False
        else:
            self.button.set_label("Run Syncplay")
            self.config['noStore'] = True

    def _showPlayerFileDialog(self):
        dialog = gtk.FileChooserDialog(parent=self.window,action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialog.run()
        if dialog.get_filename() != None:
            self.config['playerPath'] = dialog.get_filename()
        dialog.destroy()
        self.mpcEntry.set_text(self.config['playerPath'])

    def _showMediaFileDialog(self):
        dialog = gtk.FileChooserDialog(parent=self.window,action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialog.run()
        if dialog.get_filename() != None:
            self.config['file'] = dialog.get_filename()
        dialog.destroy()
        self.fileEntry.set_text(self.config['file'])

    def _addMalPanel(self, vbox):
        panel = gtk.Expander("MAL Updater Settings")
        panel.show()
        panelVbox = gtk.VBox(False, 0)

        malCredHbox = gtk.HBox(False,0)
        malCredHbox.show()
        self.malUpdaterOnCheck = gtk.CheckButton("MAL Updater On")
        self.malUpdaterOnCheck.show()
        malCredHbox.add(self.malUpdaterOnCheck)
        self.clearCredentialsButton = gtk.Button("Clear Saved Credentials")
        self.clearCredentialsButton.connect("clicked", lambda w: self._clearMalCredentials())
        self.clearCredentialsButton.show()
        malCredHbox.add(self.clearCredentialsButton)
        panelVbox.add(malCredHbox)

        self.malUsername = self._addLabeledEntryToVbox("Username: ", " ", panelVbox, lambda __, w: self._saveDataAndLeave())
        self.malPassword = self._addLabeledEntryToVbox("Password: ", " ", panelVbox, lambda __, w: self._saveDataAndLeave())

        spinButtonHbox = gtk.HBox(True, 0)
        percentBoxLabel = gtk.Label("Progress Threshold For Updating: ")
        percentBoxLabel.show()
        spinButtonHbox.add(percentBoxLabel)
        self.percentBox = gtk.SpinButton(adjustment=gtk.Adjustment(0,1,100,1,1,0))
        self.percentBox.show()
        spinButtonHbox.add(self.percentBox)
        spinButtonHbox.show()
        panelVbox.add(spinButtonHbox)

        panelVbox.show()
        panel.add(panelVbox)
        vbox.add(panel)

    def _clearMalCredentials(self):
        return

    def setAvailablePaths(self, paths):
        self._availablePlayerPaths = paths
    
    class WindowClosed(Exception):
        pass
