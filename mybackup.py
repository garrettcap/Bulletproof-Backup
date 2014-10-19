#!/usr/bin/python
import os
import os.path as path
import sys
import shutil
import getopt
import pprint
import argparse
from cPickle import dump, load
from gooey import Gooey

import initialization
from logs import logger
from store import Store


myArchive = os.path.expanduser("~/Desktop/myBackup")
myObjects = myArchive + "/objects"
myIndex = myArchive + "/index"
store = Store(myIndex, myObjects, logger)


def make_directories(paths):
    if not os.path.exists(paths):
        os.makedirs(paths)
        logger.info("Directory creation successful")


def update_index():
    index_file = load((open(myIndex, 'rb')))  # loads index file
    modified_dict = index_file
    files_list = []
    for root, dirs, files in os.walk(myObjects):  # walks through backup directory
        for item in files:
            files_list.append(item)  # returns a list of files in directory, (calling the "files" list breaks counter)
    for keys in index_file.keys():  # iterates through list of filename in index
        if keys not in files_list:  # checks to see if files arent in backup directory
            del modified_dict[keys]  # deletes if not in backup directory
    dump(modified_dict, open(myIndex, "wb"))  # dumps info into index file


#recovers a single file from archive
def get_file(desired_file):
    update_index()  # updates index
    index_file = load((open(myIndex, 'rb')))
    for hash_file, file_names in index_file.iteritems():
        top_files, short_value = os.path.split(file_names)
        if short_value == desired_file:
            if top_files == ".":
                begin_fullpath = os.path.join(myObjects, hash_file)
            else:
                begin_fullpath = os.path.join(myObjects, (os.path.join(top_files, hash_file)))
            final_fullpath = os.path.join(os.getcwd(), short_value)
            shutil.copy2(begin_fullpath, final_fullpath)
            print "File successfully extracted to " + final_fullpath
            sys.exit()
    logger.error("File not found in backup")
    print "Try putting filename in quotations and adding extension. Ex. 'My file.txt'"


#recovers all files from archive
def restore_files(destination_directory):
    update_index()
    index_file = load((open(myIndex, 'rb')))  # loads index file
    make_directories(destination_directory)  # makes directories
    os.chdir(destination_directory)
    for root, dirs, files in os.walk(myObjects):  # walks through backup directory
        for file_name in files:
            file_fullpath = os.path.join(root, file_name)  # creates the fullpath to backup folder files
            new_filepath = index_file.get(file_name)  # retrives the file values from dict
            head, tail = os.path.split(new_filepath)  # splits filename into top directories
            make_directories(head)  # makes required directories if non-existent
            shutil.copy2(file_fullpath, new_filepath)  # copies files to restore and renames
    logger.info("Restore successful")
    print "Restore successful"


def list_all_items():  # lists all files in backup folder
    update_index()
    index_file = load((open(myIndex, 'rb')))
    for files in index_file.itervalues():
        path.join(files)
        pprint.pprint(files)  # prints filepath


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "his:lr:g:", ["init", "store=", "list"])
    except getopt.GetoptError:
        logger.error(getopt.GetoptError)
        print("Must be in the following format")
        print("Options are [-i or --init to initialize and create backup folder]")
        print("            [-s or --store <directory_path> to create a backup of directory in backup folder]")
        print("            [-r or --restore <destination_directory> to restore entire backup into destination]")
        print("            [-l or --list to list all files currently in backup folder]")
        print("            [-g or -get <'filename'> restores individual file to current directory]")
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print("Options are [-i or --init to initialize and create backup folder]")
            print("            [-s or --store <directory_path> to create a backup of directory in backup folder]")
            print("            [-r or --restore <destination_directory> to restore entire backup into destination]")
            print("            [-l or --list to list all files currently in backup folder]")
            print("            [-g or -get <'filename'> restores individual file to current directory]")
            sys.exit()
        elif opt in ("-i", "--init"):
            initialization.init(myArchive, logger)
        elif opt in ("-l", "--list"):
            list_all_items()
        elif opt in ("-r", "--restore"):
            restore_files(arg)
        elif opt in ("-s", "--store"):
            print("Store")
            stored_directory = arg
            update_index()
            store.store_backup(stored_directory)
        elif opt in ("-g" or "--get"):
            if not type(arg) is str:
                print("-g or --get <'filename'> (filename must be in quotes)")
                sys.exit()
            get_file(arg)
        else:
            logger.error("Command not found, type -h for help")

if __name__ == "__main__":
    # main()
    main(sys.argv[1:])