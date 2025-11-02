#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def get_block_number(file_path: Path):
    """
    Extracts the block number from a filename.
    Expects the filename to be like "123456.png" or "123456.json".
    Returns the number as an integer, or None if it cannot be parsed.
    """
    try:
        return int(file_path.stem)
    except ValueError:
        return None

def sync_folder(source: Path, dest: Path, limit: int = 100):
    """
    Copies the latest `limit` files (based on the numerical block in the filename)
    from the source directory to the destination. Then, ensures that the destination
    holds only these latest `limit` files by deleting any older files.
    """
    # Ensure destination directory exists.
    dest.mkdir(parents=True, exist_ok=True)

    # List and filter files in the source directory based on a valid integer block
    source_files = [f for f in source.iterdir() if f.is_file()]
    valid_source_files = []
    for file in source_files:
        block_num = get_block_number(file)
        if block_num is not None:
            valid_source_files.append((block_num, file))
    
    # Sort files descending by the extracted block number.
    valid_source_files.sort(key=lambda x: x[0], reverse=True)
    
    # Select the top 'limit' files.
    latest_source_files = valid_source_files[:limit]

    # Copy each file to the destination (overwriting if necessary).
    for block, src_file in latest_source_files:
        dest_file = dest / src_file.name
        shutil.copy2(src_file, dest_file)
        print(f"Copied {src_file} to {dest_file}")

    # Now, clean up the destination directory: only keep the latest `limit` files.
    dest_files = [f for f in dest.iterdir() if f.is_file()]
    valid_dest_files = []
    for file in dest_files:
        block_num = get_block_number(file)
        if block_num is not None:
            valid_dest_files.append((block_num, file))
    
    # Sort destination files descending by the block number.
    valid_dest_files.sort(key=lambda x: x[0], reverse=True)
    
    # Determine the set of filenames that should remain.
    keep_files = {file.name for _, file in valid_dest_files[:limit]}

    # Remove any extra files from the destination.
    for _, file in valid_dest_files[limit:]:
        try:
            file.unlink()
            print(f"Removed old file {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

def main():
    # Define source paths.
    GRAPH_FOLDER_IMAGE = Path("/mnt/hdd1/storage_data/graphs_images/")
    CHART_FOLDER_IMAGES = Path("/mnt/hdd1/storage_data/chart_data_images/")
    GRAPH_DATA = Path("/mnt/hdd1/storage_data/graphs_data/")

    # Define the destination parent folder.
    DEST_BASE = Path.home() / "toni/datanalysis/vibe/dependency.pics-static"

    # Map each source folder to its correct destination subfolder.
    # The assumption here is:
    #   - Chart images go to "data"
    #   - Graph images go to "graphs"
    #   - Graphs data (JSON) go to "gantt"
    mapping = {
        CHART_FOLDER_IMAGES: DEST_BASE / "gantt",
        GRAPH_FOLDER_IMAGE: DEST_BASE / "graphs",
        GRAPH_DATA: DEST_BASE / "data",
    }

    # Process each source -> destination mapping.
    for source, dest in mapping.items():
        print(f"Syncing files from {source} to {dest}...")
        sync_folder(source, dest)
        print(f"Completed syncing for {source}\n")

if __name__ == '__main__':
    main()
