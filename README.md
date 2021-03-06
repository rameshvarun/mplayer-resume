# MPlayer-Resume

This is a simple wrapper for mplayer, which let's you resume watching videos from the position where you quit. It works by parsing the stdout of mplayer, and continuously writing the timecode to a file in `~/.timecodes/`. Files identified by their hash (to handle renaming). Based off of [https://github.com/graysky2/mplayer-resumer](https://github.com/graysky2/mplayer-resumer).

You can symlink `mplayer-resume.py` into `/usr/local/bin/`.
```bash
ln -s /path/to/mplayer-resume.py /usr/local/bin/mplayer-resume
```

Then, videos can be played with:
```bash
mplayer-resume video.mp4
```
