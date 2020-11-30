import os

# Support ls, ls -l
def ls(base_dir, long=False):
    toret = ""
    dirs = os.listdir(base_dir)
    toret += "\n".join(dirs)
    return toret
