#!/usr/bin/env python

"""This script convetrs from any media format to audio (ogg or mp3) using
ffmpeg. It was written to solve two problems:
1. Use linux utils like find to include files from subdirectories.
2. Use multiprocessing to convert multipe files at once.
"""

import sys
import subprocess
from multiprocessing import Pool

def main():
    """Execute only if run as a script."""

    if '-h' in sys.argv or '--help' in sys.argv:
        print_help()

    arguments = map_arguments()
    sys.stdout.write('Converting from standard input (use -h for help) ...\n')

    pool = Pool()
    src_files = pool.map(convert_files, enumerate(sys.stdin.readlines()))
    pool.close()
    pool.join()

    if arguments['-d'].lower() == 'yes' or arguments['-d'].lower() == 'y':
        sys.stdout.write('Deleting ...\n')
        delete_files(src_files)

def map_arguments():
    """Maps the sys.argv to a dictionary and returns it. Omits sys.argv[0].

    You may also look at OptionParser.
    """
    arguments = {
        '-c': 'ogg',
        '-d': 'no',
        '-q': '4'
    }
    args = sys.argv[:]
    args.pop(0)
    while len(args) != 0:
        if '-c' in args[0] or '-d' in args[0] or '-q' in args[0]:
            try:
                arguments[args[0]] = args[1]
            except IndexError:
                raise ValueError('Wrong arguments passed')
            args.pop(0)
            args.pop(0)
        else:
            raise ValueError('Wrong arguments passed')
    return arguments

def audio_codec():
    """Returns the right file extension, codec and audio quality based on the
    command line arguments.
    """
    arguments = map_arguments()
    if arguments['-c'] == 'ogg':
        return '.ogg', 'libvorbis', arguments['-q']
    elif arguments['-c'] == 'mp3':
        return '.mp3', 'libmp3lame', arguments['-q']
    else:
        raise ValueError('Wrong file type')

def convert_files(enumerated_src_file):
    """Uses multiprocessin to convert multiple files at once.

    Returns the converted source file (used in delete_files function).
    """
    i, src_file = enumerated_src_file
    src_file = src_file.strip()
    file_extension, acodec, quality = audio_codec()

    dst_file = '.'.join(src_file.split('.')[:-1]) + file_extension
    sys.stdout.write(str(i + 1) + ': ' + src_file + ' -> ' + dst_file + '\n')
    subprocess.call(['ffmpeg', '-i', src_file, '-vn', '-acodec',
                     acodec, '-aq', quality, dst_file, '-loglevel', 'quiet'])
    return src_file

def delete_files(src_files):
    """Deletes the source files when -d yes is used as an argument to the
    console.
    """
    for i, src_file in enumerate(src_files):
        sys.stdout.write(str(i + 1) + ': ' + src_file + '\n')
        subprocess.call(['rm', src_file])

def print_help():
    """Prints help when the -h or --help argument is used in the command line.
    """
    sys.stdout.write(
        'Use: find [ARGUMENTS] ... | mediatoaudio.py [ARGUMENTS] ...\n'
        ' or: ls [ARGUMENTS] ... | mediatoaudio.py [ARGUMENTS] ...\n'
        'mediatoaudio.py uses standard input to convert files with ffmpeg.\n'
        '\nArguments:\n' \
        '  -c\taudio codec\t\togg or mp3 (default: ogg)\n'
        '  -d\tdelete source files\tyes or y (default: no)\n'
        '  -q\taudio quality\t\t0 to 9 - see ffmpeg options (default: 4)\n\n'
        'Examples:\n'
        '  find . -name "*.mp4" | mediatoaudio.py  # default arguments\n'
        '  ls | mediatoaudio.py -c mp3 -d yes  # convert to mp3, delete the'
        ' source files\n'
    )
    sys.exit()

if __name__ == '__main__':
    main()
