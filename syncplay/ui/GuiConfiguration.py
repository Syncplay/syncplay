import pygtk
import os
pygtk.require('2.0')
import gtk
gtk.set_interactive(False)
import cairo, gio, pango, atk, pangocairo, gobject #@UnusedImport

class GuiConfiguration:
    def __init__(self, args, force=False):
        self.args = args
        self.closedAndNotSaved = False
        if(args.player_path == None or args.host == None or args.name == None or force):
            self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.window.set_title("Syncplay Configuration")  
            self.window.connect("delete_event", lambda w, e: self._windowClosed())
            vbox = gtk.VBox(False, 0)
            self.window.add(vbox)
            vbox.show()
            self._addLabeledEntries(args, vbox)
    
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
        
    def _addLabeledEntries(self, args, vbox):  
        if(args.host == None):
            host = ""
        elif(":" in args.host):
            host = args.host
        elif("port" in args):
            host = args.host+":"+str(args.port)
        else:
            host = args.host 
        self.hostEntry = self._addLabeledEntryToVbox('Host: ', host, vbox, self._focusNext)
        self.userEntry = self._addLabeledEntryToVbox('Username: ', args.name, vbox, self._focusNext)
        self.roomEntry = self._addLabeledEntryToVbox('Default room (optional): ', args.room, vbox, self._focusNext)
        self.passEntry = self._addLabeledEntryToVbox('Server password (optional): ', args.password, vbox, self._focusNext)
        self._tryToFillUpMpcPath()
        self.mpcEntry = self._addLabeledEntryToVbox('Path to player executable: ', self.args.player_path, vbox, self._focusNext)
 
    def _tryToFillUpMpcPath(self):
        if(self.args.player_path == None):
            paths = ["C:\Program Files (x86)\MPC-HC\mpc-hc.exe",
                     "C:\Program Files\MPC-HC\mpc-hc.exe",
                     "C:\Program Files\MPC-HC\mpc-hc64.exe",
                     "C:\Program Files\Media Player Classic - Home Cinema\mpc-hc.exe",
                     "C:\Program Files\Media Player Classic - Home Cinema\mpc-hc64.exe",
                     "C:\Program Files (x86)\Media Player Classic - Home Cinema\mpc-hc.exe",
                     "C:\Program Files (x86)\K-Lite Codec Pack\Media Player Classic\mpc-hc.exe",
                     "C:\Program Files\K-Lite Codec Pack\Media Player Classic\mpc-hc.exe",
                     "C:\Program Files (x86)\Combined Community Codec Pack\MPC\mpc-hc.exe",
                     "C:\Program Files\MPC HomeCinema (x64)\mpc-hc64.exe",
                     ]
            for path in paths:
                if(os.path.isfile(path)):
                    self.args.player_path = path
                    return
                 
           
    def getProcessedConfiguration(self):
        if(self.closedAndNotSaved):
            raise self.WindowClosed
        return self.args
                    
    def _saveDataAndLeave(self):
        self.args.host = self.hostEntry.get_text()
        self.args.name = self.userEntry.get_text()
        self.args.room = self.roomEntry.get_text()
        self.args.password = self.passEntry.get_text()
        self.args.player_path = self.mpcEntry.get_text()
        self.window.destroy()
        gtk.main_quit()
        
    def _focusNext(self, widget, entry):
        self.window.get_toplevel().child_focus(gtk.DIR_TAB_FORWARD) 

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
        hbox = gtk.HBox(False, 0)
        vbox.add(hbox)
        hbox.show()
        return entry

    class WindowClosed(Exception):
        def __init__(self):
            Exception.__init__(self)


                
                
