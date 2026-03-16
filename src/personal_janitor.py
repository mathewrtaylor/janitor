#!/usr/bin/env python
# coding: utf-8
"""
Personal Cleaner Files Script

This script is designed to scan folder of choice and move to target folders.
This looks for commonly used extensions.

Usage:
    - Adjust the source_dir folder to match your target folder (Downloads or Documents is common)
    - In the config folder, add or change any file associations in the filetype_mapping.yaml file
    - Run the script to automatically organize and archive old files.

CLI Options:
    --source PATH     Source directory to scan (default: ~/Downloads)
    --days N          Minimum age in days before moving a file (default: 7)
    --config PATH     Path to filetype_mapping.yaml (default: ../config/filetype_mapping.yaml)

Notes:
    - A log file will be created in a directory one level up from this file.
    - If a file with the same name already exists in the destination, a numbered
      suffix is appended (e.g., example(1).txt).
"""

import argparse
import logging
import os
import shutil
import yaml
from datetime import datetime
from pathlib import Path
from typing import Union


def make_unique(destination: str, name: str) -> str:
    """
    Ensure unique filenames by appending a numerical suffix if the filename already exists in the destination directory.

    Args:
        destination (str): The destination directory where the file will be saved.
        name (str): The original filename.

    Returns:
        str: A unique filename that does not exist in the destination directory.

    Example:
        If a file named "example.txt" already exists in the destination directory,
        the function will return a unique filename like "example(1).txt".
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


def move_file(source: Union[str, Path], destination: str, name: str) -> None:
    """
    Moves a file from the source path to the destination path.

    Args:
        source (Union[str, Path]): The path to the source file.
        destination (str): The path to the destination directory.
        name (str): The name of the file.

    Returns:
        None

    Notes:
        - If a file with the same name already exists in the destination directory,
          a unique name is generated using the `make_unique` function.
        - The file is then moved to the destination directory.
        - A log entry is created indicating the file movement.
    """
    if os.path.isfile(os.path.join(destination, name)):
        unique_name = make_unique(destination, name)
        dest_name = os.path.join(destination, unique_name)
    else:
        dest_name = os.path.join(destination, name)
    try:
        shutil.move(source, dest_name)
        logging.info(f"Moved: {name} to {str(dest_name)}")
    except (PermissionError, OSError) as e:
        logging.error(f"Could not move '{source}': {e}")


def check_files_in_dir(base_folder: Union[str, Path], days_threshold: int) -> None:
    """
    Move files in the base_folder to their respective destination folders based on their extensions
    if they are older than the specified days_threshold.

    Args:
        base_folder (Union[str, Path]): The base folder path to scan.
        days_threshold (int): The threshold in days for the age of the files.

    Returns:
        None
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
                    if name.lower().endswith(extension.lower()):
                        # Get the destination folder
                        destination_folder = dest_dirs.get(file_type)

                        if destination_folder:
                            # Move the file to the appropriate destination directory if it's old enough
                            try:  # Accounting for files with no modifications, and only a create time
                                modification_time = datetime.fromtimestamp(
                                    os.path.getmtime(files.path)
                                )
                                # Calculate the difference between current date and modification time
                                difference = current_date - modification_time
                            except OSError:
                                creation_time = datetime.fromtimestamp(
                                    os.path.getctime(files.path)
                                )
                                # Calculate the difference between current date and creation time
                                difference = current_date - creation_time
                            # Move the file if it's over threshold
                            if difference.days > days_threshold:
                                os.makedirs(destination_folder, exist_ok=True)
                                move_file(files.path, destination_folder, files.name)
                                break  # No need to continue checking extensions once moved


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by type and age."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.home() / "Downloads",
        help="Source directory to scan (default: ~/Downloads)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Minimum age in days before moving a file (default: 7)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to filetype_mapping.yaml (default: ../config/filetype_mapping.yaml)",
    )
    args = parser.parse_args()

    # Setting up Audit Log
    # Used for troubleshooting
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
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    days_threshold = args.days
    source_dir = args.source

    # Add / Change filetype associations in the filetype_mapping.yaml file in config.
    if args.config:
        config_file = args.config
    else:
        config_path = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "config")
        config_file = os.path.join(config_path, "filetype_mapping.yaml")

    try:
        with open(config_file, "r") as f:
            config_data = yaml.load(f, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_file}")
        raise SystemExit(f"Error: Configuration file not found: {config_file}")
    except yaml.YAMLError as e:
        logging.error(f"Failed to parse configuration file: {e}")
        raise SystemExit(f"Error: Failed to parse configuration file: {e}")

    if "destinations" not in config_data or "file_types" not in config_data:
        raise SystemExit(
            "Error: Configuration file must contain 'destinations' and 'file_types' keys."
        )

    dest_dirs = {key: Path(path).expanduser() for key, path in config_data["destinations"].items()}
    file_type_mapping = config_data["file_types"]

    check_files_in_dir(source_dir, days_threshold)
    logging.info(
        f"Finished organizing files older than {days_threshold} days and placed them in the appropriate folders."
    )
