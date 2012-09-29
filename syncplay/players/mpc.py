#coding:utf8

from ..mpc_api import MPC_API
import time
import threading

class MPCHCAPIPlayer(object):
    def __init__(self, manager):
        self.__syncplayClient = manager
        self.mpc_api = MPC_API()
        self.mpc_api.callbacks.on_update_filename = lambda _: self.make_ping()
        self.mpc_api.callbacks.on_mpc_closed = lambda: self.__syncplayClient.stop(False)
        self.mpc_api.callbacks.on_fileStateChange = lambda _: self.lockAsking()
        self.mpc_api.callbacks.on_update_playstate = lambda _: self.unlockAsking()
        self.preventAsking = True
        self.askLock = threading.RLock()
        self.playerStateChangeLock = threading.RLock()
           
    def drop(self):
        pass

    def lockAsking(self):
        self.preventAsking = True
        
    def unlockAsking(self):
        self.preventAsking = False
    
    def set_speed(self, value):
        pass
    
    def __testMpcReady(self):
        i = 0
        while self.preventAsking:
            if(i >= 100):
                raise Exception("Player failed opening file")
            i+=1
            time.sleep(0.1)

    def make_ping(self):
        try:
            self.__testMpcReady()
            self.mpc_api.callbacks.on_update_filename = self.handleUpdatedFilename
            self.__syncplayClient.initPlayer(self)
            self.handleUpdatedFilename(self.mpc_api.fileplaying)
            self.ask_for_status()
        except:
            pass
        
    def display_message(self, message):
        try:
            self.mpc_api.send_osd(message, 2, 3000)
        except Exception, err:
            self.mpc_error(err)

    def set_paused(self, value):
        try:
            self.playerStateChangeLock.acquire()
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
        finally:
            self.playerStateChangeLock.release()

    def set_position(self, value):
        try:
            self.playerStateChangeLock.acquire()
            self.mpc_api.seek(value)
        except MPC_API.PlayerNotReadyException:
            self.set_position(value)
            return
        except Exception, err:
            self.mpc_error(err)
        finally:
            self.playerStateChangeLock.release()


    def ask_for_status(self):
        try:
            if(not self.preventAsking and self.mpc_api.is_file_ready() and self.askLock.acquire(0)):
                try:
                    position = self.mpc_api.ask_for_current_position()
                    paused = self.mpc_api.is_paused()
                    position = float(position)
                    if(not self.preventAsking and self.mpc_api.is_file_ready()):
                        self.__syncplayClient.updatePlayerStatus(paused, position)
                    else:
                        self._echoGlobalStatus()
                finally:
                    self.askLock.release()    
            else:
                self._echoGlobalStatus()
        except MPC_API.PlayerNotReadyException:
            self.ask_for_status()
        except Exception, err:
            self.mpc_error(err)
            
    def _echoGlobalStatus(self):
        self.__syncplayClient.updatePlayerStatus(self.__syncplayClient.global_paused, self.__syncplayClient.getGlobalPosition())
        
    def __pauseChangeCheckLoop(self, i, changeFrom):
        try:
            self.playerStateChangeLock.acquire()
            if(i < 10):
                if(self.mpc_api.is_paused() <> changeFrom):
                    return
                else:
                    time.sleep(0.1)
                    self.__pauseChangeCheckLoop(i+1, changeFrom)
        finally:
            self.playerStateChangeLock.release()
                
    def __forcePause(self):
        try:
            self.playerStateChangeLock.acquire()
            self.__pauseChangeCheckLoop(0, True)
            self.set_paused(True)
        finally:
            self.playerStateChangeLock.release()

    def __setUpStateForNewlyOpenedFile(self, position):
        try:
            self.playerStateChangeLock.acquire()
            self.__forcePause()
            self.mpc_api.seek(position)
        except MPC_API.PlayerNotReadyException:
            time.sleep(0.1)
            self.__setUpStateForNewlyOpenedFile(position)
        finally:
            self.playerStateChangeLock.release()
        
    def handleUpdatedFilename(self, filename):
        try:
            self.askLock.acquire()
            position = self.__syncplayClient.getGlobalPosition()
            self.__setUpStateForNewlyOpenedFile(position)
            self.__syncplayClient.updateFile(str(filename.encode('ascii','replace')), self.mpc_api.fileduration, self.mpc_api.filepath)
        finally:
            self.askLock.release()
        
    def mpc_error(self, err=""):
        self.__syncplayClient.stop()


def run_mpc(manager, mpc_path, file_path, args):
    mpc = MPCHCAPIPlayer(manager)
    mpc.mpc_api.callbacks.on_connected = lambda: mpc.mpc_api.open_file(file_path) if(file_path) else None
    mpc.mpc_api.start_mpc(mpc_path, args)