import os
import shutil
import argparse
import logging
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

# Define file categories and their corresponding extensions
CATEGORIES = {
    'Images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.heic'},
    'Videos': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'},
    'Documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.md', '.log'},
    'Audio': {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'},
    'Archives': {'.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.xz'}
}

def get_category(extension):
    """Return the category based on the file extension."""
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return 'Other'

def get_creation_date(path):
    """
    Get the creation date of a file.
    Falls back to last modified time on systems where birth time is unavailable (e.g., standard Linux).
    """
    stat = path.stat()
    try:
        # st_birthtime is available on Windows and macOS
        return datetime.fromtimestamp(stat.st_birthtime)
    except AttributeError:
        # Fallback to st_mtime (last modified) on Linux
        return datetime.fromtimestamp(stat.st_mtime)

def generate_unique_filename(destination_dir, filename):
    """
    Generate a unique filename to prevent overwriting existing files.
    If 'file.txt' exists, it tries 'file_1.txt', 'file_2.txt', etc.
    """
    destination_path = destination_dir / filename
    if not destination_path.exists():
        return destination_path

    stem = destination_path.stem
    suffix = destination_path.suffix
    counter = 1

    while True:
        new_filename = f"{stem}_{counter}{suffix}"
        new_path = destination_dir / new_filename
        if not new_path.exists():
            return new_path
        counter += 1

def organize_files(source_dir, dry_run=False):
    source_path = Path(source_dir).resolve()
    
    if not source_path.is_dir():
        print(f"Error: The directory '{source_dir}' does not exist.")
        return

    # Setup logging configuration
    log_file = source_path / 'organize_files.log'
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Collect files to move (ignore the script itself, logs, and subdirectories)
    files_to_move = [
        f for f in source_path.iterdir() 
        if f.is_file() and f.name not in ('organize_files.log', 'organize_files.py')
    ]
    
    if not files_to_move:
        print("No files found to organize.")
        return

    print(f"Found {len(files_to_move)} file(s) to organize.")
    
    if dry_run:
        print("\n--- DRY RUN MODE ENABLED ---")
        print("No files will be moved. Check output below and logs for what would happen.\n")
        logging.info("=== STARTED ORGANIZATION (DRY RUN) ===")
    else:
        logging.info("=== STARTED ORGANIZATION ===")

    # Process each file with a nice progress bar
    for file_path in tqdm(files_to_move, desc="Organizing files", unit="file"):
        category = get_category(file_path.suffix)
        creation_date = get_creation_date(file_path)
        
        year = creation_date.strftime('%Y')
        month = f"{creation_date.strftime('%m')} - {creation_date.strftime('%B')}"
        
        # Formulate destination directory path based on logic
        dest_dir = source_path / category / year / month
        
        # Formulate final unique destination path
        dest_path = generate_unique_filename(dest_dir, file_path.name)
        
        if dry_run:
            logging.info(f"[WOULD MOVE] '{file_path.name}' -> '{dest_path.relative_to(source_path)}'")
        else:
            try:
                # Create destination directory structure if it doesn't exist
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                # Perform the move
                shutil.move(str(file_path), str(dest_path))
                logging.info(f"[MOVED] '{file_path.name}' -> '{dest_path.relative_to(source_path)}'")
            except Exception as e:
                logging.error(f"[ERROR] Failed to move '{file_path.name}': {str(e)}")

    if dry_run:
        print("\nDry run complete. Read 'organize_files.log' in the folder for details.")
    else:
        print(f"\nOrganization complete! Check '{log_file.name}' for a detailed report.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automatically organize files by type, year, and month."
    )
    parser.add_argument(
        "directory", 
        help="Path to the directory you want to organize."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Simulate the process without moving any files."
    )
    
    args = parser.parse_args()
    organize_files(args.directory, args.dry_run)
