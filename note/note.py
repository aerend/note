import argparse
import os
import subprocess
import sys

editor = os.environ.get('EDITOR', 'vim')
folder = os.path.expanduser(os.environ.get('NOTEDIR', '~/Dropbox/Apps/Editorial/'))
extension = os.environ.get('NOTEEXT', '.md')


def list():
    for file in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, file)):
            if not extension or file.endswith(extension):
                print(file)


def edit(file):
    if file:
        subprocess.call([editor, folder + file + extension])
    else:
        subprocess.call([editor, folder])


def append(file, entries):
    if not file:
        print('Error: a note must be specified when appending entries')
    else:
        with open(folder + file + extension, 'a') as note:
            for entry in entries:
                note.write(entry + '\n')


def main():
    parser = argparse.ArgumentParser(description='A simple cli to work with plain text notes.')
    parser.add_argument('note', nargs='?', default='',
                        help='note to edit, leave empty to open notes directory')
    parser.add_argument('-l', '--list', action='store_true', dest='list', default=False,
                        help='list all available notes')
    parser.add_argument('-a', '--append', nargs='+',
                        help='append entries to the given note')
    args = parser.parse_args()

    if args.list:
        list()
    elif args.append:
        append(args.note, args.append)
    else:
        edit(args.note)

if __name__ == '__main__':
    main()