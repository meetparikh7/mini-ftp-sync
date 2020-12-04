
#!/usr/bin/env python3

import json
import os
import time

import commands
import file_transfer
import util


class Syncer:
    def __init__(self, basedir):
        self.last_synced = {}
        self.basedir = basedir

    def sync(self, sock):
        util.send(sock, "ls -l")
        remote_data = util.recv(sock)
        remote_data = json.loads(remote_data)
        client_data = commands.ls(self.basedir, long=True)
        client_data = json.loads(client_data)
        client_filelist = list(map(lambda f: f["name"], client_data))
        remote_filelist = list(map(lambda f: f["name"], remote_data))
        cue_download = []
        cue_upload = []
        for file in remote_data:
            if file["name"] not in client_filelist:
                cue_download.append(file["name"])
        for file in client_data:
            if file["name"] not in remote_filelist:
                cue_upload.append(file["name"])
        for file in remote_data:
            if not file["name"] in client_filelist:
                continue
            # do not request hash if file was modified before previous sync
            if file['name'] in self.last_synced and file["mtime"] < self.last_synced[file['name']]:
                continue
            util.send(sock, f"hash {file['name']}")
            hsh = util.recv(sock)
            local_hsh = util.hashfile(os.path.join(self.basedir, file['name']))
            if hsh != local_hsh: # IMPORTANT LOGIC
                local_file = [f for f in client_data if f.get('name')== f['name']][0]
                if file['mtime'] > self.last_synced[file['name']]:
                    # server is always right
                    cue_download.append(file['name'])
                else:
                    cue_upload.append(file['name'])
        for filename in cue_upload:
            util.send(sock, f"upload {filename}")
            file_transfer.upload_file(sock, self.basedir, filename)
            self.last_synced[filename] = time.time()
        for filename in cue_download:
            util.send(sock, f"download {filename}")
            file_transfer.download_file(sock, self.basedir, filename)
            self.last_synced[filename] = time.time()
