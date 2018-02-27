import shelve
import os
import hashlib

code_dir = os.path.dirname(os.path.realpath(__file__))
shelf = shelve.open(os.path.join(code_dir, '.shacache'))

def get_file_sha(filepath):
    realpath = os.path.abspath(os.path.realpath(filepath))
    if realpath not in shelf:
        with open(filepath, 'rb') as f:
            h = hashlib.sha1()
            h.update(f.read())
            shelf[realpath] = h.hexdigest()
    return shelf[realpath]
