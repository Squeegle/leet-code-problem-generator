#!/bin/bash

# Exit on error
set -e

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if problems were generated today
if [ -f "$SCRIPT_DIR/problem_tracker.json" ]; then
    LAST_GENERATED=$(grep -o '"last_generated": "[^"]*"' "$SCRIPT_DIR/problem_tracker.json" | cut -d'"' -f4)
    TODAY=$(date +%Y-%m-%d)
    
    if [ "$LAST_GENERATED" = "$TODAY" ]; then
        echo "Problems already generated today. Skipping."
        exit 0
    fi
fi

# Generate new problems
echo "Generating new LeetCode problems..."
python3 "$SCRIPT_DIR/generate_leetcode_problems.py" 