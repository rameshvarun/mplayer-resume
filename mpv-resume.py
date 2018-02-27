#!/usr/bin/env python

import argparse
import sys
import os
import subprocess
import re
import time
import hashlib
import errno
import json

parser = argparse.ArgumentParser(prog="mpv-resume",
        description="Automatically resume videos from where you left off.")
parser.add_argument('file', help='The video file.')
args = parser.parse_args()

import timecodedb

from shacache import get_file_sha
shasum = get_file_sha(args.file)

timecode_arg = "-ss " + str(timecodedb.read(shasum))

player = subprocess.Popen("mpv " + timecode_arg + " " + args.file + " --input-ipc-server=/tmp/mpv-resume-socket", shell=True)

try:
    last_timecode = None
    while True:
        time.sleep(4)
        res = subprocess.check_output('''echo '{ "command": ["get_property", "playback-time"] }' | socat - /tmp/mpv-resume-socket''', shell=True)

        timecode = json.loads(res)['data']
        if timecode != last_timecode:
            timecodedb.write(shasum, timecode)
            print "Position %s saved..." % timecode
            last_timecode = timecode
except KeyboardInterrupt: print "Ctrl-C'd - killing VLC."
except: print "Unexpected error:", sys.exc_info()[0]

player.kill()
