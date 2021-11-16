# pysockethub

Distributes data received on one socket to all other connected sockets.

Supports multiple inbound and outbound sockets.

Example usage:

Listen on port 1234 for up to 10 incoming connections:

`python pysockethub.py -l 0.0.0.0:1234`