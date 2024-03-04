# Folder Synchronization: sync_folders


## Description: 
'sync_folders' is a simple Python program designed to unidirectionally and periodically synchronize the contents of two folders. 

It recursively compares the files and subfolders in the source folder with those in the replica folder and replicates any changes found, while also maintaining a log file of synchronization operations.

## Features:

- Unidirectionally synchronize the contents of two folders.
- Periodically check for changes in the source folder and replicate them to the replica folder.
- Log file operations to a file and to the console output.
- Support for recursive synchronization of subfolders.
- Customizable synchronization interval and log file path via command line arguments.

## Installation:

Clone the repository:

`git clone https://github.com/mleiras/sync_folders.git`

## Usage:

Run the program using the following command:

`python sync_folders.py /path/to/source /path/to/replica [--interval INTERVAL] [--log-file LOG_FILE]`

- **/path/to/source**: Path to the source folder to be synchronized.
- **/path/to/replica**: Path to the replica folder where changes will be replicated.
- **--interval INTERVAL**: Synchronization interval in seconds (default: 1800 seconds).
- **--log-file LOG_FILE**: Path to the log file (default: sync_log.txt).


Example:

`python sync_folders.py Folder_source Folder_replica --interval 300 --log-file log.txt`


## Requirements:
Python 3.x

## Libraries used:
- os
- shutil
- time
- logging
- hashlib
- argparse

## License:

This project is licensed under the MIT License. See the [LICENSE](https://raw.githubusercontent.com/mleiras/sync_folders/main/LICENSE.txt) file for details.
