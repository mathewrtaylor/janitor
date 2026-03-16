# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-03-16

### Added
- CLI argument support via `argparse`: `--source`, `--days`, `--config` flags allow runtime configuration without editing source code.
- Audio file type category with destination `~/Music`, supporting: `.aac`, `.aiff`, `.flac`, `.m4a`, `.mp3`, `.oga`, `.opus`, `.wav`, `.wma`.
- Missing video formats: `.mkv`, `.mts`, `.m2ts`, `.ts`.
- Config file validation: clear error messages if `filetype_mapping.yaml` is missing, malformed, or has an invalid structure.

### Fixed
- Bare `except:` clause replaced with `except OSError` to avoid catching `KeyboardInterrupt` and `SystemExit`.
- Removed duplicate `import datetime` (shadowed by `from datetime import datetime`).
- Removed unused imports: `sys`, `timedelta`.
- Removed debug `print()` statement from `move_file`.
- Fixed inconsistent path construction in `move_file` — now uses `os.path.join` consistently.
- Fixed `os.path.getmtime(files)` and `os.path.getctime(files)` to use `files.path` explicitly.
- Fixed extension matching to use `.lower()` on both the filename and extension, handling mixed-case extensions (e.g., `.JPG`, `.Jpg`).
- Fixed type hint for `source` parameter in `move_file` to `Union[str, Path]`.
- Fixed invalid `.tar.xy` extension in config (removed duplicate; `.tar.xz` retained).
- Removed internal/temporary PowerBI extensions (`.pbix.d`, `.pbix.tmp`, `.pbit.tmp`, `.pbix.asdatabase`, etc.) that clutter the destination folder.
- Fixed misleading log message: now reports "Finished organizing files older than N days" instead of "Cleaned up log files".
- Fixed module docstring typo: "confifg" → "config".
- Replaced `##` double-hash comment style with standard `#`.

### Changed
- `days_threshold` is now configurable via `--days` CLI flag (default: 7).
- Source directory is now configurable via `--source` CLI flag (default: `~/Downloads`).

## [1.0.0] - Initial Release

### Added
- Initial file organization script scanning a source directory and moving files by extension and age.
- YAML-based configuration for file type mappings and destination directories.
- Unique filename handling to prevent overwrites.
- Daily log file written to `log/` directory.
