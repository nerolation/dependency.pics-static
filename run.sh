#!/bin/bash
# run.sh
# This script ensures an SSH agent is running and that your new deploy key is loaded,
# navigates to your dependency.pics-static repository,
# runs "sync_data.py" and "create_recent_block.py" using your virtual environment,
# and then stages, commits, and pushes changes from the "data", "graphs", and "gantt" folders.

# Check if an SSH agent is running; if not, start it.
if [ -z "$SSH_AUTH_SOCK" ]; then
    echo "No SSH agent detected. Starting ssh-agent..."
    eval "$(ssh-agent -s)" || { echo "Failed to start ssh-agent."; exit 1; }
fi

# Check if your deploy key is already loaded; if not, add it.
if ! ssh-add -l >/dev/null 2>&1; then
    echo "No SSH keys loaded. Adding your deploy key (~/.ssh/my_repo_deploy_key) to the agent..."
    ssh-add ~/.ssh/my_repo_deploy_key || { echo "Failed to add SSH key. Exiting."; exit 1; }
fi

# Change to the repository directory.
cd ~/toni/datanalysis/vibe/dependency.pics-static || { echo "Directory not found!"; exit 1; }

# Run sync_data.py using your virtual environment.
./venv/bin/python3 sync_data.py
if [ $? -ne 0 ]; then
    echo "sync_data.py failed."
    exit 1
fi

# Run create_recent_block.py using your virtual environment.
./venv/bin/python3 create_recent_block.py
if [ $? -ne 0 ]; then
    echo "create_recent_block.py failed."
    exit 1
fi

date -u "+%Y-%m-%d %H:%M:%S UTC" > last-updated.txt
echo "last-updated.txt updated."

# Stage changes in the folders "data", "graphs", and "gantt".
git add data graphs gantt last-updated.txt

# Create a commit with an automated message.
git commit -m "Automated update: ran sync_data and create_recent_block scripts"

# Push the commit to GitHub.
git push
