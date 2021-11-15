"""

Features:
    x Option to specify host:port[:max_connections] to listen on.
        x max_connections limits how many connections on a port.  Default is 10.
        x Multiple listen ports are supported by duplicating the cmd line option.
    x Option to specify host:port[:auto_reconnect] to make outgoing connection to.
        x Multiple outgoing connections are supported.
        x auto_reconnect will attempt to reconnect on a disconnection
        x Option for reconnect delay - adaptive vs. fixed
    x Option to enable logging
    x Option to specify log format
        x raw: binary, all data as it arrives goes into a file
        x frames: binary, but has a frame with some header information indicating the source of the data
        x hex: similar to frames but header is in readable ascii and data is in hex
        x plugin: calls user-supplied function (specify plugin module name on cmdline)
    x Option to enable debug output to screen with hex or ascii + timestamps
    x Option to output summary stats table at fixed rate
    - Option to restrict incoming connections by IP range (whitelist / blacklist)
    - Option to make connections recv only (no tx)

tests:
    - plugin path resolution (may need to add option to specify path to plugin module?)
    - What happens when remote end doesn't recv
    - Correctly handle loopback (not allowed) - client <-> server = error
    - hostnames vs. IPs (particularly in the binary loggers that include this info)

todo:
    - option for timestamp in log filename
    - docstrings
    - diagrams
    - logo
    - mention socat / netcat in docs (http://www.dest-unreach.org/socat/)
    - add .reg file for windows users
    - ability to make some connections recv only (don't accept any data from the remote side)
    - installer - adds to python scripts path

"""

# System imports
import argparse
import collections
import importlib
import logging
import pkgutil
import select
import socket
import struct
import sys
import threading
import time


# Third-party imports
import hexdump
import prettytable

# Local imports
import ansicolor
import colorlog

# Globals
MAX_CONNECTIONS_DEFAULT = 10
AUTO_RECONNECT_DEFAULT = True
LOCK = threading.Lock()  # Protects access to socket lists between threads
LOG_LEVEL = logging.DEBUG

PALETTE = ['DEEP_SKY_BLUE_1', 'DARK_ORANGE', 'LIGHT_YELLOW', 'LIGHT_RED',
           'GREEN_1', 'PLUM_2']

def setup_log():
    global log
    logging.setLoggerClass(colorlog.ColorLog)
    log = logging.getLogger(__name__)
    log_handler = logging.StreamHandler()
    log_formatter = colorlog.ColorFormatter()
    log_handler.setFormatter(log_formatter)
    log.addHandler(log_handler)
    log.setLevel(LOG_LEVEL)

setup_log()

# Code
def validate_port(arg):
    try:
        port = int(arg)
    except ValueError:
        msg = f'ERROR: Port must be a number (got {repr(arg)})'
        log.error('Port must be a number (got %s)', repr(arg))
        sys.exit(1)
    return port

def validate_bool(arg):
    return arg.lower() in ['true', '1']

def validate_listen_arg(arg):
    arg_parts = arg.split(':')

    if len(arg_parts) < 2:
        msg = "Please specify listen arg in format host:port[:max_connections].  (got: %s)"
        log.error(msg, arg)
        sys.exit(1)

    host = arg_parts[0]

    port = validate_port(arg_parts[1])

    if len(arg_parts) > 2:
        # User specified max_connections
        msg = 'max_connections be a positive number (got %s)'
        try:
            max_connections = int(arg_parts[2])
        except ValueError:
            log.error(msg, repr(arg_parts[2]))
            sys.exit(1)

        if max_connections < 1:
            log.error(msg, repr(arg_parts[2]))
            sys.exit(1)

    else:
        # max_connections not specified; use default
        max_connections = MAX_CONNECTIONS_DEFAULT

    return host, port, max_connections

def validate_remote_arg(arg):
    """
    arg: host:port:auto_reconnect
    where:
        auto_reconnect: 0/1 or True/False
    """
    arg_parts = arg.split(':')

    if len(arg_parts) < 2:
        msg = "Please specify remote arg in format host:port[:auto_reconnect]. (got %s)"
        log.error(msg, arg)
        sys.exit(1)

    host = arg_parts[0]

    port = validate_port(arg_parts[1])

    if len(arg_parts) > 2:
        # User specified auto_reconnect
        msg = f'ERROR: auto_reconnect be a positive number (got {repr(arg_parts[2])})'

        auto_reconnect = validate_bool(arg_parts[2])

    else:
        # auto_reconnect not specified; use default
        auto_reconnect = AUTO_RECONNECT_DEFAULT

    return host, port, auto_reconnect

class SocketServer:
    def __init__(self, host, port, max_connections, stats_table):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.stats_table = stats_table
        self.connected_sockets = []
        self.last_readable = None
        self.listen_socket = None
        self._create_listen_socket()

    def shutdown(self):
        for sock in self.sockets():
            sock.close()

    def _create_listen_socket(self):
        # log.debug("_create_listen_socket")
        # Create a listen socket and remember the maximum number connections
        # it supports.
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.listen_socket.bind((self.host, self.port))
        except OSError as exc:
            msg = "Couldn't bind to %s:%d (%s)"
            log.error(msg, self.host, self.port, str(exc))
            sys.exit(1)

        self.listen_socket.listen()
        self.listen_socket.setblocking(False)

    def __contains__(self, item):
        # if item in [self.listen_socket] + self.connected_sockets:
        if item in self.sockets():
            return True
        return False

    def sockets(self):
        """
        Returns a list of all of the socket objects owned by this instance,
        including both the listen socket and any connected client sockets.
        """
        if self.listen_socket:
            return [self.listen_socket] + self.connected_sockets
        return self.connected_sockets

    def service_readable(self, sock):
        data = None

        if not sock in self:
            return None

        if sock is self.listen_socket:
            # Accept incoming connection
            connected_socket, addr = sock.accept()
            self.connected_sockets.append(connected_socket)
            log.info('Accepted connection from: %s', addr)
            # listen_sockets_connections[sock].append(connected_socket)

            # Check to see if the maximum number of connections has
            # been reached.
            if len(self.connected_sockets) >= self.max_connections:
            # if len(listen_sockets_connections[sock]) >= listen_sockets_max_connections[sock]:

                # Close the listening socket so that we don't get any more
                # connections on this port.  We'll have to create a new
                # listen socket and re-key its associated dicts once a slot
                # opens up.
                msg = "Maximum connections (%d) reached on port %d"
                log.info(msg, self.max_connections, self.port)
                sock.close()
                self.listen_socket = None

        else:
            # Recv data
            # A connected socket is readable.  recv the data.

            self.last_readable = sock

            try:
                data = sock.recv(4096)
            except ConnectionResetError:
                self._remove_connected_socket(sock)

            if not data:
                # When recv() returns None or b'', that means the connection
                # is closed.  Mark this socket for removal from the sockets
                # list.
                addr, port = sock.getpeername()
                log.info("Client disconnected (%s:%d)", addr, port)
                self._remove_connected_socket(sock)

            self.stats_table.update_rx(sock, len(data))

        return data

    def _remove_connected_socket(self, sock):
        self.connected_sockets.remove(sock)
        # Re-open the listen socket if it had previously been closed due to
        # max connections.
        if self.listen_socket is None:
        # if len(self.connected_sockets) < self.max_connections:
            self._create_listen_socket()

    def distribute(self, data):
        for sock in self.connected_sockets:
            if sock is not self.last_readable:
                sock.send(data)
                self.stats_table.update_tx(sock, len(data))
        self.last_readable = None


def flatten(lst):
    """
    Given a list of lists (lst), returns a single list containing the contents of
    all the lists in lst.

    e.g.:
        lst = [[1, 2, 3], [4, 5, 6]]
        flatten(lst) -> [1, 2, 3, 4, 5, 6]

    Thanks:
    https://stackoverflow.com/a/952952/9318077
    """
    return [item for sublist in lst for item in sublist]

class SocketClient:
    def __init__(self, host, port, stats_table, auto_reconnect=True):
        self.host = host
        self.port = port
        self.stats_table = stats_table
        self.auto_reconnect = auto_reconnect
        self.sockets = []  # Holds one socket when connected; otherwise empty.
        self.last_readable = None
        self.thread = None
        self.keep_running = True
        self._connect()

    def _do_connect(self):
        # Create the socket and try to connect

        connect_attempts = 1
        while self.keep_running:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Initially retry quickly (10Hz), then back off (1/10Hz).  Note
            # that connect() may timeout sooner than the specified timeout
            # (e.g. after 2 seconds, despite the timeout being set to 10
            # seconds).  An additional delay could be added to strictly limit
            # the rate of connect() attempts.
            timeout = min(10, (.1 * connect_attempts))
            sock.settimeout(timeout)
            connect_attempts += 1

            try:
                sock.connect((self.host, self.port))
            except socket.timeout:
                sock.close()
                del sock
                continue
            except OSError:
                sock.close()
                del sock
                continue

            self.sockets.append(sock)
            log.info("Connected to %s:%d", self.host, self.port)
            break

    def _connect(self):
        # daemon=True allows ^C to shut down the application during connect
        # (), but may leave a stale connection hanging around.
        self.thread = threading.Thread(target=self._do_connect, daemon=True)
        # self.thread = threading.Thread(target=self._do_connect)
        self.thread.start()

    def shutdown(self):
        self.keep_running = False
        if self.sockets:
            self.sockets[0].close()

    def service_readable(self, sock):
        if not sock in self.sockets:
            return None

        self.last_readable = sock
        data = None

        try:
            data = sock.recv(4096)
        except (OSError, ConnectionResetError) as exc:
            # OSError means socket operation timed out while recv'ing.  And,
            # on Windows, it can also mean that the remote end closed the
            # connection.  If so, then winerror will be set and we should
            # disconnect.
            # if platform.system() == 'Windows':
            #     if exc.winerror is not None:
            addr, port = sock.getpeername()
            log.info("Client disconnected (exc) (%s:%d) (%s)", addr, port, str(exc))
            sock.close()
            self.sockets.remove(sock)

            # Launch a thread to reconnect
            if self.auto_reconnect:
                self._connect()

            return None

        if not data:
            # When recv() returns None or b'', that means the connection is
            # closed.  Mark this socket for removal from the sockets list.
            addr, port = sock.getpeername()
            log.info("Client disconnected (%s:%d)", addr, port)
            sock.close()
            self.sockets.remove(sock)
            if self.auto_reconnect:
                self._connect()
            return None

        self.stats_table.update_rx(sock, len(data))

        return data

    def distribute(self, data):
        if self.sockets:
            if self.sockets[0] is not self.last_readable:
                self.sockets[0].send(data)
                self.stats_table.update_tx(self.sockets[0], len(data))
        self.last_readable = None

class HexdumpPrinter:
    def __init__(self):
        self.sock_to_color_map = {}
        self.args = args

    def show(self, sock, data):
        try:
            color = self.sock_to_color_map[sock]
        except KeyError:
            color = PALETTE[len(self.sock_to_color_map) % len(PALETTE)]
            self.sock_to_color_map[sock] = color

        hdump = hexdump.hexdump(data, result='return')
        if self.args.color:
            hdump = getattr(ansicolor.fore, color) + hdump + ansicolor.style.RESET
        addr, port = sock.getpeername()
        log.info("Received %d bytes from %s:%d:\n%s",
                 len(data), addr, port, hdump)

class SocketStatsTable:
    def __init__(self):
        self.sock_to_color_map = {}
        self.tx_bytes = collections.defaultdict(int)
        self.rx_bytes = collections.defaultdict(int)
        self.last_rx_time = {}
        self.args = args
        self.last_show_time = 0
        self.show_delay = 1
        self.awaiting_flag = False

    def update_tx(self, sock, length):
        self.tx_bytes[sock] += length

    def update_rx(self, sock, length):
        self.rx_bytes[sock] += length
        self.last_rx_time[sock] = time.time()

    def show(self, sockets):
        now = time.time()
        if (now - self.last_show_time) < self.show_delay:
            return

        self.last_show_time = now

        lines = []

        for sock in sockets:
            try:
                addr, port = sock.getpeername()
            except OSError:
                # Socket was a listening socket, not a remote connection
                continue

            try:
                idle_sec = int(now - self.last_rx_time[sock])
            except KeyError:
                self.last_rx_time[sock] = now
                idle_sec = 0

            # connected = sock in sockets

            try:
                color = self.sock_to_color_map[sock]
            except KeyError:
                color = PALETTE[len(self.sock_to_color_map) % len(PALETTE)]
                self.sock_to_color_map[sock] = color

            if self.args.color:
                # line = f'{getattr(ansicolor.fore, color)}{addr}:{port}\t{rx_bytes}\t{connected}{ansicolor.style.RESET}'
                line = [f'{getattr(ansicolor.fore, color)}{addr}', port,
                        self.tx_bytes[sock],
                        self.rx_bytes[sock],
                        # f'{(now - self.last_rx_time[sock]).total_seconds()}{ansicolor.style.RESET}']
                        f'{idle_sec}{ansicolor.style.RESET}']
            else:
                # line = f'{addr}:{port}\t{rx_bytes}\t{connected}'
                line = [addr, port, self.tx_bytes[sock], self.rx_bytes[sock], idle_sec]
            lines.append(line)

        if lines:
            table = prettytable.PrettyTable()
            table.field_names = ['addr', 'port', 'tx_bytes', 'rx_bytes', 'rx_idle_sec']
            table.add_rows(lines)
            # log.info('%s', '\n' + "\n".join(lines))
            log.info('%s', '\n' + table.get_string())
            self.awaiting_flag = False
        else:
            if not self.awaiting_flag:
                log.info("Not showing statistics until connection established.")
                self.awaiting_flag = True

class RawLogger:
    """
    Logger that writes bytes straight to disk as they arrive.
    No additional metadata is stored in the file.
    """
    def __init__(self, outfilename):
        self.outfilename = outfilename
        self.logfile = None

    def log(self, sock, data):
        if self.logfile is None:
            self.logfile = open(self.outfilename, 'wb')
            log.info("Opened '%s' for logging (logfmt=raw)", self.outfilename)

        self.logfile.write(data)

class FrameLogger:
    """
    Logger that writes frames with sync, header, and data.

    Format of frame is:
    <sync:2> <time:4> <addr_len:4> <addr:addr_len> <port:2> <data_len:4> <data:data_len>
    """
    def __init__(self, outfilename):
        self.outfilename = outfilename
        self.logfile = None

    def log(self, sock, data):
        if self.logfile is None:
            self.logfile = open(self.outfilename, 'wb')
            log.info("Opened '%s' for logging (logfmt=frames)", self.outfilename)

        # Create a frame
        self.logfile.write(b'\xEB\x90')                   # Frame sync
        now = int(time.time())
        self.logfile.write(struct.pack('>I', now))        # Time data was received
        addr, port = sock.getpeername()
        self.logfile.write(struct.pack('>I', len(addr)))  # Length of addr string
        self.logfile.write(addr.encode())                 # addr
        self.logfile.write(struct.pack('>H', port))       # Port number
        self.logfile.write(struct.pack('>I', len(data)))  # Length of data
        self.logfile.write(data)                          # Received data

class HexLogger:
    """
    Logger that writes hexdump-formatted data.  E.g.:

    2021-11-14 20:01:50.958 127.0.0.1:60910:
        00000000: 6C 6B 6A 0D 0A                                    lkj..
    """
    def __init__(self, outfilename):
        self.outfilename = outfilename
        self.logfile = None

    def log(self, sock, data):
        if self.logfile is None:
            self.logfile = open(self.outfilename, 'w')
            log.info("Opened '%s' for logging (logfmt=hexdump)", self.outfilename)

        # Generate timestamp
        now = time.time()
        time_str = time.strftime('%Y-%m-%d %H:%M:%S.',
                                 time.localtime(now))
        # Tack on subseconds
        subsec = now - int(now)
        msec = int(subsec * 1000)
        time_str += f'{msec:03d} '

        # Tack on sender host and port
        self.logfile.write(time_str)
        addr, port = sock.getpeername()
        self.logfile.write(f'{addr}:{port}:\n')

        # Finally, output an indented hexdump of the data
        for line in hexdump.hexdump(data, result='generator'):
            self.logfile.write('\t' + line + '\n')

def get_logger(args):
    if args.logfilename:
        # Logging to file is enabled.

        if args.logplugin:
            # User specified a custom logger via plugin.

            # Build a dictionary of available plugins.  (Plugins are python
            # modules with names that start with psh_)
            discovered_plugins = {
                name: importlib.import_module(name)
                for finder, name, ispkg
                in pkgutil.iter_modules()
                if name.startswith('psh_')
            }

            log.info("Available plugins: %r", ', '.join(discovered_plugins.keys()))

            # Verify that the module has a log() function.
            plugin_module = discovered_plugins['psh_' + args.logplugin]
            plugin_module.LOGFILENAME = args.logfilename
            if not hasattr(plugin_module, 'log'):
                log.error("Plugin %s has no log() function.", args.logplugin)
                sys.exit(1)

            return plugin_module


        # No plugin; just use one of the default file loggers.
        if args.logfmt == 'raw':
            return RawLogger(args.logfilename)
        if args.logfmt == 'frames':
            return FrameLogger(args.logfilename)
        if args.logfmt == 'hexdump':
            return HexLogger(args.logfilename)

    # Logging to file is not enabled.  Main always calls logger.log(), so we
    # supply a do-nothing logger in this case.
    class DummyLogger:
        def log(self, sock, data):
            pass

    return DummyLogger()

def main(args):
    hex_printer = HexdumpPrinter()
    stats_table = SocketStatsTable()
    show_hex = args.statusfmt == 'hexdump'
    show_table = args.statusfmt == 'table'

    logger = get_logger(args)

    servers = []
    for arg in args.local:
        listen_host, listen_port, max_connections = validate_listen_arg(arg)
        server = SocketServer(listen_host, listen_port, max_connections, stats_table)
        servers.append(server)
        log.info("Serving on %s:%d (max_connections:%d)",
                 listen_host, listen_port, max_connections)

    clients = []
    for arg in args.remote:
        host, port, auto_reconnect = validate_remote_arg(arg)
        client = SocketClient(host, port, stats_table, auto_reconnect)
        clients.append(client)
        msg = "Connecting to %s:%d (auto_reconnect:%s)"
        log.info(msg, host, port, auto_reconnect)

    log.info("Hub running.  Press ^C to exit.")
    keep_running = True
    select_timeout = .1
    try:
        while keep_running:
            time.sleep(.1)

            # Build a list of all the sockets to be waited on with select()
            select_sockets = flatten([l.sockets() for l in servers])
            select_sockets += flatten([c.sockets for c in clients])
            if not select_sockets:
                time.sleep(select_timeout)
                continue

            # Wait for some data to arrive, or for a client to connect to one
            # of our listening sockets.
            rlist, _wlist, _xlist = select.select(select_sockets,
                                                  [],
                                                  [],
                                                  select_timeout)
            for sock in rlist:
                data = None
                for item in servers + clients:
                    data = item.service_readable(sock)
                    if data:
                        break

                if data:
                    # Distribute received data to all other connections
                    for item in servers + clients:
                        item.distribute(data)

                    logger.log(sock, data)

                    if show_hex:
                        hex_printer.show(sock, data)

            if show_table:
                stats_table.show(select_sockets)

    except KeyboardInterrupt:
        # Shut down socket connections and threads
        for item in clients + servers:
            item.shutdown()

def parse_args():
    descr = "Python TCP Socket Hub - Distributes data to connected clients."
    descr += "  If no options are specified, listens for up to 10 connections on localhost:1234"

    parser = argparse.ArgumentParser(description=descr,
                                     # )
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Create a group so that we can require at least one --listen or --remote arg
    group = parser.add_mutually_exclusive_group(required=True)

    help_msg = ("Local interface and port to serve connections on.  host:port[:max_connections]. \
                Option may be specified multiple times.")
    group.add_argument("-l", "--local", action='append', default=[],
                       help=help_msg)

    help_msg = ("Remote host to connect to.  host:port[:auto_reconnect] auto_reconnect:true/false. \
                 Option may be specified multiple times.")
    group.add_argument("-r", "--remote", action='append', default=[],
                       help=help_msg)

    parser.add_argument("--status", default='True',
                       help="Display status messages during program operation.")

    parser.add_argument("--statusfmt", default='table', choices=['hexdump', 'table'],
                       help="Specifies format of status messages.")

    parser.add_argument("--color", default='True',
                        help="Enable colored output")

    parser.add_argument("-o", "--logfilename", default=None,
                        help="Output filename for logging")


    log_group = parser.add_mutually_exclusive_group(required=False)

    log_group.add_argument("--logfmt", default='raw', choices=['raw', 'frames', 'hexdump'],
                           help="Log file format.")

    help_msg = ("Plugin name.  A python module named psh_<name> containing a log(sock, data) \
                function.")
    log_group.add_argument("--logplugin",
                           help=help_msg)

    args = parser.parse_args()

    # Convert the bool arg strings to bool
    args.log = validate_bool(args.status)
    args.color = validate_bool(args.color)

    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)
