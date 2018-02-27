#!/usr/bin/env python

import argparse
import os
import errno
import hashlib
import subprocess
from ffprobe import FFProbe
from colorama import init, Fore, Style
init()

# Try to create the timecodes home directory.
TIMECODES_DIR = os.path.join(os.path.expanduser("~"), ".timecodes")
try: os.mkdir(TIMECODES_DIR)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(TIMECODES_DIR): pass
    else: raise

VIDEO_EXTENSIONS = set([".mp4"])

parser = argparse.ArgumentParser(prog="list-timecodes",
        description="Show timecodes and completion for videos.")
parser.add_argument('files', metavar='N', nargs='*',
            help='The video files or directories.', default=['.'])
args = parser.parse_args()

from shacache import get_file_sha

def print_completion(filepath):
    # Calculate file sha
    shasum = get_file_sha(filepath)

    timecode = 0.0
    timecode_file = os.path.join(TIMECODES_DIR, shasum + ".timecode")
    if os.path.isfile(timecode_file):
        with open(timecode_file, "r") as f:
            timecode = float(f.read())

    duration = float(FFProbe(filepath).video[0].duration)
    completion = timecode / duration

    if timecode > duration - 10:
        completion = 1

    out_line = "{}\t{:0.1f}%\t{:0.2f}/{:0.2f}".format(filepath, completion*100, timecode, duration)
    if completion == 1:
        print(Fore.GREEN + out_line + Style.RESET_ALL)
    else:
        print(Fore.RED + out_line + Style.RESET_ALL)

for file in args.files:
    if os.path.isfile(file):
        print_completion(file)
    elif os.path.isdir(file):
        for root, dirs, files in os.walk(file):
            for filename in files:
                if os.path.splitext(filename)[1] not in VIDEO_EXTENSIONS:
                    continue
                filepath = os.path.join(root, filename)
                print_completion(filepath)
