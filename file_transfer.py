import os

import commands
import util

def upload_file(sock, basedir, filename):
     util.send(sock, str(commands.num_chunks(basedir, filename)))
     for data in commands.download(basedir, filename):
          util.send_bytes(sock, data)

def download_file(sock, basedir, filename):
     num_chunks = int(util.recv(sock))
     with open(os.path.join(basedir, filename), 'wb') as f:
          for i in range(num_chunks):
               print(f"Received chunk {i} of {num_chunks}")
               f.write(util.recv_bytes(sock))
