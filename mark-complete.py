#!/usr/bin/env python

import argparse
import os
import errno
import hashlib
import subprocess
from ffprobe import FFProbe

parser = argparse.ArgumentParser(prog="mark-complete",
        description="Mark a video as completely watched.")
parser.add_argument('file', help='The video file.')
args = parser.parse_args()

# Try to create the timecodes home directory.
TIMECODES_DIR = os.path.join(os.path.expanduser("~"), ".timecodes")
try: os.mkdir(TIMECODES_DIR)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(TIMECODES_DIR): pass
    else: raise

# Calculate file sha
with open(args.file, 'rb') as f:
    h = hashlib.sha1()
    h.update(f.read())
    shasum = h.hexdigest()

duration = float(FFProbe(args.file).video[0].duration)

timecode_file = os.path.join(TIMECODES_DIR, shasum + ".timecode")
with open(timecode_file, 'w') as f:
    f.write(str(duration))
