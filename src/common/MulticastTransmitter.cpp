#include "MulticastTransmitter.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>

#include "Debugger.hpp"

#include <iostream>
#include <string>

bool MulticastTransmitter::Test() {
    int socket_file_descriptor;
    int new_socket;
    int value_read;
    int opt = 1;
    char buffer[1024] = {0};
    std::string hello = "Hello from server!";

    Debugger::Get().Log("Creating socket file descriptor...");
    if ((socket_file_descriptor = socket(AF_INET, SOCK_DGRAM, 0)) == 0)
    {
        Debugger::Get().Log("Socket creation failed!");
        return false;
    }

    Debugger::Get().Log("Setting socket options...");
    if (setsockopt(socket_file_descriptor, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)))
    {
        Debugger::Get().Log("Failed to set socket options!");
        return false;
    }

    Debugger::Get().Log("Creating address information...");
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_UNSPEC_GROUP; // Specify multicast address 224.0.0.1
    address.sin_port = htons(MULTICAST_PORT);

    Debugger::Get().Log("Binding socket options and address...");
    int bind_result = bind(socket_file_descriptor, (struct sockaddr *) &address, sizeof(address));
    if (bind_result < 0) {
        Debugger::Get().Log("Socket options binding failed!");
        return false;
    }

    Debugger::Get().Log("Listening on multicast socket port: " + MULTICAST_PORT);
    int listen_result = listen(socket_file_descriptor, 4);
    if (listen_result < 0) {
        Debugger::Get().Log("Socket listening error!");
        return false;
    }
    
    Debugger::Get().Log("Receiving message!");
    int bytes_received = accept(socket_file_descriptor, (struct sockaddr *) &address, (socklen_t*) &addrlen);
    if (bytes_received < 0) {
        // A negative return corresponds to an error.
        Debugger::Get().Log("Socket accepting connection error!");
        return false;
    }

    value_read = read(new_socket, buffer, 1024);
    if (value_read < 0) {
        Debugger::Get().Log("Failed to receive message.");    
        return false;
    }
    std::string readtext = buffer;
    std::cout << readtext << std::endl;

    // Send message back
    Debugger::Get().Log("Message read! Sending acknowledge.");
    int bytes_sent = send(socket_file_descriptor, hello.data(), hello.length(), 0);
    if (bytes_sent < 0) {
        Debugger::Get().Log("Failed to send message.");
        return false;
    }

    Debugger::Get().Log("All steps done successfully!");
    return true;
}