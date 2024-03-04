"Program for synchronizing folders using recursive copy and remove operations."

# Libraries used:
import os
import shutil
import time
import logging
import hashlib
import argparse


def parse_arguments() -> argparse.ArgumentParser:
    """
    Parse command line arguments for the folder synchronization program.

    source: Path to the source folder to be synchronized.
    replica: Path to the replica folder where changes will be replicated.
    --interval: Synchronization interval in seconds (default: 1800 seconds).
    --log-file: Path to the log file (default: sync_log.txt).

    Returns
    -------
    argparse.Namespace
        An object containing the parsed command line arguments.

    Example of usage:
    >>> python sync_folders.py /path/to/source /path/to/replica --interval 3600 --log-file custom_log.txt
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
    for file in os.listdir(source):
        file_path = os.path.join(source, file)
        file_replica_path = os.path.join(replica, file)
        if os.path.isdir(file_path):  # if 'file' is a directory instead of file
            subfolder = file
            if subfolder not in os.listdir(replica):
                shutil.copytree(
                    file_path, file_replica_path
                )  # copy dir with all contents to replica
                logging.info("Subfolder %s copied from source to replica.", subfolder)
            else:
                compare_folders(
                    file_path, os.path.join(replica, subfolder)
                )  # recursive

        elif file not in os.listdir(replica):
            # file not in replica, copy from source to replica
            shutil.copy2(file_path, replica)  # copy2 preserves metadata
            logging.info("File %s copied from source to replica.", file)

        else:  # if files with same name, compare hash
            for file_replica in os.listdir(replica):
                if file_replica == file:
                    if compare_files(file_path, file_replica_path):
                        pass
                    else:
                        # remove file_replica
                        os.remove(file_replica_path)
                        logging.info("File %s removed from replica.", file_replica)
                        # copy file to replica dir
                        shutil.copy2(file_path, replica)
                        logging.info("File %s copied from source to replica.", file)

    for file_replica in os.listdir(replica):
        if file_replica not in os.listdir(source):
            rep_path = os.path.join(replica, file_replica)
            if os.path.isdir(rep_path):
                shutil.rmtree(rep_path)
                logging.info("Subfolder %s removed from replica.", file_replica)
            os.remove(rep_path)
            logging.info("File %s removed from replica.", file_replica)


def synchronize_folders(source: str, replica: str, interval: int, log_file: str):
    """
    Main loop of synchronization between source and replica folders (subfolders included), with a custom period of time and a log file defined.
    It is executed in a loop until the program is terminated.

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
        time.sleep(interval)


if __name__ == "__main__":
    args = parse_arguments()
    synchronize_folders(args.source, args.replica, args.interval, args.log_file)
