# FolderZen 🧘‍♂️📁

A robust, cross-platform Python tool suite that automatically untangles chaotic folders by organizing files into elegant subfolders based on their **File Type**, followed by the **Year** and **Month** they were created.

## 🚀 Features

- **Automated Categorization**: Sorts files into `Images`, `Videos`, `Documents`, `Audio`, `Archives`, and `Other`.
- **Chronological Sorting**: Inside each category, creates folders for the `Year` and `Month` (e.g., `Images/2023/10 - October/`).
- **Dry-run Mode**: Safely test the script to see what *would* happen without actually applying the changes, giving you complete peace of mind.
- **Smart Conflict Resolution**: Never overwrites files. If a duplicate name exists, it automatically appends a number (e.g., `photo_1.jpg`).
- **Comprehensive Logging**: Generates a detailed `organize_files.log` file showing every action taken.
- **Progress Tracking**: Features a sleek, terminal-based progress bar using `tqdm`.
- **Reversible Actions**: Included `undo_organize.py` script lets you safely revert changes if you change your mind!

## ⚙️ Requirements

- Python 3.6+
- Works on Windows, macOS, and Linux
- `tqdm` module for the progress bar

## 📦 Installation

1. Ensure you have Python installed. You can download it from [python.org](https://python.org).
2. Install the required dependency using `pip`:

```bash
pip install tqdm
```

3. Download or copy the scripts (`organize_files.py` and `undo_organize.py`) to your computer.

## 💻 Usage

Run the scripts from your terminal or command prompt by passing the path of the folder you want to organize.

### 1. Organize Files
**Basic Setup (Moving Files):**
```bash
python organize_files.py /path/to/your/messy/folder
```

**(Highly Recommended) Dry-Run Mode:**
Use the `--dry-run` flag to simulate the process. It will show you exactly where files *would* go, without touching or moving anything.

```bash
python organize_files.py /path/to/your/messy/folder --dry-run
```

### 2. Undo Organization
If you organized a folder but decide to revert it, `undo_organize.py` can parse the log file and return all moved files to their original location.

```bash
python undo_organize.py /path/to/your/messy/folder
```
*Note: Make sure the `organize_files.log` is still inside the target directory!*

## 🔍 How It Works

If your folder looks like this:
```
/Downloads
  vacation_pic.jpg  (Created Nov 2023)
  tax_return.pdf    (Created Apr 2023)
  song.mp3          (Created Nov 2023)
```

Running `organize_files.py` will transform it into:
```
/Downloads
  /Images
    /2023
      /11 - November
        vacation_pic.jpg
  /Documents
    /2023
      /04 - April
        tax_return.pdf
  /Audio
    /2023
      /11 - November
        song.mp3
  organize_files.log
```

## 📝 Notes
- **Linux Notice**: On standard Linux filesystems, exact "Creation Date" is often unavailable, so the script defaults to the "Last Modified" time. On Windows and macOS, the true creation (`st_birthtime`) is accurately leveraged.
- **Safety**: The script refuses to move itself (`organize_files.py`, `undo_organize.py`) or its own log file (`organize_files.log`) to keep things tidy.
