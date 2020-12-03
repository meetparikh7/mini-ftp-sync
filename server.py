#!/usr/bin/env python3

import socket
import commands
import util

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65431  # Port to listen on (non-privileged ports are > 1023)
BASEPATH = "test_dir"


def execute_command(command):
    if command[0] == "ls":
        long = False
        if "-l" in command:
            long  = True
        return commands.ls(BASEPATH, long)
    elif command[0] == "hash":
        return commands.hashfile(BASEPATH, command[1])


def main(socket_serv):
    socket_serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_serv.bind((HOST, PORT))
    socket_serv.listen()
    sock, addr = socket_serv.accept()
    try:
        print("Connected by", addr)
        while True:
            command = util.recv(sock)
            command = util.split_command(command)
            if command[0] == "exit":
                break
            elif command[0] == "download":
                filename = command[1]
                util.send(sock, str(commands.num_chunks(BASEPATH, filename)))
                for data in commands.download(BASEPATH, filename):
                    util.send_bytes(sock, data)
            else:
                toret = execute_command(command) or "Invalid command!"
                util.send(sock, toret)
    finally:
        sock.close()

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_serv:
        try:
            main(socket_serv)
        except:
            print("Unexpected error encountered")
            import traceback; traceback.print_exc()
        finally:
            socket_serv.close()
