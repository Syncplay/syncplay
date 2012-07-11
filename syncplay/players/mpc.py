#coding:utf8

from ..mpc_api import MPC_API
import time
import threading

class MPCHCAPIPlayer(object):
    def __init__(self, manager):
        self._syncplayClient = manager
        self.mpc_api = MPC_API()
        
        self.pinged = False

        self.mpc_api.callbacks.on_update_filename = lambda _: self.make_ping()
        self.mpc_api.callbacks.on_mpc_closed = lambda: self.mpc_error("MPC closed")
    
        self.mpc_api.callbacks.on_fileStateChange = self.lockAsking
        self.mpc_api.callbacks.on_update_playstate = self.unlockAsking
    
        self.askSemaphore = False
        self.askLock = threading.RLock()
        
    def drop(self):
        pass

    def lockAsking(self, state):
        self.askSemaphore = True
        
    def unlockAsking(self, state):
        self.askSemaphore = False
    
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
        self.test_mpc_ready()
        self.mpc_api.callbacks.on_update_filename = self.handle_updated_filename
        self._syncplayClient.initPlayer(self)
        self.handle_updated_filename(self.mpc_api.fileplaying)
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

    def __askForPositionUntilPlayerReady(self):
        try:
            return self.mpc_api.ask_for_current_position()
        except MPC_API.PlayerNotReadyException:
            time.sleep(0.1)
            return self.__askForPositionUntilPlayerReady()

    def ask_for_status(self):
        try:
            self.askLock.acquire()
            if(self.mpc_api.is_file_ready() and not self.askSemaphore):
                position = self.__askForPositionUntilPlayerReady()
                paused = self.mpc_api.is_paused()
                position = float(position)
                if(not self.askSemaphore):
                    self._syncplayClient.updatePlayerStatus(paused, position)
                    return
            self._syncplayClient.updatePlayerStatus(True, self._syncplayClient.getGlobalPosition())
        except Exception, err:
            self.mpc_error(err)
        finally:
            self.askLock.release()
   
    def __pauseChangeCheckLoop(self, i, changeFrom):
        time.sleep(0.1)
        if(i < 10):
            if(self.mpc_api.is_paused() <> changeFrom):
                return
            else:
                self.__pauseChangeCheckLoop(i+1, True)
                
    def __force_pause(self):
        self.__pauseChangeCheckLoop(0, True)
        self.set_paused(True)

    def __set_up_newly_opened_file(self, filename, position):
        try:
            self.__force_pause()
            self.mpc_api.seek(position)
        except MPC_API.PlayerNotReadyException:
            time.sleep(0.1)
            self.__set_up_newly_opened_file(filename, position)

        
    def handle_updated_filename(self, filename):
        try:
            self.askLock.acquire()
            position = self._syncplayClient.getGlobalPosition()
            self.__set_up_newly_opened_file(filename, position)
            self._syncplayClient.updateFilename(str(filename))
        finally:
            self.askLock.release()
        
    def mpc_error(self, err=""):
        print "ERROR:", str(err) + ',', "desu"
        if self._syncplayClient.running:
            print 'Failed to connect to MPC-HC API!'
        self._syncplayClient.stop()

def run_mpc(manager, mpc_path, file_path, args):
    mpc = MPCHCAPIPlayer(manager)
    mpc.mpc_api.callbacks.on_connected = lambda: mpc.mpc_api.open_file(file_path) if(file_path) else None
    mpc.mpc_api.start_mpc(mpc_path, args)
