# Janitor - Personal Cleaner Files Script

This script scans a folder of your choice and moves files to target folders based on their extensions and age. It supports commonly used file types and can automatically organize and archive old files.

## Requirements

- Python 3.8+
- PyYAML (`pip install -r requirements.txt`)

## Usage

Run the script from the command line:

```bash
python src/personal_janitor.py
```

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--source PATH` | `~/Downloads` | Source directory to scan |
| `--days N` | `7` | Minimum file age in days before moving |
| `--config PATH` | `../config/filetype_mapping.yaml` | Path to the config file |

**Examples:**

```bash
# Use defaults (scan ~/Downloads, move files older than 7 days)
python src/personal_janitor.py

# Scan a different folder
python src/personal_janitor.py --source ~/Desktop

# Change the age threshold to 30 days
python src/personal_janitor.py --days 30

# Use a custom config file
python src/personal_janitor.py --config /path/to/my_config.yaml
```

## Configuration

File type associations are defined in `config/filetype_mapping.yaml`. The file has two sections:

- **`destinations`**: Maps a category name to a target folder path (supports `~` for home directory).
- **`file_types`**: Maps each category name to a list of file extensions.

### Adding a New File Type

To add a new category (e.g., "music"), add an entry to both sections:

```yaml
destinations:
    audio: ~/Music          # add your new destination here
    ...

file_types:
    audio:                  # add your new extensions here
    - .mp3
    - .flac
    ...
```

To add extensions to an existing category, simply add them to the list under `file_types`.

## Supported File Types

| Category | Extensions |
|----------|------------|
| Audio | .aac, .aiff, .flac, .m4a, .mp3, .oga, .opus, .wav, .wma |
| 3D Prints | .3mf, .stl |
| Docs | .doc, .docx, .json, .log, .odt, .pdf, .txt |
| eBooks | .epub, .mobi |
| Excel | .csv, .parquet, .xls, .xlsm, .xlsx |
| Images | .jpg, .jpeg, .png, .gif, .webp, .tiff, .psd, .raw, .heif, .heic, .svg, .ai, .eps, and more |
| PowerBI | .pbids, .pbit, .pbix, .rdl, .rdlc, .pbiviz, and more |
| PowerPoint | .ppt, .pptx |
| Programs | .AppImage, .apk, .exe, .msi |
| Python | .ipynb, .py |
| SQL | .sql |
| Videos | .mp4, .mkv, .avi, .mov, .wmv, .webm, .mts, .m2ts, .ts, and more |
| Web | .htm, .html |
| Zips | .7z, .deb, .gz, .rar, .tar, .tar.xz, .tgz, .zip |

## Behavior Notes

- Files are only moved if they are **older than the `--days` threshold** (based on modification time, falling back to creation time).
- If a file with the same name already exists in the destination, a numbered suffix is appended automatically (e.g., `report(1).pdf`).
- Destination folders are created automatically if they do not exist.
- A log file is written to the `log/` directory one level above `src/`, named `personal_janitor_MM_DD_YYYY.log`.

## Functions

- `make_unique(destination, name)`: Returns a unique filename by appending a counter suffix if a file with that name already exists.
- `move_file(source, destination, name)`: Moves a file to the destination, using `make_unique` to avoid overwrites. Logs success or failure.
- `check_files_in_dir(base_folder, days_threshold)`: Scans the source folder, matches each file to a type via the YAML config, and moves files older than the threshold to their destination.

## Credit

Sourced idea from: https://www.youtube.com/watch?v=QjAHcKPUaFM and https://github.com/tuomaskivioja/File-Downloads-Automator/
My thanks to Tuomas for the inspiration!
