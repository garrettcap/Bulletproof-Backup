import os
import shutil
import hashlib
from pprint import pprint
from cPickle import dump, load


def index_check_and_add(hash_name, relative_path, file_name, index_file):
    file_path = os.path.join(relative_path, file_name)
    index_file[hash_name] = file_path
    return file_path


class Store:
    def __init__(self, index_path, objects_path, logger):
        self.myIndex = index_path
        self.myObjects = objects_path
        self.logger = logger

    def create_file_signature(self, filename):
        temp_file = None
        signature = None
        try:
            temp_file = open(filename, "rb")
            file_hash = hashlib.sha1()
            s = temp_file.read(16384)
            while s:
                file_hash.update(s)
                s = temp_file.read(16384)
            hash_value = file_hash.hexdigest()
            signature = hash_value
        except IOError:
            signature = None
            self.logger.error(IOError)
        except OSError:
            signature = None
            self.logger.error = OSError
        finally:
            if temp_file:
                temp_file.close()
                self.logger.info("Hashing successful " + filename)
                return signature

    def store_backup(self, user_input_directory):
        index_file = load((open(self.myIndex, 'rb')))  # loads index file
        files_not_added_count = 0  # file not added counter duh!
        new_files_added = []  # really....
        self.logger.info("Backup init successful")  # logger

        for root, dirs, files in os.walk(user_input_directory):
            for file_name in files:
                original_path = os.path.join(root, file_name)
                hash_name = self.create_file_signature(original_path)  # creates a hash for the file
                self.logger.info(hash_name)
                if hash_name in index_file:  # checks file against index
                    files_not_added_count += 1
                else:
                    relative_path = os.path.relpath(root, user_input_directory)
                    os.chdir(self.myObjects)
                    if not os.path.exists(relative_path):
                        os.makedirs(relative_path)
                    file_backup_path = os.path.join(relative_path, hash_name)
                    shutil.copy2(original_path, file_backup_path)  # copies files...
                    #  adds files to index and new files added list
                    new_file = index_check_and_add(hash_name, relative_path, file_name, index_file)
                    new_files_added.append(new_file)  # adds files to

        dump(index_file, open(self.myIndex, "wb"))  # dumps info into index file
        print("Files not added: " + str(files_not_added_count))
        print("New files added: ")
        pprint(new_files_added)
        self.logger.info("Backup Successful")

        #store_backup("/home/gar/Desktop/moop") # use for testing purposes