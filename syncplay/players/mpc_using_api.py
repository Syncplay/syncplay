#coding:utf8
from ..mpc_api import MPC_API
from twisted.internet import reactor

class MPCHCAPIPlayer(object):
    def __init__(self, manager):
        self.manager = manager
        self.mpc_api = MPC_API()
        
        self.pinged = False
        self.tmp_filename = None
        self.tmp_position = None
        
        self.mpc_api.callbacks.on_file_ready = lambda _: reactor.callLater(0.7,self.make_ping)
        self.mpc_api.callbacks.on_update_filename = self.handle_updated_filename
    def drop(self):
        pass

    def set_speed(self, value):
        pass

    def make_ping(self):
        self.manager.init_player(self)
        self.pinged = True
        self.ask_for_status()
        self.mpc_api.callbacks.on_file_ready = None

    def display_message(self, message):
        try:
            self.mpc_api.send_osd(message)
        except:
            self.mpc_error()

    def set_paused(self, value):
        try:
            if value:
                self.mpc_api.pause()
            else:
                self.mpc_api.unpause()
        except:
            self.mpc_error()

    def set_position(self, value):
        try:
            self.mpc_api.seek(value)
        except:
            self.mpc_error()

    def ask_for_status(self):
        position = self.tmp_position if self.tmp_position else 0
        paused = None
        try:
            if(self.mpc_api.is_file_ready()):
                position = self.mpc_api.ask_for_current_position()
                paused = self.mpc_api.is_paused()
                position = float(position)
                self.tmp_position = position
                self.manager.update_player_status(paused, position)
            else:
                self.manager.update_player_status(True, position)
        except MPC_API.NoSlaveDetectedException: 
            self.mpc_error()
    
    def handle_updated_filename(self,filename):
        self.filename = str(filename[0])
        self.manager.update_filename(self.filename)
        self.mpc_api.seek(self.manager.get_global_position())
        reactor.callLater(0.7, self.mpc_api.pause)
        
    def mpc_error(self):
        if self.manager.running:
            print 'Failed to connect to MPC-HC API!'
        self.manager.stop()


def run_mpc(manager, mpc_path, file_path, args):
    mpc = MPCHCAPIPlayer(manager)
    mpc.mpc_api.callbacks.on_connected = lambda _: mpc.mpc_api.open_file(file_path) if(file_path) else None
    mpc.mpc_api.start_mpc(mpc_path, args)

