import hashlib
import mimetypes
import os
import struct

HEADER_SIZE = struct.calcsize('l')

def send_bytes(sock, s):
     s_len = len(s)
     network_s_len = struct.calcsize(f"{s_len}s")
     packed = struct.pack(f'l{s_len}s', network_s_len, s)
     return sock.sendall(packed)

def recv_bytes(sock):
     data = sock.recv(HEADER_SIZE)
     s_len, = struct.unpack("l", data)
     data = sock.recv(s_len)
     s, = struct.unpack(f"{s_len}s", data)
     return s

def send(sock, s):
     s = s.encode("utf-8")
     return send_bytes(sock, s)

def recv(sock):
     s = recv_bytes(sock)
     return s.decode("utf-8")


def file_details(filepath):
     return {
          "mtime": os.path.getmtime(filepath),
          "size": os.path.getsize(filepath),
          "type": mimetypes.guess_type(filepath)[0] or "unknown"
     }


def hashfile(filepath):
     with open(filepath, "rb") as f:
          file_hash = hashlib.md5()
          chunk = f.read(8192)
          while chunk:
               file_hash.update(chunk)
               chunk = f.read(8192)
          return file_hash.hexdigest()

def split_command(command):
     command = command.strip().split(" ")
     command = list(filter(lambda v: v, command))
     return command


def format_table(columns, data):
     s = ""
     for c in columns:
          s += c + "\t\t"
     s += "\n" + ("-" * 2 * len(s)) + "\n"
     for row in data:
          for c in columns:
               s += str(row[c]) + "\t"
          s += "\n"
     return s
