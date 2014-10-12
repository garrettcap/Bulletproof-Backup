import os
import os.path as path
import sys
import shutil
import hashlib
import getopt
import pprint

from cPickle import dump, load

myArchive = os.path.expanduser("~/Desktop/myBackup")
myObjects = myArchive + "/objects"
myIndex = myArchive + "/index"


def init():  # creates archive folder and index files
    if path.exists(myArchive) and path.isdir(myArchive):
        print("Archive Directory already exists.")
    else:
        user_input = raw_input("Would you like to create an archive? ")
        if user_input.lower() == "yes" or user_input.lower() == "y":
            create_archive()
        else:
            print("Archive not created.")


def create_archive():
    index_init = {}  # initializes blank index dictionary

    os.mkdir(myArchive, 0777)  # creates new archive directory
    os.mkdir(myArchive + "/objects", 0777)  # creates new object subdirectory
    dump(index_init, open(myArchive + "/index", 'wb'))  # creates empty? index file
    print("Archive successfully created.")


def create_file_signature(filename):
    temp_file = None
    signature = None
    try:
        temp_file = open(filename, "rb")
        hash = hashlib.sha1()
        s = temp_file.read(16384)
        while s:
            hash.update(s)
            s = temp_file.read(16384)
        hash_value = hash.hexdigest()
        signature = hash_value
    except IOError:
        signature = None
    except OSError:
        signature = None
    finally:
        if temp_file:
            temp_file.close()
            return signature


def index_check_and_add(hash_name, file_name, index_file):
    index_file[hash_name] = file_name

def index_rename_to_original(restore_fullpath, index_file, destination_directory, file1):
    print index_file
    print file1
    print destination_directory + "123"
    index_file_name = index_file.get(file1)
    print index_file_name
    new_file_fullpath = os.path.join(destination_directory, index_file_name)
    print new_file_fullpath
    os.rename(restore_fullpath, new_file_fullpath)


def store_backup(user_input_directory):
    index_file = load((open(myIndex, 'rb')))  # loads index file
    files_not_added_count = 0  # file not added counter duh!
    new_files_added = []  # really....
    print("Yay!")  # logger

    for root, dirs, files in os.walk(user_input_directory):
        for file_name in files:
                original_path = path.join(user_input_directory, file_name)
                hash_name = create_file_signature(original_path)  # creates a hash for the file
                if hash_name in index_file.values():  # checks file against index
                    files_not_added_count += 1
                else:
                    backup_path = path.join(myObjects, file_name)
                    shutil.copy2(original_path, myObjects)  # copies files...
                    os.rename(backup_path, myObjects + "/" + hash_name)  # renames files to hash equil
                    index_check_and_add(hash_name, file_name, index_file)  # adds hash/filename to index
                    new_files_added.append(file_name)

    dump(index_file, open(myIndex, "wb"))  # dumps info into index file
    print("Files not added: " + str(files_not_added_count))
    print("New files added: ")
    pprint.pprint(new_files_added)

#store_backup("/home/gar/Desktop/moop") # use for testing purposes


#recovers a single file from archive
def get_file():
    return 0


#recovers all files from archive
def restore_files(destination_directory):
    index_file = load((open(myIndex, 'rb')))
    for files in index_file.iterkeys():
        original_fullpath = os.path.join(myObjects, files)
        shutil.copy2(original_fullpath, destination_directory)
        restore_fullpath = os.path.join(destination_directory, files)
        index_rename_to_original(restore_fullpath, index_file, destination_directory, files)


def list_all_items():
    index_file = load((open(myIndex, 'rb')))
    for files in index_file.itervalues():
        path.join(files)
        pprint.pprint(files)

def main(argv):  # command line interpreter
    try:
        opts, args = getopt.getopt(argv, "his:lr:", ["init", "store=", "list"])
    except getopt.GetoptError:
        print("Must be in the following format")
        print("Options are [-i or --init to initialize and create backup folder]")
        print("            [-s or --store <directory_path> to create a backup of directory in backup folder]")
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print("Options are [-i or --init to initialize and create backup folder]")
            print("            [-s or --store <directory_path> to create a backup of directory in backup folder")
            sys.exit()
        elif opt in ("-i", "--init"):
            init()
        elif opt in ("-l", "--list"):
            list_all_items()
        elif opt in ("-r", "--restore"):
            restore_files(arg)
        elif opt in ("-s", "--store"):
            print("Store")
            stored_directory = arg
            store_backup(stored_directory)
        else:
            print('ERROR')

if __name__ == "__main__":
    main(sys.argv[1:])