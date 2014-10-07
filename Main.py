__author__ = "Garrett Capaccioli"
import os, os.path, sys, shutil, hashlib, getopt, cPickle as pickle

#Define Archive Location
#OR BETTER, a version that looks in a specific location for the current user.
#The tilde ( ~ ) at the start of the following string is used to indicate
#the user's home directory, so this line for /myArchive/ directory on the
#user's Desktop:
myArchive = os.path.expanduser("~/Desktop/myArchive")
myObjects = myArchive + "/objects"
myIndex = myArchive + "/index"

def init():  # creates archive folder and index files
    index_init = {}  # initalizes blank index dictionary
    print "Current archive path:" + myArchive
    if os.path.exists(myArchive) and os.path.isdir(myArchive):
        print "Archive Directory already exists"
    if os.path.exists(myArchive) and os.path.exists(myArchive + "/objects"):
        print "Directory not created"
    else:
        user_input = raw_input("Would you like to create the directory (yes or y): ")
        if user_input == "yes" or user_input == "y":
            os.mkdir(myArchive, 0777)  # makes the main directory
            os.mkdir(myArchive + "/objects", 0777)  # makes the object directory
            pickle.dump(index_init, open(myArchive + "/index", 'wb'))  # creates proper index file
            print "Directory successfully created"

def create_file_signature(filename):
    f = None
    signature = None
    try:
        f = open(filename, "rb")
        hash = hashlib.sha1()
        s = f.read(16384)
        while s:
            hash.update(s)
            s = f.read(16384)
        hashvalue = hash.hexdigest()
        signature = hashvalue
    except IOError:
        signature = None
    except OSError:
        signature = None
    finally:
        if f:
            f.close()
            return signature

def index_check_and_add(hash_name, file_name, index_file):
    index_file[file_name] = hash_name

def store_backup(user_input_directory):
    index_file = pickle.load((open(myIndex, 'rb')))  # loads index file
    files_not_added_count = 0  # file not added counter duh!
    new_files_added = []  # really....
    print "Yay!"  # logger and shit
    for root, dirs, files in os.walk(user_input_directory):
        print "Yay2!"  # logger goes here
        for file_name in files:
                print "yay3!"  # logger would go here
                original_path = os.path.join(user_input_directory, file_name)
                hash_name = create_file_signature(original_path)  # creates a hash for the file
                if hash_name in index_file.values():  # checks file against index
                    files_not_added_count += 1
                else:
                    backup_path = os.path.join(myObjects, file_name)
                    shutil.copy2(original_path, myObjects)  # copies files...
                    os.rename(backup_path, myObjects + "/" + hash_name)  # renames files to hash equil
                    index_check_and_add(hash_name, file_name, index_file)  # adds hash/filename to index
                    new_files_added.append(file_name)

    pickle.dump(index_file, open(myIndex, "wb"))  # dumps info into index file
    print "Files not added: " + str(files_not_added_count)
    print "New files added: " + str(new_files_added)

#store_backup("/home/gar/Desktop/moop") # use for testing purposes

def main(argv):  # command line interpreter (dont touch this bitch)
    try:
        opts, args = getopt.getopt(argv, "his:", ["init", "store="])
    except getopt.GetoptError:
        print 'Must be in the following format'
        print "Options are [-i or --init to initalize and create backup folder]"
        print "            [-s or --store <directory_path> to create a backup of directory in backup folder]"
        sys.exit()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print "Options are [-i or --init to initalize and create backup folder]"
            print "            [-s or --store <directory_path> to create a backup of directory in backup folder"
            sys.exit()
        elif opt in ("-i", "--init"):
            init()
        elif opt in ("-s", "--store"):
            storedirectory = arg
            store_backup(storedirectory)
        else:
            print 'ERROR'
if __name__ == "__main__":
    main(sys.argv[1:])

