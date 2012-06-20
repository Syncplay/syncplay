#coding:utf8
import thread
import sys, os

from twisted.internet import reactor

from syncplay import client
from syncplay.players import mpc

def stdin_thread(sock):
    try:
        fd = sys.stdin.fileno()
        while True:
            data = os.read(fd, 1024)
            if not data:
                break   
            sock.execute_command(data.rstrip('\n\r'))
    except:
        pass

if __name__ == '__main__':
    args = sys.argv[1:]
    host = args.pop(0) 
    name = args.pop(0) 
    if ':' in host:
        host, port = host.split(':', 1)
        port = int(port)
    else:
        port = 8999
    manager = client.Manager(host, port, name, lambda m: mpc.run_mpc(m))
    thread.start_new_thread(stdin_thread, (manager,))
    manager.start()
