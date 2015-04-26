# MPlayer-Resume

This is a simple wrapper for mplayer, which let's you resume watching videos from the position where you quit. It works by parsing the stdout of mplayer, and continuously writing the timecode to a file in the same directory. Based off of [https://github.com/graysky2/mplayer-resumer](https://github.com/graysky2/mplayer-resumer).

You can symlink `mplayer-resume.py` into `/usr/local/bin/mplayer-resume`. Then, videos can be played with:
```
mplayer-resume video.mp4
```
