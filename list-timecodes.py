#!/usr/bin/env python

import argparse
import os
import errno
import hashlib
import subprocess
from ffprobe import FFProbe
from colorama import init, Fore, Style
init()

from lib import timecodedb
from lib.shacache import get_file_sha

VIDEO_EXTENSIONS = set([".mp4"])

parser = argparse.ArgumentParser(prog="list-timecodes",
        description="Show timecodes and completion for videos.")
parser.add_argument('files', metavar='N', nargs='*',
            help='The video files or directories.', default=['.'])
args = parser.parse_args()

def print_completion(filepath):
    # Calculate file sha
    shasum = get_file_sha(filepath)

    timecode = timecodedb.read(shasum)

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
