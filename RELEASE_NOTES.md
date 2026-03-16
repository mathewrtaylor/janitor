# Release Notes

## v1.1.0 - 2026-03-16

### Summary

This release focuses on bug fixes, code quality improvements, and usability enhancements. The script now supports command-line arguments, has proper error handling, and covers more file types out of the box.

### Highlights

**CLI Support** — No more editing source code to change the source folder or age threshold. Use `--source`, `--days`, and `--config` flags at runtime.

**Audio Files** — A new `audio` category routes `.mp3`, `.flac`, `.wav`, `.aac`, `.m4a`, and other audio formats to `~/Music`.

**More Video Formats** — Added `.mkv`, `.mts`, `.m2ts`, and `.ts` to the videos category.

**Better Error Messages** — If the config file is missing or invalid, the script now exits with a clear, descriptive error instead of a cryptic Python traceback.

**Case-Insensitive Matching** — File extensions are now matched case-insensitively, so `.JPG`, `.Jpg`, and `.jpg` are all handled correctly.

### Upgrade Notes

- No breaking changes. Existing `filetype_mapping.yaml` configs remain compatible.
- To use the new audio category, ensure your config has an `audio` entry under both `destinations` and `file_types` (already included in the default config).
- The hardcoded `days_threshold = 7` in source is replaced by `--days 7` as the default CLI argument.
