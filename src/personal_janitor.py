#!/usr/bin/env python
# coding: utf-8
"""
Personal Cleaner Files Script

This script is designed to scan folder of choice and move to target folders.
This looks for commonly used extensions.

Usage:
    - Adjust the source_dir folder to match your target folder(Downloads or Documents is common)
    - In the confifg folder, add or change any file associations in the filetype_mapping.yaml file
    - Run the script to automatically organize and archive old files.

Notes:
    - A log file will be created in a directory one level up
"""

import datetime
import logging
import os
import socket
import sys
import shutil
import yaml
from datetime import datetime, timedelta
from pathlib import Path


def make_unique(destination: str, name: str) -> str:
    """
    Ensure unique filenames by appending a numerical suffix if the filename already exists in the destination directory.

    Args:
        destination (str): The destination directory where the file will be saved.
        name (str): The original filename.

    Returns:
        str: A unique filename that does not exist in the destination directory.

    Example:
        If a file named "example.txt" already exists in the destination directory, the function will return a unique filename like "example(1).txt".
    """
    destination_path = Path(destination)
    base_name = destination_path / name
    if not base_name.exists():
        return name
    stem = base_name.stem
    suffix = base_name.suffix

    counter = 1
    # If file exists, adds a number to the end of the filename
    while (destination_path / f"{stem}({counter}){suffix}").exists():
        counter += 1
    return f"{stem}({counter}){suffix}"


def move_file(source: str, destination: str, name: str) -> None:
    """
    Moves a file from the source path to the destination path.

    Args:
        source (str): The path to the source file.
        destination (str): The path to the destination directory.
        name (str): The name of the file.

    Returns:
        None: The function does not return any value.

    Notes:
        - If a file with the same name already exists in the destination directory,
          a unique name is generated using the `make_unique` function.
        - The file is then moved to the destination directory.
        - A log entry is created indicating the file movement.
    """
    if os.path.isfile(f"{destination}/{name}"):
        unique_name = make_unique(destination, name)
        dest_name = os.path.join(destination, unique_name)
    else:
        dest_name = os.path.join(destination, name)
    print(source, dest_name)
    shutil.move(source, dest_name)
    logging.info(f"Moved: {name} to {str(dest_name)}")


def check_files_in_dir(base_folder: str, days_threshold: int) -> None:
    """
    Move files in the base_folder to their respective destination folders based on their extensions
    if they are older than the specified days_threshold.

    Args:
    - base_folder (str): The base folder path.
    - days_threshold (int): The threshold in days for the age of the files.

    Returns:
    - None
    """
    # Get current date
    current_date = datetime.now()
    
    # Iterate over files in base_folder
    for files in os.scandir(base_folder):
        if files.is_file():
            name = files.name
            # Iterate over file type mappings
            for file_type, extensions in file_type_mapping.items():
                # Check if the file extension matches any in the current mapping setups
                for extension in extensions:
                    if name.endswith(extension) or name.endswith(extension.upper()):
                        # Get the destination folder
                        destination_folder = dest_dirs.get(file_type)
                        if destination_folder:
                            # Move the file to the appropriate destination directory if it's old enough
                            try:  # Accounting for files with no modifications, and only a create time
                                modification_time = datetime.fromtimestamp(
                                    os.path.getmtime(files)
                                )
                                # Calculate the difference between current date and modification time
                                difference = current_date - modification_time
                            except:
                                creation_time = datetime.fromtimestamp(
                                    os.path.getctime(files)
                                )
                                # Calculate the difference between current date and creation time
                                difference = current_date - creation_time
                            # Move the file if it's over threshold
                            if difference.days > days_threshold:
                                os.makedirs(destination_folder, exist_ok=True)
                                source_path = Path(files)
                                move_file(source_path, destination_folder, files.name)
                                break  # No need to continue checking extensions once moved


if __name__ == "__main__":
    ## Setting up Audit Log
    ## Used for troubleshooting
    full_script_name = os.path.basename(__file__)
    script_name = full_script_name[: full_script_name.rindex(".")]
    now = datetime.now()  # current date and time
    log_name = f'{script_name}_{now.strftime("%m_%d_%Y")}.log'
    log_path = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "log")  # This puts a log directory one level up from this file. 
    # Change .parent.parent to .parent to keep in the same directory.
    os.makedirs(log_path, exist_ok=True)
    log_file = os.path.join(log_path, log_name)
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.disable(logging.DEBUG)
    # local_machine_running = socket.gethostname()
    days_threshold = 7

    # Add / Change filetype associations in the filetype_mapping.yaml file in config.
    config_path = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "config")
    with open(f'{config_path}\\filetype_mapping.yaml', 'r') as f:
        file_type_mapping = yaml.load(f, Loader=yaml.SafeLoader)

    # Destination directories. Set to each user defaults, adjust as appropriate.
    dest_dirs = {
        "three_d": Path.home() / "Documents/3dPrints",
        "docs": Path.home() / "Documents/Docs",
        "ebooks": Path.home() / "Documents/eBooks",
        "excel": Path.home() / "Documents/Excel",
        "images": Path.home() / "Pictures",
        "powerbi": Path.home() / "Documents/PowerBI",
        "powerpoint": Path.home() / "Documents/Powerpoint",
        "programs": Path.home() / "Documents/Programs",
        "python": Path.home() / "Documents/Python",
        "sql": Path.home() / "Documents/SQL",
        "videos": Path.home() / "Videos",
        "web": Path.home() / "Documents/Web",
        "zips": Path.home() / "Documents/Zip"
    }

    # Source Directory, where you'd like this to start.
    source_dir = Path.home() / "Downloads"    

    check_files_in_dir(source_dir, days_threshold)
    logging.info(
        "Cleaned up log files older than a week and placed them in the appropriate folder."
    )