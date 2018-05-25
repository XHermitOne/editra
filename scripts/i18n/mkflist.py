#!/usr/bin/env python
import os

def findFiles(path, flist):
    """Find all files under the given path"""
    if os.path.isdir(path):
        fnames = [ os.path.join(path, p)
                   for p in os.listdir(path)
                   if not p.startswith('.') and p != 'extern']
        for fname in fnames:
            findFiles(fname, flist)
    elif path.endswith(".py"):
        flist.append(path)

if __name__ == '__main__':
    # Generate the file list
    path = "../../src/"
    cbrowser = "../../plugins/codebrowser/codebrowser/"
    fbrowser = "../../plugins/filebrowser/filebrowser/"
    launch = "../../plugins/Launch/Launch/"
    pshell = "../../plugins/PyShell/PyShell/"

    flist = list()
    for p in (path, cbrowser, fbrowser, launch, pshell):
        findFiles(p, flist)

    f = open('app.fil', 'wb')
    f.write("\n".join(flist))
    f.close()
