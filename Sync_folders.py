import os
import shutil
import time
import logging
import hashlib
import argparse

# command line arguments

def parse_arguments():
    parser = argparse.ArgumentParser(description="Folder Synchronization")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("--interval", type=int, default=1800, help="Synchronization interval in seconds (default: 1800)")
    parser.add_argument("--log-file", default="sync_log.txt", help="Path to the log file (default: sync_log.txt)")
    return parser.parse_args()


# compare files with hash 

def compare_files(source, replica): # compare hash of files (sha3 more secure)
    source_hash = hashlib.sha3_256(open(source, 'rb').read()).hexdigest()
    replica_hash = hashlib.sha3_256(open(replica, 'rb').read()).hexdigest()

    return source_hash == replica_hash

# compare folders (loop for each file inside each folder)

def compare_folders(source, replica):
    print(os.listdir(source))
    print(os.listdir(replica))

    for file_replica in os.listdir(replica):
        if file_replica not in os.listdir(source):
            # remove file_replica
            print(f'2 - File {file_replica} not in source - removing it now.') # file not in source,  remove from replica
            os.remove(replica+'/'+file_replica)
            logging.info(f'File {file_replica} removed from replica.')
    
    for file in os.listdir(source):
        if file not in os.listdir(replica): 
            # copy file to replica dir
            print(f'1 - File {file} not in replica - copying now. - ADD TO LOG') # file not in replica, copy from source to replica
            shutil.copy2(source+"/"+file, replica) # copy2 preserves metadata
            logging.info(f'File {file} copied from source to replica.')

        else: # if files with same name, compare hash 
            for file_replica in os.listdir(replica):
                if file_replica == file:
                    if compare_files(source+'/'+file, replica+'/'+file_replica):
                        print('3 - True - same file. Operations not needed.')
                    else:
                        print(f'4 - False - different contents between {file} and {file_replica}. Removing file from replica and copying now the new one. - ADD TO LOG')
                        # remove file_replica
                        os.remove(replica+'/'+file_replica)
                        logging.info(f'File {file_replica} removed from replica.')
                        # copy file to replica dir
                        shutil.copy2(source+"/"+file, replica)
                        logging.info(f'File {file} copied from source to replica.')

    # if dir inside source instead of file, copy also dir with shutil.copytree
    # para remover dir usar shutil.rmtree


# main loop with paths and interval as arguments 

def synchronize_folders(source, replica, interval, log_file):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename=log_file, encoding='utf-8', level=logging.DEBUG) # using logging library as is more scalable and standard
    logging.info(f'STARTING SYNCHRONIZATION with an interval of {interval} seconds.')
    n = 0
    
    while True:
        n += 1
        compare_folders(source, replica)
        logging.info(f'Synchronization {n} successful.')
        # periodically synchronize folders
        time.sleep(interval)


if __name__ == "__main__":
    args = parse_arguments()
    synchronize_folders(args.source, args.replica, args.interval, args.log_file)