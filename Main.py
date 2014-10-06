__author__ = "Garrett Capaccioli"
import os, os.path
#Define Archive Location
#OR BETTER, a version that looks in a specific location for the current user.
#The tilde ( ~ ) at the start of the following string is used to indicate
#the user's home directory, so this line for /myArchive/ directory on the
#user's Desktop:
myArchive = os.path.expanduser("~/Desktop/myArchive")
print "Current archive path:" + myArchive
if os.path.exists(myArchive) and os.path.isdir(myArchive):
    print "Archive Directory already exists"
else:
    print "Archive Directory not yet created"

def make_directory():

    if os.path.exists(myArchive) and os.path.exists(myArchive + "/objects"):
        print "Directory not created"

    else:
        user_input = raw_input("Would you like to create the directory:")
        if user_input == "yes" or user_input == "y":
            os.mkdir(myArchive, 0777)
            os.mkdir(myArchive + "/objects", 0777)
            open(myArchive + "/index", 'a')
            print "Directory successfully created"

make_directory()