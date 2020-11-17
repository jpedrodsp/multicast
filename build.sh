#!/bin/bash
BUILD_DIR="$(pwd)/build"

mkdir BUILD_DIR

# Build server
echo "Building server executable..."
g++ src/server/*.cpp -o BUILD_DIR/server

# Build client
echo "Building client executable..."
g++ src/client/*.cpp -o BUILD_DIR/client