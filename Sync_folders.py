import os
import shutil
import time
import logging
import hashlib
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Folder Synchronization")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("--interval", type=int, default=10, help="Synchronization interval in seconds (default: 1800)")
    parser.add_argument("--log-file", default="sync_log.txt", help="Path to the log file (default: sync_log.txt)")
    return parser.parse_args()


# write log for each operation (logging library?)

# give hash of file (sha3 more secure)

# compare files with hash 

# compare folders (loop for each file inside each folder)

def compare_folders(source, replica, log_file):

    # if different:
    # copy file X from source folder to replica folder
    file = "test1.txt"
    shutil.copy2(source+"/"+file, replica) # cope2 preserves metadata
    # remove file x from replica if not existing in source folder
    # if dir inside source instead of file, copy also dir with shutil.copytree
    # para remover dir usar shutil.rmtree


# main loop with paths and interval as arguments 

def synchronize_folders(source, replica, interval, log_file):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename=log_file, encoding='utf-8', level=logging.DEBUG)
    logging.info(f'STARTING SYNCHRONIZATION with an interval of {interval} seconds.')
    
    while True:
        # cenas
        logging.info('teste intervalo')

        time.sleep(interval)


if __name__ == "__main__":
    args = parse_arguments()
    synchronize_folders(args.source, args.replica, args.interval, args.log_file)