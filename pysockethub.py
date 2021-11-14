"""

Features:
    x Option to specify host:port[:max_connections] to listen on.
        x max_connections limits how many connections on a port.  Default is 10.
        x Multiple listen ports are supported by duplicating the cmd line option.
    - Option to specify host:port[:auto_reconnect] to make outgoing connection to.
        x Multiple outgoing connections are supported.
        x auto_reconnect will attempt to reconnect on a disconnection
        - Option for reconnect delay - adaptive vs. fixed
    - Option to enable logging
        Multiple formats are supported:
            raw: binary, all data as it arrives goes into a file
            frames: binary, but has a frame with some header information indicating the source of the data
            hex: similar to frames to header is in readable ascii and data is in hex
            ptp: PTP telemetry format
    - Option to enable debug output to screen with hex or ascii + timestamps
    - Option to output summary stats table at fixed rate or on activity (with rate limiting)
    - Option to restrict incoming connections by IP range (whitelist / blacklist)

    - Support "plugin" for binary logging formats: calls fn with (host, port,
      data).  Allows stateful parsing of data streams for frame
      synchronization, etc.

tests:
    - What happens when remote end doesn't recv
    - Correctly handle loopback (not allowed) - client <-> server = error
    - hostnames vs. IPs (particularly in the binary loggers that include this info)

todo:
    x colored log messages
    - option to suppress color
    - rename on-screen logging to something else (logging = to disk)
    - rename client / server -> client / server?
    - add logging
    - docstrings
    - diagrams
    - logo
    - mention socat in docs (http://www.dest-unreach.org/socat/)
    - add .reg file for windows users

"""

# System imports
import argparse
import collections
import datetime
import logging
import platform
import queue
import select
import socket
import sys
import threading
import time

# Third-party imports
import hexdump

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
    def __init__(self, host, port, max_connections):
        self.host = host
        self.port = port
        self.max_connections = max_connections
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

    def handle_readable(self, sock):
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
    def __init__(self, host, port, auto_reconnect=True):
        self.host = host
        self.port = port
        self.auto_reconnect = auto_reconnect
        self.sockets = []  # Holds zero or one sockets
        self.last_readable = None
        self.thread = None
        self.keep_running = True
        self._connect()

    def _do_connect(self):
        # Create the socket and try to connect

        while self.keep_running:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            try:
                sock.connect((self.host, self.port))
            except socket.timeout as exc:
                sock.close()
                del sock
                log.debug('timeout %s', str(exc))
                # time.sleep(1)
                continue
            except OSError as exc:
                sock.close()
                del sock
                log.debug('OSError %s %s %s', str(exc), repr(self.host), repr(self.port))
                # time.sleep(1)
                continue

            self.sockets.append(sock)
            log.info("Connected to %s:%d", self.host, self.port)
            break

    def _connect(self):
        # daemon=True allows ^C to shut down the application during connect
        # (), but may leave a stale connection hanging around.
        # self.thread = threading.Thread(target=self._do_connect, daemon=True)
        self.thread = threading.Thread(target=self._do_connect)
        self.thread.start()

    def shutdown(self):
        self.keep_running = False
        if self.sockets:
            self.sockets[0].close()

    def handle_readable(self, sock):
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

        return data

    def distribute(self, data):
        if self.sockets:
            if self.sockets[0] is not self.last_readable:
                self.sockets[0].send(data)
        self.last_readable = None

class HexdumpLogger:
    def __init__(self, args):
        self.sock_to_color_map = {}
        self.args = args
        self.enabled = args.logfmt == 'hexdump'

    def log(self, data, sock):
        if not self.enabled:
            return
        try:
            color = self.sock_to_color_map[sock]
        except KeyError:
            color = PALETTE[len(self.sock_to_color_map) % len(PALETTE)]
            self.sock_to_color_map[sock] = color

        hdump = hexdump.hexdump(data, result='return')
        hdump = getattr(ansicolor.fore, color) + hdump + ansicolor.style.RESET
        addr, port = sock.getpeername()
        log.info("Received %d bytes from %s:%d:\n%s",
                 len(data), addr, port, hdump)

class TableLogger:
    def __init__(self, args):
        self.sock_to_color_map = {}
        self.sock_rx_bytes = collections.defaultdict(int)
        self.args = args
        self.last_dt = datetime.datetime(1900, 1, 1, 0, 0, 0)
        self.max_dt = datetime.timedelta(seconds=1)
        self.enabled = args.logfmt == 'table'

    def log(self, data, sock):
        if not self.enabled:
            return

        self.sock_rx_bytes[sock] += len(data)


    def show(self, sockets):
        if not self.enabled:
            return
        now = datetime.datetime.now()
        if not (now - self.last_dt) > self.max_dt:
            return

        self.last_dt = now

        lines = []
        # all_socks = list(set(sockets + list(self.sock_rx_bytes.keys())))
        # for sock in all_socks:
        for sock in sockets:
        # for sock, rx_bytes in self.sock_rx_bytes.items():
            try:
                rx_bytes = self.sock_rx_bytes[sock]
            except KeyError:
                rx_bytes = 0

            connected = sock in sockets

            try:
                addr, port = sock.getpeername()
            except OSError:
                continue

            try:
                color = self.sock_to_color_map[sock]
            except KeyError:
                color = PALETTE[len(self.sock_to_color_map) % len(PALETTE)]
                self.sock_to_color_map[sock] = color

            line = f'{getattr(ansicolor.fore, color)}{addr}:{port}\t{rx_bytes}\t{connected}{ansicolor.style.RESET}'
            lines.append(line)

        if lines:
            log.info('%s', '\n' + "\n".join(lines))
        else:
            log.info("Awaiting connections...")


def main(args):
    hex_logger = HexdumpLogger(args)
    table_logger = TableLogger(args)

    servers = []
    for arg in args.listen:
        listen_host, listen_port, max_connections = validate_listen_arg(arg)
        server = SocketServer(listen_host, listen_port, max_connections)
        servers.append(server)
        log.info("Listening on %s:%d (max_connections:%d)",
                 listen_host, listen_port, max_connections)

    clients = []
    for arg in args.remote:
        host, port, auto_reconnect = validate_remote_arg(arg)
        client = SocketClient(host, port, auto_reconnect)
        clients.append(client)
        msg = "Establishing outbound connection to %s:%d (auto_reconnect:%s)"
        log.info(msg, host, port, auto_reconnect)

    log.info("Hub running.  Press ^C to exit.")
    keep_running = True
    select_timeout = .1
    try:
        while keep_running:
            time.sleep(.1)

            select_sockets = flatten([l.sockets() for l in servers])
            select_sockets += flatten([c.sockets for c in clients])
            if not select_sockets:
                time.sleep(select_timeout)
                log.debug('continue')
                continue

            rlist, _wlist, _xlist = select.select(select_sockets,
                                                  [],
                                                  [],
                                                  select_timeout)
            for sock in rlist:
                data = None
                for item in servers + clients:
                    data = item.handle_readable(sock)
                    if data:
                        break

                if data:
                    # Distribute received data to all other connections
                    for item in servers + clients:
                        item.distribute(data)

                    hex_logger.log(data, sock)
                    table_logger.log(data, sock)

            table_logger.show(select_sockets)

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

    help_msg = "Local interface and port to listen on.  host:port[:max_connections]."
    help_msg += "  Option may be specified multiple times."
    group.add_argument("-l", "--listen", action='append', default=[],
                       help=help_msg)

    help_msg = "Remote host to call.  host:port[:auto_reconnect] auto_reconnect:true/false."
    help_msg += "  Option may be specified multiple times."
    group.add_argument("-r", "--remote", action='append', default=[],
                       help=help_msg)

    parser.add_argument("-g", "--log", default='False',
                       help="Enable logging to disk")

    parser.add_argument("--logfmt", default='hexdump', choices=['hexdump', 'table'],
                       help="On-screen log format.")

    parser.add_argument("-c", "--color", default='True',
                        help="Enable colored output")

    args = parser.parse_args()

    # Convert the bool arg strings to bool
    args.log = validate_bool(args.log)
    args.color = validate_bool(args.color)

    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)
