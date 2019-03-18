import argparse
import configparser
import os
import subprocess
import sys
import tempfile

CONFIG_FILE_LOCATIONS = ['~/.config/note/noterc', '~/.noterc']

config = configparser.ConfigParser()
config.read(map(os.path.expanduser, CONFIG_FILE_LOCATIONS))

editor = config.get('DEFAULT', 'editor', fallback='vim')
folder = config.get('DEFAULT', 'folder', fallback='~/notes/')
filetype = config.get('DEFAULT', 'filetype', fallback='.md')

# editor = os.environ.get('EDITOR', 'vim')
# folder = os.path.expanduser(os.environ.get('NOTEDIR', '~/notes/'))
# extension = os.environ.get('NOTEEXT', '.md')


def file_path(file):
    """returns the full path for the file in the notes folder with the filetype specified."""
    return folder + file + filetype


def user_edit(text):
    """lets the user edit text in the command line editor of choice."""
    with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
        tf.write(text)
        tf.flush()
        subprocess.call([editor, tf.name])
        # needs to be read separately via the file name and not the file
        # handle due to an issue with vim on macOS
        # https://stackoverflow.com/questions/46018144/editing-temporary-file-with-vim-in-python-subprocess-not-working-as-expected-on
        with open(tf.name, 'r') as infile:
            user_edits = infile.read()
    return user_edits


def edit_lines_matching(note, pattern):
    with open(file_path(note), 'r') as infile:
        file = infile.read().split('\n')
    matching_lines = [line for line in file if pattern in line]
    text = '\n'.join(matching_lines)
    edited_text = user_edit(text)
    print(edited_text)


def list_():
    for file in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, file)):
            if not filetype or file.endswith(filetype):
                print(file)


def edit(file=None):
    # TODO: make file an optional parameter
    if file:
        subprocess.call([editor, file_path(file)])
    else:
        subprocess.call([editor, folder])


def append(file, entries):
    if not file:
        print('Error: a note must be specified when appending entries')
    else:
        with open(filepath(file), 'a') as note:
            for entry in entries:
                note.write(entry + '\n')


def prepend(file, entries):
    if not file:
        print('Error: a note must be specified when prepending entries')
    else:
        with open(filepath(file), 'r') as note:
            original_contents = note.readlines()
        with open(filepath(file), 'w') as note:
            for entry in entries:
                note.write(entry + '\n')
            for entry in original_contents:
                note.write(entry)


def main():
    parser = argparse.ArgumentParser(description='A simple cli to work with plain text notes.')
    parser.add_argument('note', nargs='*', default='',
                        help='note to edit, leave empty to open notes directory')
    parser.add_argument('-l', '--list', action='store_true', dest='list', default=False,
                        help='list all available notes')
    parser.add_argument('-a', '--append', nargs='+',
                        help='append entries to the given note')
    parser.add_argument('-p', '--prepend', nargs='+',
                        help='prepend entries to the given note')
    # TODO: testing
    args = parser.parse_args()

    if args.list:
        list_()
    elif args.append:
        append(args.note, args.append)
    elif args.prepend:
        prepend(args.note, args.prepend)
    else:
        if 0 == len(args.note):
            edit()
        elif 1 == len(args.note):
            edit(args.note[0])
        elif 2 == len(args.note):
            edit_lines_matching(args.note[0], args.note[1])


if __name__ == '__main__':
    main()
