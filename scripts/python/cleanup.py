import os
import time
import shutil
import logging

__author__ = 'cjengdahl'


"""
This script checks the modified time of each file
in the DELETE_PATH.  If the file is older than the DELETE_AFTER
parameter in hours, the file/directory will be deleted.  In addition,
a DELETE_ALWAYS tuple can indicate a file type should be
deleted regardless of how old it its.  Similarly, a DELETE_NEVER
tuple can mark a file type that should never be deleted

"""

DELETE_ALWAYS = ('.tor', '.torrent')
DELETE_NEVER = ()
DELETE_AFTER = 24
DELETE_PATH = '/Users/cengdahl/Downloads/'

logging.basicConfig(format='%(asctime)s %(message)s', filename='/Users/cengdahl/Library/Logs/cleanup.log', level=logging.INFO)

def rotten_file(file):
    """
    determines if a file is too old to keep around
    :param file (string): file to evaluate
    :return (bool): True if file is old enough to delete, False otherwise
    """
    name, ext = os.path.splitext(file)

    return (time.time() - os.path.getmtime(DELETE_PATH +
            file) > (DELETE_AFTER*3600))


def precious_file(file):
    """
    determines if a file should never be deleted
    :param file (string): file to evaluate
    :return (bool): True if file is precious, False otherwise
    """
    name, ext = os.path.splitext(file)

    return ext in DELETE_NEVER


def worthless_file(file):
    """
    determines if a file should alway be deleted
    :param file (string): file to evaluate
    :return (bool): True if file is precious, False otherwise
    """
    name, ext = os.path.splitext(file)

    return ext in DELETE_ALWAYS

# files to evaluate
contents = []

# omit hidden files
for file in os.listdir(DELETE_PATH):
    if not file.startswith('.'):
        contents.append(file)

# begin log
logging.info('Cleaning Directory')

# evaluate all files
for file in contents:
    fullpath = DELETE_PATH + file
    if (not rotten_file(file) and not worthless_file(file)):
        continue
    elif not precious_file(file):
        if os.path.isfile(fullpath):
            os.remove(fullpath)
            logging.info('deleting file %s', file)
        elif os.path.isdir(fullpath):
            shutil.rmtree(fullpath)
            logging.info('deleting directory %s', file)
