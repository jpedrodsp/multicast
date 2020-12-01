import socket
import struct
import sys

import multicast
import utils

utils.log("Loading configuration...")
multicast_group = (multicast.MULTICAST_GROUP, multicast.MULTICAST_PORT_EXPRESSION)

# Create the UDP datagram socket and configure a few options
utils.log("Pre-configuring socket...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)                                                  # Timeout in seconds
ttl = struct.pack('b', 1)                                           # Set TTL to 1 hop (limits the network reach to local-only)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)    # Define socket options

expression_string = bytes(input("Please input your expression here:"), "utf-8")

utils.log("Sending expression for processing...")
try:
    # Send multicast message
    sent = sock.sendto(expression_string, multicast_group)
    # Wait for response
    msg_count = 0
    while True:
        try:
            recv_message, server_address = sock.recvfrom(multicast.MULTICAST_BUFFER_SIZE_BYTES)
            if recv_message:
                msg_count += 1
        except socket.timeout:
            if msg_count <= 0:
                utils.log("ERROR: No server response received. Please try again.")
            break
        else:
            utils.log('Received {!r} from {}'.format(recv_message, server_address))
finally:
    utils.log("Closing socket and server...")
    sock.close()