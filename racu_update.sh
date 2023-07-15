#!/bin/bash

# Change to the project directory
# cd .

# Stash any local changes
# git stash

# Fetch the latest changes from the remote repository
git fetch

# Get the current branch
current_branch=$(git symbolic-ref --short HEAD)

# Check if the branch is behind the remote branch
if [ -n "$(git rev-list --left-only --count origin/$current_branch...HEAD)" ]; then
    # Pull the latest changes
    git pull

    # Check if there are any merge conflicts
    if [ -n "$(git ls-files --unmerged)" ]; then
        echo "Merge conflicts detected. Please resolve them manually."
        exit 1
    fi
else
    echo "No new changes found in the remote repository."
fi

# Restart the pm2 process
pm2 restart Racu.Core 1>/dev/null 2>&1

# Check the pm2 process status
pm2_status=$(pm2 jlist | jq -r '.[] | select(.name == "Racu.Core") | .pm2_env.status')

if [ "$pm2_status" = "online" ]; then
    echo "Process restarted successfully."
else
    echo "Failed to restart the process. Check the pm2 logs for more information."
    exit 1
fi

exit 0
