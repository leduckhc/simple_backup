#
# author: Milan Le @ Quantasoft, 2019
#

import argparse
import zipfile
import os
import sys
from datetime import datetime

INCLUDE_EXTENSIONS = [
    '.py',
    '.c', '.cpp', '.h', '.hpp',
    '.cs',
    '.html', '.js', '.css', '.php'
    '.dart',
    '.sh', '.zsh', '.fish']

EXCLUDE_DIRECTORIES = ['.git', 'build', 'dist']


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True,
        help='Source folder to be added')
    parser.add_argument('-t', '--target', required=True,
        help='Target backup zip file')
    parser.add_argument('-n', '--dry-run',
        help='Before running just print out')
    if len(sys.argv) < 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()


def has_extension(filename):
    for ext in INCLUDE_EXTENSIONS:
        if filename.endswith(ext):
            return True
    return False


def retrieve_filepaths(dirname):
    filepaths = []
    for root, directories, files in os.walk(dirname):
        for filename in files:
            if has_extension(filename):
                filepath = os.path.join(root, filename)
                filepaths.append(filepath)
    return filepaths


def create_zip(source, target, source_root=None):
    timestamp = datetime.now().strftime('_%Y-%m-%d_%H-%M')
    target += timestamp + '.zip'
    print('Source directory       -> Target zipfile')
    print(source, '->', target)
    filepaths = retrieve_filepaths(source)
    with zipfile.ZipFile(target, 'w') as myzip:
        for filename in filepaths:
            print(filename)
            if source_root:
                arcname = os.path.relpath(filename, source_root)
                myzip.write(filename, arcname)
            else:
                myzip.write(filename)


def backup(source_root, target_root):
    for source in os.listdir(source_root):
        target = os.path.join(target_root, source)
        source = os.path.join(source_root, source)
        if os.path.isdir(source):
            create_zip(source, target, source_root)


if __name__ == '__main__':
    arg = parse_arguments()
    backup(arg.source, arg.target)

    # backup(os.path.expanduser(arg.source), os.path.expanduser(arg.target))
