#!/usr/bin/env python

import argparse
import sys
import os
import subprocess
import hashlib
import errno
import requests
import time
import re

parser = argparse.ArgumentParser(prog="vlc-resume",
        description="Automatically resume videos in VLC from where you left off.")
parser.add_argument('file', help='The video file.')
args = parser.parse_args()

# Try to create the timecodes home directory.
TIMECODES_DIR = os.path.join(os.path.expanduser("~"), ".timecodes")
try: os.mkdir(TIMECODES_DIR)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(TIMECODES_DIR): pass
    else: raise

# Calculate file sha
shasum = None
with open(args.file, 'rb') as f:
    h = hashlib.sha1()
    h.update(f.read())
    shasum = h.hexdigest()

timecode_file = os.path.join(TIMECODES_DIR, shasum + ".timecode")

timecode_arg = ""
if os.path.isfile(timecode_file):
	with open(timecode_file, "r") as f:
		timecode_arg = "--start-time=" + f.read()

password = os.urandom(10).encode('hex')

command = "/Applications/VLC.app/Contents/MacOS/VLC --intf macosx --extraintf http --http-password=%s %s \"%s\"" % \
    (password, timecode_arg, args.file)
print "Running \"" + command + "\""
player = subprocess.Popen(command, shell=True)

try:
    seconds = 1
    while True:
        time.sleep(1); seconds += 1

        result = requests.get('http://localhost:8080/requests/status.xml', auth=('', password))
        plid = int(re.search("<currentplid>(-?\d*)</currentplid>", result.text).group(1))
        if plid < 0:
            print "VLC is no longer playing our file. Quitting."
            break

        if seconds % 5 != 0: continue

        timecode = int(re.search("<time>(\d*)</time>", result.text).group(1))
        with open(timecode_file, 'w') as f:
            f.write(str(timecode))
            print "Position %s saved..." % timecode
except KeyboardInterrupt: print "Ctrl-C'd - killing VLC."
except: print "Unexpected error:", sys.exc_info()[0]

player.kill()
