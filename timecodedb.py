import os
import errno

TIMECODES_DIR = os.path.join(os.path.expanduser("~"), ".timecodes")

# Try to create the timecodes home directory.
try:
    os.mkdir(TIMECODES_DIR)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(TIMECODES_DIR):
        pass
    else:
        raise

def read(shasum):
    timecode_file = os.path.join(TIMECODES_DIR, shasum + ".timecode")
    if os.path.isfile(timecode_file):
    	with open(timecode_file, "r") as f:
    		return float(f.read())
    return 0.0

def write(shasum, timecode):
    timecode_file = os.path.join(TIMECODES_DIR, shasum + ".timecode")
    with open(timecode_file, 'w') as f:
        f.write(str(timecode))
