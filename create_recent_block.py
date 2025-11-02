import os
import json

# Expand the user path for GRAPH_DATA.
GRAPH_DATA = os.path.expanduser("~/toni/datanalysis/vibe/dependency.pics-static/data")

def main():
    # List all files in the directory and print them.
    try:
        files = os.listdir(GRAPH_DATA)
        print(f"Files in directory {GRAPH_DATA}: {files}")
    except Exception as e:
        print(f"Error listing directory {GRAPH_DATA}: {e}")
        return

    block_data = []

    # Iterate over all files.
    for filename in files:
        # Process only .json files and skip the summary file.
        if filename.endswith(".json") and filename != "recent_blocks.json":
            filepath = os.path.join(GRAPH_DATA, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    # Print the file's keys (if it is a dictionary).
                    if isinstance(data, dict):
                        print(f"{filename} loaded with keys: {list(data.keys())}")
                    else:
                        print(f"{filename} did not load a dict, got type {type(data)}")
                    
                    # Check if the dict has a 'block_number' key.
                    if isinstance(data, dict) and "block_number" in data:
                        block_data.append(data)
                    else:
                        print(f"File {filename} does not contain 'block_number' key.")
            except Exception as e:
                print(f"Skipping file {filename} due to error: {e}")

    # Report how many files provided valid block data.
    print(f"Found {len(block_data)} valid JSON files with 'block_number' key.")

    # Sort by block_number descending if we have any data.
    if block_data:
        try:
            block_data_sorted = sorted(block_data, key=lambda x: int(x["block_number"]), reverse=True)
        except Exception as e:
            print(f"Error during sorting: {e}")
            block_data_sorted = []
    else:
        block_data_sorted = []

    # Only keep the highest 20 blocks.
    recent_blocks = block_data_sorted[:51]

    # Write the summary to recent_blocks.json with pretty formatting.
    summary_path = os.path.join(GRAPH_DATA, "recent_blocks.json")
    with open(summary_path, "w") as outfile:
        json.dump(recent_blocks, outfile, indent=2)

    print(f"Saved recent_blocks.json with {len(recent_blocks)} blocks.")

if __name__ == "__main__":
    main()
