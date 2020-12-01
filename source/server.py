import socket
import struct
import sys

# Multicast utilities and configurations
import multicast
import utils

# Threading utilities
import threading
import time

def multicast_ping_retrieve_id():
    pingsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pingsock.settimeout(0.5)                                                  # Timeout in seconds
    ttl = struct.pack('b', 1)                                               # Set TTL to 1 hop (limits the network reach to local-only)
    pingsock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)    # Define socket options
    multicast_pingaddress = (multicast.MULTICAST_GROUP, multicast.MULTICAST_PORT_PING)
    bytes_sent = pingsock.sendto(b'PING', multicast_pingaddress)
    server_id = 1
    msg_count = 0
    responded = []
    while True:
        try:
            recv_message, sender_address = pingsock.recvfrom(multicast.MULTICAST_BUFFER_SIZE_BYTES)
            if recv_message:
                msg_count += 1
                received_id = int(recv_message.decode("utf-8"))
                utils.log('Response from ID: {}'.format(recv_message))
                responded.append(received_id)
                if received_id >= server_id:
                    server_id = received_id + 1
        except socket.timeout:
            if msg_count <= 0:
                utils.log("ERROR: No ping response received. Please try again.")
            break
    pingsock.close()
    return server_id, responded

def multicast_ping_respond(server_id):
    utils.log("Preparing responding listening socket for server {}...".format(server_id))
    local_address = ("", multicast.MULTICAST_PORT_PING)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(local_address)
    group = socket.inet_aton(multicast.MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        recv_message, client_address = sock.recvfrom(multicast.MULTICAST_BUFFER_SIZE_BYTES)
        msg = recv_message.decode("utf-8")
        if msg == "PING":
            utils.log("Responding ping message as server {}...".format(server_id))
            id_bytestr = str(server_id).encode("utf-8")
            sent = sock.sendto(id_bytestr, client_address)

def multicast_should_respond_expression(server_id):
    __server_id, responded = multicast_ping_retrieve_id()
    utils.log("Servers responded: {}".format(responded))
    responded.sort()
    if server_id in responded:
        if responded.index(server_id) == 0:
            return True
    return False

if __name__ == "__main__":
    utils.log("Initializing and retrieving server id...")
    server_id, responded = multicast_ping_retrieve_id()
    if server_id == None:
        utils.log("Failed to define server id")
        exit(1)
    utils.log("Setting server id to: {}".format(server_id))

    multicast_group = multicast.MULTICAST_GROUP
    server_address = ('', multicast.MULTICAST_PORT_EXPRESSION)

    # Create the respond socket
    utils.log("Creating ping responding socket...")
    ping_responding_thread = threading.Thread(target=multicast_ping_respond, args=[server_id])
    ping_responding_thread.start()

    # Create the UDP socket and bind it to network interface
    utils.log("Creating expressions socket...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    utils.log("Socket is now listening for expressions...")
    while True:
        recv_message, client_address = sock.recvfrom(multicast.MULTICAST_BUFFER_SIZE_BYTES)
        utils.log("Received message from [{}]: {}".format(client_address, recv_message))
        # Check with other servers who will respond the requisition
        should_respond = multicast_should_respond_expression(server_id)
        if should_respond:
            utils.log("Responding expression calculation...")
            expression = recv_message.decode("utf-8")
            solved_data = utils.resolve_expression(expression)
            utils.log("Sending: {}".format(solved_data))
            sock.sendto(str(solved_data).encode("utf-8"), client_address)
        else:
            utils.log("Ignoring expression calculation...")
    
    ping_responding_thread.stop()