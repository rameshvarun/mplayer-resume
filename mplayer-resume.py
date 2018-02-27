#!/usr/bin/env python

import argparse
import sys
import os
import subprocess
import re
import time
import hashlib
import errno

parser = argparse.ArgumentParser(prog="mplayer-resume",
        description="Automatically resume videos from where you left off.")
parser.add_argument('file', help='The video file.')
args = parser.parse_args()

# Try to create the timecodes home directory.
TIMECODES_DIR = os.path.join(os.path.expanduser("~"), ".timecodes")
try:
    os.mkdir(TIMECODES_DIR)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(TIMECODES_DIR):
        pass
    else:
        raise

from shacache import get_file_sha
shasum = get_file_sha(args.file)

timecode_file = os.path.join(TIMECODES_DIR, shasum + ".timecode")

timecode_arg = ""
if os.path.isfile(timecode_file):
	with open(timecode_file, "r") as f:
		timecode_arg = "-ss " + f.read()

player = subprocess.Popen("mplayer " + timecode_arg + " " + args.file, stdout=subprocess.PIPE , shell=True)


code = "\x1b[J\r"
regex = re.compile("\s*A:\s*([-+]?\d*\.\d+|\d+)\s*V:\s*([-+]?\d*\.\d+|\d+)")

last_save = time.time()
def process_line(line):
	global last_save

	if time.time() > last_save + 5:
		match = regex.search(line)
		if match:
			timecode = match.group(2)
			with open(timecode_file, 'w') as f:
				f.write(timecode)
				print "Position saved..."
				last_save = time.time()

reading_lines = False
current_line = ""
while True:
	buffer = player.stdout.read(100)
	if buffer == "": break
	while code in buffer:
		pos = buffer.find(code)

		if not reading_lines:
			reading_lines = True
		else:
			current_line += buffer[:(pos - 1)]
			process_line(current_line)
			current_line = ""
		buffer = buffer[(pos + len(code)):]
	current_line += buffer
