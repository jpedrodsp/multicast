# socket_multicast_receiver.py
import socket
import struct
import sys
import multicast
import utils

def multicast_ping_retrieve_id():
    pingsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pingsock.settimeout(1)                                                  # Timeout in seconds
    ttl = struct.pack('b', 1)                                               # Set TTL to 1 hop (limits the network reach to local-only)
    pingsock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)    # Define socket options
    multicast_pingaddress = (multicast.MULTICAST_GROUP, multicast.MULTICAST_PORT_PING)
    bytes_sent = pingsock.sendto(b'PING', multicast_pingaddress)
    server_id = 1
    msg_count = 0
    while True:
        try:
            recv_message, sender_address = pingsock.recvfrom(multicast.MULTICAST_BUFFER_SIZE_BYTES)
            if recv_message:
                msg_count += 1
                received_id = int(recv_message.decode("utf-8"))
                utils.log('Response from ID: {}'.format(recv_message))
                if received_id >= server_id:
                    server_id = received_id + 1
        except socket.timeout:
            if msg_count <= 0:
                utils.log("ERROR: No ping response received. Please try again.")
            break
    pingsock.close()
    return server_id

def multicast_ping_respond(server_id):
    utils.log("Preparing listening socket for server {}...".format(server_id))
    local_address = ("", multicast.MULTICAST_PORT_PING)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(local_address)
    group = socket.inet_aton(multicast.MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    pass

if __name__ == "__main__":
    utils.log("Initializing and retrieving server id...")
    server_id = multicast_ping_retrieve_id()
    if server_id == None:
        utils.log("Failed to define server id")
        exit(1)
    utils.log("Setting server id to: {}".format(server_id))

    multicast_group = multicast.MULTICAST_GROUP
    server_address = ('', multicast.MULTICAST_PORT_EXPRESSION)

    # Create the UDP socket and bind it to network interface
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        recv_message, client_address = sock.recvfrom(multicast.MULTICAST_BUFFER_SIZE_BYTES)
        utils.log("Received message from [{}]: {}".format(client_address, recv_message))
        expression = recv_message.decode("utf-8")
        solved_data = utils.resolve_expression(expression)
        utils.log("Sending: {}".format(solved_data))
        sock.sendto(str(solved_data).encode("utf-8"), client_address)