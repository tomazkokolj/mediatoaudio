# Media to Audio

This script convetrs any media format to ogg (or mp3) audio using ffmpeg. It was written to solve two problems:
* Include files from subdirectories using standard linux utils.
* Convert multiple files at once using multiprocessing.

#### Help
```
Use: find [ARGUMENTS] ... | mediatoaudio.py [ARGUMENTS] ...
 or: ls [ARGUMENTS] ... | mediatoaudio.py [ARGUMENTS] ...
mediatoaudio.py uses standard input to convert files with ffmpeg.

Arguments:
 -c    audio codec            ogg or mp3 (default: ogg)
 -d    delete source files    yes or y (default: no)
 -q    audio quality          0 to 9 - see ffmpeg options (default: 4)

Examples:
 find . -name "*.mp4" | mediatoaudio.py  # default arguments
 ls | mediatoaudio.py -c mp3 -d yes  # convert to mp3, delete the source files
```
