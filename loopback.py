"""
Implements a minimal socket server with optional loopback capability.
This program is used for debugging network connections.

Loopback can be enabled or disabled by uncommenting the line contining
"conn.send(data)".

Features:
    - Gracefully closes on ^C
    - ^C closes connection when connected
    - ^C exits the program when not connected (waiting for connection)
    - Returns to listening state when client disconnects
    - Only one client at a time supported
    - Logs received data to screen with timestamp in hexdump format

Operation:
    python3 loopback.py

"""


import logging
import socket
import sys

import hexdump

# Globals
log = logging.getLogger(__name__)
HOST = '127.0.0.1'
PORT = 5000

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

def set_debug(state):
    """Enables debugging output by installing a log handler for this module's logger"""
    if state:
        if not log.handlers:
            log_handler = logging.StreamHandler()
            fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
            datefmt = '%Y-%m-%d %H:%M:%S'
            log_formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
            log_handler.setFormatter(log_formatter)
            log.addHandler(log_handler)
            log.setLevel(logging.DEBUG)
    else:
        # Remove existing handlers
        for handler in log.handlers:
            log.removeHandler(handler)

set_debug(True)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
s.settimeout(.1)

while True:
    log.info("Waiting for connection on port %d" % (PORT))
    try:
        while True:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                pass
            else:
                break
    except KeyboardInterrupt:
        log.info("Got KeyboardInterrupt")
        sys.exit(0)

    conn.settimeout(.1)
    log.info("Got connection")
    try:
        while True:
            try:
                data = conn.recv(1024)
            except socket.timeout:
                pass
            except ConnectionResetError:
                log.info('Connection reset by remote client')
                break
            else:
                if data:
                    dump_str = hexdump.hexdump(data, result='return')
                    log.info("Received:\n" + dump_str)
                else:
                    log.info('Disconnected')
                    break
                # conn.send(data)  # Loopback the received data
    except KeyboardInterrupt:
        conn.close()
        log.info("Got KeyboardInterrupt")

log.info('Done')
