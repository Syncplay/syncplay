#coding:utf8
from ..mpc_api import MPC_API

class MPCHCAPIPlayer(object):
    def __init__(self, manager, host = None):
        self.manager = manager
        self.mpc_api = MPC_API()
        
        self.pinged = False
        self.tmp_filename = None
        self.tmp_position = None

    def drop(self):
        pass

    def set_speed(self, value):
        pass

    def make_ping(self):
        self.ask_for_status()

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
        position = None
        filename = None
        paused = None
        if(not self.pinged):
            self.manager.init_player(self)
            self.pinged = True
        else:
            try:
                if(self.mpc_api.is_file_ready()):
                    position = self.mpc_api.ask_for_current_position()
                    filename = self.mpc_api.fileplaying
                    paused = self.mpc_api.is_paused()
            
                    position = float(position)
                    self.tmp_position = position
                    if filename != self.tmp_filename:
                        self.tmp_filename = filename
                        self.manager.update_filename(str(filename))
                    self.manager.update_player_status(paused, position)
            except MPC_API.NoSlaveDetectedException: 
                self.mpc_error()

    def mpc_error(self):
        if self.manager.running:
            print 'Failed to connect to MPC-HC API!'
        self.manager.stop()


def run_mpc(manager, mpc_path, file_path, args):
    mpc = MPCHCAPIPlayer(manager)
    mpc.mpc_api.callbacks.on_file_ready = mpc.make_ping
    mpc.mpc_api.callbacks.on_connected = lambda: mpc.mpc_api.open_file(file_path) if(file_path) else None
    mpc.mpc_api.start_mpc(mpc_path, args)

