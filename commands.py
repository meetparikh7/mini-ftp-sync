import json
import math
import os
import time
import util

# Support ls, ls -l
def ls(base_dir, long=False):
    toret = []
    files = os.listdir(base_dir)
    if not long:
        toret = files
    else:
        for f in files:
            details = util.file_details(os.path.join(base_dir, f))
            # details["mtime"] = time.strftime(
            #     "%Y-%m-%d %H:%M:%S", time.gmtime(details["mtime"])
            # )
            details["name"] = f
            toret.append(details)
    return json.dumps(toret)


def hashfile(base_dir, filename):
    toret = ""
    filename = os.path.join(base_dir, filename)
    print(util.hashfile(filename))
    return util.hashfile(filename)


def num_chunks(base_dir, filename):
    filename = os.path.join(base_dir, filename)
    return math.ceil(util.file_details(filename)["size"] / 1024)


def download(base_dir, filename):
    filename = os.path.join(base_dir, filename)
    with open(filename, "rb") as f:
        data = f.read(1024)
        while data:
            yield data
            data = f.read(1024)
