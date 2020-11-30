#!/usr/bin/env python3

import socket
import util

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65431  # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_serv:
    socket_serv.bind((HOST, PORT))
    socket_serv.listen()
    sock, addr = socket_serv.accept()
    with sock:
        print("Connected by", addr)
        while True:
            command = util.recv(sock)
            util.send(sock, command)

if __name__ == "__main__":
    pass
