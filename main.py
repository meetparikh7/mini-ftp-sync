#!/usr/bin/env python3

import socket
import util

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65431        # The port used by the server

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            print("prompt>", end=" ")
            command = input()
            util.send(s, command)
            print(util.recv(s))
