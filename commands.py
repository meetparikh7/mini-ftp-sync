import os
import time
import util

# Support ls, ls -l
def ls(base_dir, long=False):
    toret = ""
    files = os.listdir(base_dir)
    if not long:
        toret += "\n".join(files)
    else:
        for f in files:
            details = util.file_details(os.path.join(base_dir, f))
            details["mtime"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.gmtime(details["mtime"])
            )
            toret += f"{f}\t{details['size']}\t{details['mtime']}\t{details['type']}\n"
    return toret.strip()


def hashfile(base_dir, filename):
    toret = ""
    filename = os.path.join(base_dir, filename)
    print(util.hashfile(filename))
    return util.hashfile(filename)
