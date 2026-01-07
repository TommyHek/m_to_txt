# MATLAB `.m` to `.txt` Converter (Preserve Folder Structure)

A small Python utility that **recursively** converts all MATLAB `*.m` files under a given folder (including subfolders) into `*.txt` files **while preserving the original directory structure**.

The conversion is implemented as an **exact byte-for-byte copy** of the source file content (only the file extension changes). This avoids encoding problems and guarantees fidelity.

---

## What it does

For every `*.m` file found under `<INPUT_ROOT>`:

- Keeps the same relative path
- Writes the output as `*.txt` under `<OUTPUT_ROOT>`
- Default output root: `<INPUT_ROOT>_txt`

**Mapping example**

`<INPUT_ROOT>/utils/helper.m` → `<OUTPUT_ROOT>/utils/helper.txt`

---

## Requirements

- Python **3.8+**
- No third‑party packages

Check your version:

```bash
python --version
```

---

## Files

- `m_to_txt.py` — main script

---

## Quick start

### Windows (PowerShell / CMD)

```bash
python m_to_txt.py "D:\MatlabProject"
```

### macOS / Linux

```bash
python3 m_to_txt.py "/home/user/MatlabProject"
```

Outputs will be written to:

- `D:\MatlabProject_txt\...` (Windows)
- `/home/user/MatlabProject_txt/...` (macOS/Linux)

---

## Usage

```bash
python m_to_txt.py <INPUT_ROOT> [options]
```

### Options

| Option | Description | Default |
|---|---|---|
| `-o`, `--output-root <PATH>` | Set the output folder root | `<INPUT_ROOT>_txt` |
| `--overwrite` | Overwrite existing `.txt` outputs | Off (skip existing) |
| `--dry-run` | Print planned actions without writing files | Off |

---

## Examples

### 1) Convert with default output root

```bash
python m_to_txt.py "./MatlabProject"
```

### 2) Convert and set a custom output folder

```bash
python m_to_txt.py "./MatlabProject" -o "./ExportedTxt"
```

### 3) Overwrite existing outputs

```bash
python m_to_txt.py "./MatlabProject" --overwrite
```

### 4) Dry run (preview only)

```bash
python m_to_txt.py "./MatlabProject" --dry-run
```

---

## Output structure

Given the following input:

```
MatlabProject/
  main.m
  utils/
    helper.m
    io/
      read_data.m
```

Default output:

```
MatlabProject_txt/
  main.txt
  utils/
    helper.txt
    io/
      read_data.txt
```

---

## Encoding and fidelity

This tool copies files using binary read/write (`read_bytes()` → `write_bytes()`), so:

- The output `.txt` content is **identical** to the input `.m` content
- No decoding/encoding is performed
- This is the safest approach when files contain mixed encodings or special characters

If you need to **force UTF‑8 re-encoding**, you can modify the script accordingly, but note that doing so may change file bytes and may fail on non‑UTF‑8 content.

---

## Exit codes

- `0` — success (no errors)
- `2` — completed with errors (at least one file failed)

---

## Troubleshooting

### “No .m files found”
- Confirm the input path is correct.
- Ensure there are `*.m` files somewhere under the provided root.

### Permission errors
- Verify you have read access to the input folder and write access to the output folder.
- Windows: try running the terminal as Administrator.
- macOS/Linux: ensure the output path is writable (or use `sudo` only if necessary).

### I want to output inside the input folder
You can set `--output-root` to a subfolder under `<INPUT_ROOT>`, but it is generally recommended to keep output separate to avoid confusion when browsing the project.

---

## License

Add your preferred license text here (e.g., MIT, Apache-2.0), or mark as internal use only.
