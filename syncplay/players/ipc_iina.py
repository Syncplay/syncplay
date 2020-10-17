import os.path
import subprocess
import time

from syncplay.players.python_mpv_jsonipc.python_mpv_jsonipc import log, MPV, MPVError, MPVProcess
from syncplay.utils import resourcespath

class IINA(MPV):
    """The main IINA interface class. Use this to control the MPV player instantiated by IINA."""

    def _start_mpv(self, ipc_socket, mpv_location, **kwargs):
        # Attempt to start IINA 3 times.
        for i in range(3):
            try:
                self.mpv_process = IINAProcess(ipc_socket, mpv_location, **kwargs)
                break
            except MPVError:
                log.warning("IINA start failed.", exc_info=1)
                continue
        else:
            raise MPVError("IINA process retry limit reached.")

class IINAProcess(MPVProcess):
    """
    Manages an IINA process, ensuring the socket or pipe is available. (Internal)
    """

    def _start_process(self, ipc_socket, args):
        self.process = subprocess.Popen(args)
        ipc_exists = False
        for _ in range(100): # Give IINA 10 seconds to start.
            time.sleep(0.1)
            self.process.poll()
            if os.path.exists(ipc_socket):
                ipc_exists = True
                log.debug("Found IINA socket.")
                break
            if self.process.returncode != 0: # iina-cli returns immediately after its start
                log.error("IINA failed with returncode {0}.".format(self.process.returncode))
                break
        else:
            self.process.terminate()
            raise MPVError("IINA start timed out.")
        
        if not ipc_exists or self.process.returncode != 0:
            self.process.terminate()
            raise MPVError("IINA not started.")

    def _get_arglist(self, exec_location, **kwargs):
        args = [exec_location]
        args.append(resourcespath + 'iina-bkg.png')
        self._set_default(kwargs, "mpv-input-ipc-server", self.ipc_socket)
        args.extend("--{0}={1}".format(v[0].replace("_", "-"), self._mpv_fmt(v[1]))
                    for v in kwargs.items())
        return args
