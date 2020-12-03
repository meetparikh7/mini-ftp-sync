#!/usr/bin/env python3

import json
import os
import socket

import commands
import file_transfer
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
                elif command_split[0] == "ls":
                    data = util.recv(s)
                    data = json.loads(data)
                    if "-l" in command_split:
                        print(util.format_table(("name", "type", "size"), data))
                    else:
                        print("\n".join(data))
                elif command_split[0] == "download":
                    filename = command_split[1]
                    file_transfer.download_file(s, CLIENT_DIR, filename)
                elif command_split[0] == "upload":
                    filename = command_split[1]
                    file_transfer.upload_file(s, CLIENT_DIR, filename)
                else:
                    print(util.recv(s))
        except:
            print("Server broke connection unexpectedly")
            import traceback; traceback.print_exc()
        finally:
            s.close()
