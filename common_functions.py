import sys, os
import ConfigParser
import argparse

def stdin_thread(manag):
    try:
        fd = sys.stdin.fileno()
        while True:
            data = os.read(fd, 1024)
            if not data:
                break   
            manag.execute_command(data.rstrip('\n\r'))
    except:
        pass
    
def get_configuration():
    parser = argparse.ArgumentParser(description='Synchronize multiple players over the web.',
                                     epilog='If no options supplied config values will be used')
    parser.add_argument('host', metavar='host', type=str, nargs='?', help='server\'s address')
    parser.add_argument('name', metavar='name', type=str, nargs='?', help='desired username')
    parser.add_argument('args', metavar='opts', type=str, nargs='*', help='player options, if you need to pass options starting with - prepend them with single \'--\' argument') 
    args = parser.parse_args()

    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read('syncplay.ini')
    try:
        if(args.host == None):
            host = config.get('sync', 'host')
        else:
            host = args.host
        if(args.name == None):
            name = config.get('sync', 'name')
        else:
            name = args.name
    except ConfigParser.NoSectionError:
        sys.exit("Host or username not specified")        

    with open('syncplay.ini', 'wb') as configfile:
        try:
            config.set('sync', 'host' ,host)
            config.set('sync', 'name' ,name)
        except ConfigParser.NoSectionError:
            config.add_section('sync')
            config.set('sync', 'host' ,host)
            config.set('sync', 'name' ,name)
        config.write(configfile)
        
    if ':' in host:
        host, port = host.split(':', 1)
        port = int(port)
    else:
        port = 8999
    return host,port,name,args.args