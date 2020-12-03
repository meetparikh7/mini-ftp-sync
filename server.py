#!/usr/bin/env python3

import socket
import commands
import util

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65431  # Port to listen on (non-privileged ports are > 1023)
BASEPATH = "test_dir"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_serv:
    socket_serv.bind((HOST, PORT))
    socket_serv.listen()
    sock, addr = socket_serv.accept()
    with sock:
        print("Connected by", addr)
        while True:
            command = util.recv(sock)
            command = command.strip().split(" ")
            command = list(filter(lambda v: v, command))
            toret = ""
            if command[0] == "ls":
                long = False
                if "-l" in command:
                    long  = True
                toret = commands.ls(BASEPATH, long)
            elif command[0] == "hash":
                toret = commands.hashfile(BASEPATH, command[1])
            elif command[0] == "exit":
                break
            util.send(sock, toret)

if __name__ == "__main__":
    pass
