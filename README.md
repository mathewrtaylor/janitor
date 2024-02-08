# Janitor - Personal Cleaner Files Script

This script is designed to scan a folder of choice and move files to target folders based on their extensions. It looks for commonly used extensions and can be used to automatically organize and archive old files.

## Usage

- Adjust the `source_dir` variable to match your target folder (e.g., Downloads or Documents).
- Run the script to initiate the automatic organization and archiving of old files.

## Supported File Types

The script supports the following file types and their respective destination folders:
- 3D Prints: .3mf, .stl
- Docs: .doc, .docx, .json, .log, .odt, .pdf, .txt
- eBooks: .epub, .mobi
- Excel: .csv, .xls, .xlsm, .xlsx
- Images: Various image file types
- PowerBI: .pbids, .pbit, .pbix, .potx, .rdl
- PowerPoint: .ppt, .pptx
- Programs: .apk, .exe, .msi
- Python: .ipynb, .py
- SQL: .sql
- Videos: Various video file types
- Web: .htm, .html
- Zips: .7z, .deb, .gz, .rar, .tar, .tar.xy, .tar.xz, .tgz, .zip

## Functions

The script includes the following functions:
- `make_unique(destination, name)`: Ensures unique filenames by appending a numerical suffix if the filename already exists in the destination directory.
- `move_file(source, destination, name)`: Moves a file from the source path to the destination path.
- `check_files_in_dir(base_folder, days_threshold)`: Moves files in the base_folder to their respective destination folders based on their extensions if they are older than the specified days_threshold.

## Credit
Sourced idea from: https://www.youtube.com/watch?v=QjAHcKPUaFM and https://github.com/tuomaskivioja/File-Downloads-Automator/
My thanks to Tuomas for the inspiration!
