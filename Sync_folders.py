import os
import shutil
import time
import logging
import hashlib
import argparse


def parse_arguments():
    """
    Command line arguments parser.

    Returns
    -------
    _type_
        _description_
    """
    parser = argparse.ArgumentParser(description="Folder Synchronization")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument(
        "--interval",
        type=int,
        default=1800,
        help="Synchronization interval in seconds (default: 1800)",
    )
    parser.add_argument(
        "--log-file",
        default="sync_log.txt",
        help="Path to the log file (default: sync_log.txt)",
    )
    return parser.parse_args()


def compare_files(source: str, replica: str) -> bool:
    """
    Comparison between two files using sha3 hashing algorithm (hashlib library).

    Parameters
    ----------
    source : str
        Name of file in source folder.
    replica : str
        Name of file in replica folder.

    Returns
    -------
    bool
        True if content of the files is identical, False otherwise.
    """
    with open(source, "rb") as source_file:
        source_hash = hashlib.sha3_256(source_file.read()).hexdigest()
    with open(replica, "rb") as replica_file:
        replica_hash = hashlib.sha3_256(replica_file.read()).hexdigest()

    return source_hash == replica_hash


def compare_folders(source: str, replica: str):
    """
    Basic logic of comparing two folders and synchronizing files one-way (replica folder needs to be the same as source folder).
    If needed, it occurs some operations (e.g. copying files from source to replica), and it is logged in the log file.

    Parameters
    ----------
    source : str
        Path of source folder.
    replica : str
        Path of replica folder.
    """
    # print(os.listdir(source))
    # print(os.listdir(replica))

    def comparing_files(file1_path: str, file2_path: str):
        if file2_path == file1_path:
            if compare_files(file1_path, file2_path):
                print("3 - True - same file. Operations not needed.")
                return True
            else:
                # remove file_replica
                os.remove(file2_path)
                logging.info("File %s removed from replica.", file2_path)
                # copy file to replica dir
                shutil.copy2(file1_path, file2_path) #### ERRO !
                logging.info("File %s copied from source to replica.", file1_path)
                return False

    for file_replica in os.listdir(replica):
        if file_replica not in os.listdir(source):
            # remove file_replica
            print(
                "2 - File %s not in source - removing it now.", file_replica
            )  # file not in source,  remove from replica
            os.remove(replica + "/" + file_replica)
            logging.info("File %s removed from replica.", file_replica)

    for file in os.listdir(source):
        print(file, os.path.isdir(source+'/'+file))
        # print(os.path.isfile(source+'/'+file))
        if os.path.isdir(source+'/'+file): # if 'file' is a directory instead of file
            if file not in os.listdir(replica):
                # copy dir to replica
                shutil.copytree(source + "/" + file, replica + "/" + file) #copy dir with all contents to replica
                logging.info("DIR %s copied from source to replica.", file)
            else:
                print('TESTE')
                for dir_file in os.listdir(source+'/'+file):
                    comparing_files(source + "/" + file+'/'+dir_file, replica + "/" + file + '/' + dir_file) ####################


        elif file not in os.listdir(replica):
           # file not in replica, copy from source to replica
            shutil.copy2(source + "/" + file, replica)  # copy2 preserves metadata
            logging.info("File %s copied from source to replica.", file)

        else:  # if files with same name, compare hash
            for file_replica in os.listdir(replica):
                if file_replica == file:
                    if compare_files(source + "/" + file, replica + "/" + file_replica):
                        # print("3 - True - same file. Operations not needed.")
                        continue
                    else:
                        # remove file_replica
                        os.remove(replica + "/" + file_replica)
                        logging.info("File %s removed from replica.", file_replica)
                        # copy file to replica dir
                        shutil.copy2(source + "/" + file, replica)
                        logging.info("File %s copied from source to replica.", file)

    # if dir inside source instead of file, copy also dir with shutil.copytree
    # para remover dir usar shutil.rmtree


# main loop with paths and interval as arguments


def synchronize_folders(source: str, replica: str, interval: int, log_file: str):
    """
    Main loop of synchronization between source and replica folders, with a custom period of time and a log file defined.

    Parameters
    ----------
    source : str
        Path of source folder.
    replica : str
        Path of replica folder.
    interval : int
        Interval in seconds for each synchronization (period of time).
    log_file : str
        Path to the log file.
    """
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        filename=log_file,
        encoding="utf-8",
        level=logging.DEBUG,
    )  # using logging library as is more scalable and standard
    logging.info("STARTING SYNCHRONIZATION with an interval of %s seconds.", interval)
    n = 0

    while True:
        n += 1
        compare_folders(source, replica)
        logging.info("Synchronization %s successful.", n)
        # periodically synchronize folders
        # time.sleep(interval)
        break


if __name__ == "__main__":
    args = parse_arguments()
    synchronize_folders(args.source, args.replica, args.interval, args.log_file)
