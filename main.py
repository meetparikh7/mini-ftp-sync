#!/usr/bin/env python3

import os
import socket

import commands
import util

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65431        # The port used by the server
CLIENT_DIR = "client_dir"


if __name__ == "__main__":
    os.makedirs("client_dir", exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            while True:
                print("prompt>", end=" ")
                command = input()
                command_split = util.split_command(command)
                util.send(s, command)
                if command.strip() == "exit":
                    break
                elif command_split[0] == "download":
                    num_chunks = int(util.recv(s))
                    filename = command_split[1]
                    with open(os.path.join(CLIENT_DIR, filename), 'wb') as f:
                        for i in range(num_chunks):
                            print(f"Received chunk {i} of {num_chunks}")
                            f.write(util.recv_bytes(sock))
                elif command_split[0] == "upload":
                    filename = command_split[1]
                    util.send(s, str(commands.num_chunks(CLIENT_DIR, filename)))
                    for data in commands.download(CLIENT_DIR, filename):
                        util.send_bytes(s, data)
                else:
                    print(util.recv(s))
        except:
            print("Server broke connection unexpectedly")
            import traceback; traceback.print_exc()
        finally:
            s.close()
