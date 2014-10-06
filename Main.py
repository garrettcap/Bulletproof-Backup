__author__ = "Garrett Capaccioli"
import os, os.path, sys, shutil, hashlib, getopt

#Define Archive Location
#OR BETTER, a version that looks in a specific location for the current user.
#The tilde ( ~ ) at the start of the following string is used to indicate
#the user's home directory, so this line for /myArchive/ directory on the
#user's Desktop:
myArchive = os.path.expanduser("~/Desktop/myArchive")

def init():
    print "Current archive path:" + myArchive
    if os.path.exists(myArchive) and os.path.isdir(myArchive):
        print "Archive Directory already exists"
    else:
        print "Archive Directory not yet created"
    if os.path.exists(myArchive) and os.path.exists(myArchive + "/objects"):
        print "Directory not created"
    else:
        user_input = raw_input("Would you like to create the directory:")
        if user_input == "yes" or user_input == "y":
            os.mkdir(myArchive, 0777)
            open(myArchive + "/index", 'a')
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

def store_backup(user_input_directory):

    try:
        shutil.copytree(user_input_directory, directory_name, symlinks=False, ignore=None)
    except shutil.Error:
        print shutil.Error()



def main(argv):
    try:
        opts, args = getopt.getopt(argv, "his:", ["init", "store="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfil>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>!!'
            sys.exit()
        elif opt in ("-i", "--init"):
            print "woot1"
            init()
        elif opt in ("-s", "--store"):
            print "moop"
            storedirectory = arg
            store_backup(storedirectory)
        else:
            print 'ERROR'

if __name__ == "__main__":
    main(sys.argv[1:])





"""CreateFileHash (file): create a signature for the specified file
Returns a tuple containing three values:
(the pathname of the file, its last modification time, SHA1 hash)
"""

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

