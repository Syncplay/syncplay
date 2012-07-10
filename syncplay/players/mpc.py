#coding:utf8

from ..mpc_api import MPC_API
import time

class MPCHCAPIPlayer(object):
    def __init__(self, manager):
        self.manager = manager
        self.mpc_api = MPC_API()
        
        self.pinged = False
        self.tmp_filename = None
        self.tmp_position = None
        
        self.mpc_api.callbacks.on_file_ready = lambda: self.make_ping()
        self.mpc_api.callbacks.on_mpc_closed = lambda: self.mpc_error("MPC closed")
    
        self.semaphore_filename = False
 
    def drop(self):
        pass

    def set_speed(self, value):
        pass

    def test_mpc_ready(self):
        try:
            self.mpc_api.ask_for_current_position()
        except MPC_API.PlayerNotReadyException:
            time.sleep(0.1)
            self.test_mpc_ready()
            return

    def make_ping(self):
        self.mpc_api.callbacks.on_file_ready = None
        self.test_mpc_ready()
        self.manager.init_player(self)
        self.pinged = True
        self.ask_for_status()

    def display_message(self, message):
        try:
            self.mpc_api.send_osd(message)
        except Exception, err:
            self.mpc_error(err)

    def set_paused(self, value):
        try:
            if value:
                self.mpc_api.pause()
            else:
                self.mpc_api.unpause()
        except MPC_API.PlayerNotReadyException:
            time.sleep(0.2)
            self.set_paused(value)
            return
        except Exception, err:
            self.mpc_error(err)

    def set_position(self, value):
        try:
            self.mpc_api.seek(value)
        except MPC_API.PlayerNotReadyException:
            self.set_position(value)
            return
        except Exception, err:
            self.mpc_error(err)

    def ask_for_status(self):
        position = self.tmp_position if self.tmp_position else 0
        paused = None
        try:
            if(self.mpc_api.is_file_ready() and not self.semaphore_filename):
                try:
                    position = self.mpc_api.ask_for_current_position()
                except MPC_API.PlayerNotReadyException:
                    time.sleep(0.1)
                    self.ask_for_status()
                    return
                if(self.tmp_filename <> self.mpc_api.fileplaying):
                    self.handle_updated_filename(self.mpc_api.fileplaying)
                    return
                paused = self.mpc_api.is_paused()
                position = float(position)
                self.tmp_position = position
                self.manager.update_player_status(paused, position)
            else:
                self.manager.update_player_status(True, self.manager.get_global_position())
        except Exception, err:
            self.mpc_error(err)

    def __force_pause(self, filename, position):
        self.set_paused(True)
        time.sleep(0.1)
        if (not self.mpc_api.is_paused()):
            self.__set_up_newly_opened_file(filename, position)

    def __set_up_newly_opened_file(self, filename, position):
        self.test_mpc_ready()
        try:
            self.mpc_api.seek(position)
        except MPC_API.PlayerNotReadyException:
            time.sleep(0.1)
            self.__set_up_newly_opened_file(filename, position)
        self.__force_pause(filename, position)
        
    def handle_updated_filename(self, filename):
        position = self.manager.get_global_position()
        if(self.semaphore_filename): 
            self.manager.update_player_status(True, position)
            return 
        self.semaphore_filename = True
        self.__set_up_newly_opened_file(filename, position)
        self.tmp_filename = filename
        self.manager.update_filename(str(self.tmp_filename))
        self.manager.update_player_status(True, position)
        self.semaphore_filename = False
        
    def mpc_error(self, err=""):
        print "ERROR:", str(err) + ',', "desu"
        if self.manager.running:
            print 'Failed to connect to MPC-HC API!'
        self.manager.stop()

def run_mpc(manager, mpc_path, file_path, args):
    mpc = MPCHCAPIPlayer(manager)
    mpc.mpc_api.callbacks.on_connected = lambda: mpc.mpc_api.open_file(file_path) if(file_path) else None
    mpc.mpc_api.start_mpc(mpc_path, args)
