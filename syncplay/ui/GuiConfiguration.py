import pygtk
import os
pygtk.require('2.0')
import gtk
gtk.set_interactive(False)
import cairo, gio, pango, atk, pangocairo, gobject #@UnusedImport
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
        self.hostEntry.select_region(0, len(self.hostEntry.get_text()))
        button = gtk.Button(stock=gtk.STOCK_SAVE)
        button.connect("clicked", lambda w: self._saveDataAndLeave())
        vbox.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
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
        self.config['playerPath'] = self.mpcEntry.get_text()
        if self.alwaysShowCheck.get_active() == True:
            self.config['alwaysShow'] = True
        else:
            self.config['alwaysShow'] = False
        if self.storeConfigCheck.get_active() == True:
            self.config['storeConfig'] = True
        else:
			self.config['storeConfig'] = False
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
        hbox.pack_end(entry, False, False, 0)
        entry.set_usize(200, -1)
        entry.show()
        return entry
    
    def _addCheckboxEntries(self, config, vbox):
        CheckVbox = gtk.VBox(False, 0)
        vbox.pack_start(CheckVbox, False, False, 0)
        self.alwaysShowCheck = gtk.CheckButton("Always Show This Dialog")
        self.alwaysShowCheck.show()
        self.storeConfigCheck = gtk.CheckButton("Do Not Store This Configuration")
        self.storeConfigCheck.show()
        self.slowOnDesyncCheck = gtk.CheckButton("Slow Down On Desync")
        self.slowOnDesyncCheck.show()
        CheckVbox.pack_start(self.alwaysShowCheck, False, False, 0)
        CheckVbox.add(self.storeConfigCheck)
        CheckVbox.add(self.slowOnDesyncCheck)
        CheckVbox.show()

    def setAvailablePaths(self, paths):
        self._availablePlayerPaths = paths
    
    class WindowClosed(Exception):
        pass
