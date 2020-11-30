import struct


HEADER_SIZE = struct.calcsize('l')

def send(sock, s):
     s = s.encode("utf-8")
     s_len = len(s)
     network_s_len = struct.calcsize(f"{s_len}s")
     packed = struct.pack(f'l{s_len}s', network_s_len, s)
     sock.sendall(packed)

def recv(sock):
     data = sock.recv(HEADER_SIZE)
     s_len, = struct.unpack("l", data)
     data = sock.recv(s_len)
     s, = struct.unpack(f"{s_len}s", data)
     return s.decode("utf-8")
