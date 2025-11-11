#!/bin/bash

##################################################################################################
#
# Find and delete all remote git branches that are fully merged into develop, master or main
#
##################################################################################################

# Prune stale remote tracking branches
echo "Pruning stale remote tracking branches..."
git fetch origin --prune

# Get list of stale branches (merged into develop, master, or main)
branches=$(
  {
    git branch -r --merged origin/develop --format="%(refname:short)" 2>/dev/null
    git branch -r --merged origin/master --format="%(refname:short)" 2>/dev/null
    git branch -r --merged origin/main --format="%(refname:short)" 2>/dev/null
  } | grep -v -E "HEAD|^origin$|origin/develop$|origin/master$|origin/main$" | sort -u
)

if [ -z "$branches" ]; then
  echo "No stale branches found."
  exit 0
fi

echo "Found the following stale branches:"
echo "$branches"
echo ""

count=0
deleted=0

# Read from file descriptor 3 to preserve stdin
while IFS= read -r branch <&3; do
  ((count++))
  read -p "Delete '$branch'? (y/n): " confirm

  if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
    # Remove origin/ prefix to get the actual branch name
    branch_name=${branch#origin/}
    git push origin --delete "$branch_name"
    if [ $? -eq 0 ]; then
      echo "✓ Deleted '$branch'"
      ((deleted++))
    else
      echo "✗ Failed to delete '$branch'"
    fi
  else
    echo "Skipped '$branch'"
  fi
  echo ""
done 3<<< "$branches"

echo "Summary: Deleted $deleted out of $count branches."