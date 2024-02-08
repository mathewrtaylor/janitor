#!/usr/bin/env python
# coding: utf-8
"""
Personal Cleaner Files Script

This script is designed to scan folder of choice and move to target folders.
This looks for commonly used extensions.

Usage:
    - Adjust the source_dir folder to match your target folder(Downloads or Documents is common)
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
from datetime import datetime, timedelta
from pathlib import Path

# Set to each user defaults, adjust as appropriate
source_dir = Path.home() / "Downloads"
dest_dir_three_d = Path.home() / "Documents/3dPrints"
dest_dir_docs = Path.home() / "Documents/Docs"
dest_dir_ebooks = Path.home() / "Documents/eBooks"
dest_dir_excel = Path.home() / "Documents/Excel"
dest_dir_images = Path.home() / "Pictures"
dest_dir_powerbi = Path.home() / "Documents/PowerBI"
dest_dir_powerpoint = Path.home() / "Documents/Powerpoint"
dest_dir_programs = Path.home() / "Documents/Programs"
dest_dir_python = Path.home() / "Documents/Python"
dest_dir_sql = Path.home() / "Documents/SQL"
dest_dir_videos = Path.home() / "Videos"
dest_dir_web = Path.home() / "Documents/Web"
dest_dir_zips = Path.home() / "Documents/Zip"

# Supported 3d file types:
three_d_extensions = [".3mf", ".stl"]

# Supported Docs file types:
docs_extensions = [".doc", ".docx", ".json", ".log", ".odt", ".pdf", ".txt"]

# Supported ebook file types:
ebooks_extensions = [".epub", ".mobi"]

# Supported excel file types:
excel_extensions = [".csv", ".xls", ".xlsm", ".xlsx"]

# Supported images file types:
images_extensions = [
    ".jpg",
    ".jpeg",
    ".jpe",
    ".jif",
    ".jfif",
    ".jfi",
    ".png",
    ".gif",
    ".webp",
    ".tiff",
    ".tif",
    ".psd",
    ".raw",
    ".arw",
    ".cr2",
    ".nrw",
    ".k25",
    ".bmp",
    ".dib",
    ".heif",
    ".heic",
    ".ind",
    ".indd",
    ".indt",
    ".jp2",
    ".j2k",
    ".jpf",
    ".jpx",
    ".jpm",
    ".mj2",
    ".svg",
    ".svgz",
    ".ai",
    ".eps",
    ".ico",
]

# Supported powerbi file types:
powerbi_extensions = [".pbids", ".pbit", ".pbix", ".potx", ".rdl"]

# Supported powerpoint file types:
powerpoint_extensions = [".ppt", ".pptx"]

# Supported program file types:
program_extensions = [".AppImage", ".apk", ".exe", ".msi"]

# Supported python file types:
python_extensions = [".ipynb", ".py"]

# Supported sql file types:
sql_extensions = [".sql"]

# Supported video file types:
videos_extensions = [
    ".webm",
    ".mpg",
    ".mp2",
    ".mpeg",
    ".mpe",
    ".mpv",
    ".ogg",
    ".mp4",
    ".mp4v",
    ".m4v",
    ".avi",
    ".wmv",
    ".mov",
    ".qt",
    ".flv",
    ".swf",
    ".avchd",
]

# Supported web file types:
web_extensions = [".htm", ".html"]

# Supported zips file types:
zips_extensions = [".7z", ".deb", ".gz", ".rar", ".tar", ".tar.xy", ".tar.xz", ".tgz", ".zip"]


def make_unique(destination, name):
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


def move_file(source, destination, name):
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


def check_files_in_dir(base_folder, days_threshold):
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
    for files in os.scandir(base_folder):
        if files.is_file():
            name = files.name
            # Defining mappings of extensions
            extension_mappings = {
                tuple(three_d_extensions): dest_dir_three_d,
                tuple(docs_extensions): dest_dir_docs,
                tuple(ebooks_extensions): dest_dir_ebooks,
                tuple(excel_extensions): dest_dir_excel,
                tuple(images_extensions): dest_dir_images,
                tuple(powerbi_extensions): dest_dir_powerbi,
                tuple(powerpoint_extensions): dest_dir_powerpoint,
                tuple(program_extensions): dest_dir_programs,
                tuple(python_extensions): dest_dir_python,
                tuple(sql_extensions): dest_dir_sql,
                tuple(videos_extensions): dest_dir_videos,
                tuple(web_extensions): dest_dir_web,
                tuple(zips_extensions): dest_dir_zips,
            }

            # Iterate over the mappings
            for extensions, destination_folder in extension_mappings.items():
                # Check if the file extension matches any in the current mapping setups
                for extension in extensions:
                    if name.endswith(extension) or name.endswith(extension.upper()):
                        # Move the file to the appropriate destination directory if it's old enough
                        try:  # Accounting for files with no modifications, and only a create time
                            modification_time = datetime.fromtimestamp(
                                os.path.getmtime(files)
                            )
                            # Calc the difference between current date and threshold
                            difference = current_date - modification_time
                        except:
                            creation_time = datetime.fromtimestamp(
                                os.path.getctime(files)
                            )
                            # Calc the difference between current date and threshold
                            difference = current_date - creation_time
                        # Move it if it's over threshold
                        if difference.days > days_threshold:
                            os.makedirs(destination_folder, exist_ok=True)
                            source_path = Path(files)
                            move_file(source_path, destination_folder, files.name)


if __name__ == "__main__":
    ## Setting up Audit Log
    ## Used for troubleshooting

    full_script_name = os.path.basename(__file__)
    script_name = full_script_name[: full_script_name.rindex(".")]
    now = datetime.now()  # current date and time
    log_name = f'{script_name}_{now.strftime("%m_%d_%Y")}.log'
    log_path = os.path.join(Path(os.path.abspath(__file__)).parent, "log")  # This puts a log directory one level up from this file.
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

    check_files_in_dir(source_dir, days_threshold)
    logging.info(
        "Cleaned up log files older than a week and placed them in the appropriate folder."
    )