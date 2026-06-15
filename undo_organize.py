import os
import shutil
import argparse
import re
from pathlib import Path
from tqdm import tqdm

def undo_organization(source_dir, dry_run=False):
    source_path = Path(source_dir).resolve()
    log_file = source_path / 'organize_files.log'
    
    if not source_path.is_dir():
        print(f"Error: The directory '{source_dir}' does not exist.")
        return
        
    if not log_file.exists():
        print(f"Error: Log file not found at '{log_file}'. Cannot undo operations without the log file.")
        return

    # Parse log file for moves
    moves_to_revert = []
    
    # Regex to match log lines: 2026-06-15 10:02:08 - INFO - [MOVED] 'filename.ext' -> 'category/year/month/filename.ext'
    # Actually, let's just do a simpler search.
    move_pattern = re.compile(r"\[MOVED\] '([^']+)' -> '([^']+)'")
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = move_pattern.search(line)
            if match:
                original_name = match.group(1)
                new_relative_path = match.group(2)
                moves_to_revert.append((original_name, new_relative_path))

    if not moves_to_revert:
        print("No moved files found in the log.")
        return

    print(f"Found {len(moves_to_revert)} file(s) to restore.")
    
    if dry_run:
        print("\n--- DRY RUN MODE ENABLED ---")
        print("No files will be moved back. Check output below for what would happen.\n")

    success_count = 0
    fail_count = 0
    
    # Reverse the order just in case, though it shouldn't matter much
    for original_name, new_rel_path in tqdm(moves_to_revert, desc="Undoing moves", unit="file"):
        current_path = source_path / new_rel_path
        restore_path = source_path / original_name
        
        # In case there was a name collision, we might not want to overwrite.
        # But if we are returning them to the original directory, since we only processed files mapped from original_name, 
        # original_name might exist if another file was called original_name? No, if it was moved, it shouldn't exist anymore in the root,
        # unless user added new files.
        if restore_path.exists():
            stem = restore_path.stem
            suffix = restore_path.suffix
            counter = 1
            while True:
                attempt = source_path / f"{stem}_{counter}{suffix}"
                if not attempt.exists():
                    restore_path = attempt
                    break
                counter += 1

        if current_path.exists():
            if dry_run:
                print(f"[WOULD RESTORE] '{current_path.relative_to(source_path)}' -> '{restore_path.relative_to(source_path)}'")
            else:
                try:
                    shutil.move(str(current_path), str(restore_path))
                    success_count += 1
                except Exception as e:
                    print(f"\n[ERROR] Failed to restore '{current_path.name}': {str(e)}")
                    fail_count += 1
        else:
            print(f"\n[WARNING] Could not find '{current_path}'. Maybe it was already moved or deleted.")
            fail_count += 1

    if dry_run:
        print("\nDry run complete. No files were changed.")
    else:
        print(f"\nUndo complete! Restored {success_count} file(s). Failed to restore {fail_count} file(s).")
        print("You may want to manually delete the empty categorized folders if no longer needed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reverts the file organization based on the organize_files.log."
    )
    parser.add_argument(
        "directory", 
        help="Path to the directory where files were organized."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Simulate the process without moving any files."
    )
    
    args = parser.parse_args()
    undo_organization(args.directory, args.dry_run)
