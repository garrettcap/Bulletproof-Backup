import os
import os.path as path
from cPickle import dump


#init function creates new archive folder
def init(archive_path, logger):  # creates archive folder and index files
    if path.exists(archive_path) and path.isdir(archive_path):
        logger.error('Archive directory already exists')
    else:
        user_input = raw_input("Would you like to create an archive? ")
        if user_input.lower() == "yes" or user_input.lower() == "y":
            create_archive(archive_path, logger)
        else:
            logger.info("Archive not created")
            print("Archive not created")


def create_archive(archive_path, logger):  # creates the backup archive and log file
    index_init = {}  # initializes blank index dictionary

    os.mkdir(archive_path, 0777)  # creates new archive directory
    os.mkdir(archive_path + "/objects", 0777)  # creates new object subdirectory
    dump(index_init, open(archive_path + "/index", 'wb'))  # creates empty? index file
    print("Archive successfully created")
    logger.info("Archive successfully created")