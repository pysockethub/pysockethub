# pysockethub

[](/img/logo_arrows.png)

Distributes data received on one socket to all other connected sockets.

Supports multiple inbound and outbound sockets.

Example usage:

Listen on port 1234 for up to 10 incoming connections:
 - `python pysockethub.py -l 0.0.0.0:1234`

Listen on port 1234 for up to 2 connections and port 2345 for up to 3 connections:
 - `python pysockethub.py -l 0.0.0.0:1234:2 -l 0.0.0.0:2345:3`

Connect to foo.com:1234 and listen for connections on port 1234:
 - `python pysockethub.py -r foo.com:1234 -l 0.0.0.0:1234`

Full usage:
```
usage: pysockethub.py [-h] (-l LOCAL | -r REMOTE) [--status STATUS] [--statusfmt {hexdump,table}] [--color COLOR] [-o LOGFILENAME]
                      [-t TIMESTAMP] [--logfmt {raw,frames,hexdump} | --logplugin LOGPLUGIN]

Python TCP Socket Hub - Distributes data to connected clients. If no options are specified, listens for up to 10 connections on
localhost:1234

optional arguments:
  -h, --help            show this help message and exit
  -l LOCAL, --local LOCAL
                        Local interface and port to serve connections on. host:port[:max_connections]. Option may be specified multiple
                        times. (default: [])
  -r REMOTE, --remote REMOTE
                        Remote host to connect to. host:port[:auto_reconnect] auto_reconnect:true/false. Option may be specified
                        multiple times. (default: [])
  --status STATUS       Display status messages during program operation. (default: True)
  --statusfmt {hexdump,table}
                        Specifies format of status messages. (default: table)
  --color COLOR         Enable colored output (default: True)
  -o LOGFILENAME, --logfilename LOGFILENAME
                        Output filename for logging (default: None)
  -t TIMESTAMP, --timestamp TIMESTAMP
                        If True, filenames will be prepended with yyyymmdd_hhmmss_ (default: True)
  --logfmt {raw,frames,hexdump}
                        Log file format. (default: raw)
  --logplugin LOGPLUGIN
                        Plugin name. A python module named psh_<name> containing a log(sock, data) function. (default: None)
```
