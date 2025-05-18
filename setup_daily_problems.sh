#!/bin/bash

# Exit on error
set -e

# Function to print error messages
error() {
    echo "Error: $1" >&2
    exit 1
}

# Function to print success messages
success() {
    echo "Success: $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed. Please install Python 3 first."
fi

# Check if required Python packages are installed
if ! python3 -c "import requests" &> /dev/null; then
    error "Python package 'requests' is not installed. Please run 'pip install -r requirements.txt' first."
fi

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if we're in the correct directory
if [ ! -f "$SCRIPT_DIR/generate_leetcode_problems.py" ]; then
    error "Could not find generate_leetcode_problems.py in $SCRIPT_DIR"
fi

# Make check_and_generate.sh executable
chmod +x "$SCRIPT_DIR/check_and_generate.sh"

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/leetcode-problems.service"
sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=LeetCode Daily Problems Generator
After=network.target

[Service]
Type=oneshot
ExecStart=$SCRIPT_DIR/check_and_generate.sh
User=$USER
WorkingDirectory=$SCRIPT_DIR

[Install]
WantedBy=multi-user.target
EOF

# Create a temporary file for the crontab
TEMP_CRON=$(mktemp) || error "Failed to create temporary file"

# Add the current crontab to the temporary file
if ! crontab -l > "$TEMP_CRON" 2>/dev/null; then
    echo "# LeetCode Daily Problems" > "$TEMP_CRON"
fi

# Check if the cron job already exists
if grep -q "generate_leetcode_problems.py" "$TEMP_CRON"; then
    success "Cron job already exists. Skipping creation."
else
    # Add our new cron job (runs at 8 AM every day)
    echo "0 8 * * * cd $SCRIPT_DIR && python3 generate_leetcode_problems.py >> $SCRIPT_DIR/leetcode_problems.log 2>&1" >> "$TEMP_CRON"

    # Install the new crontab
    if ! crontab "$TEMP_CRON"; then
        rm "$TEMP_CRON"
        error "Failed to install crontab"
    fi
fi

# Remove the temporary file
rm "$TEMP_CRON"

# Create a log file
touch "$SCRIPT_DIR/leetcode_problems.log"

# Enable and start the systemd service
sudo systemctl daemon-reload
sudo systemctl enable leetcode-problems.service
sudo systemctl start leetcode-problems.service

success "Daily LeetCode problems generation has been scheduled for 8 AM every day."
success "Problems will also be generated on system startup if not already generated that day."
success "The script will be run from: $SCRIPT_DIR"
success "Logs will be written to: $SCRIPT_DIR/leetcode_problems.log"
echo ""
echo "To check the status of your cron jobs, run: crontab -l"
echo "To view the logs, run: tail -f $SCRIPT_DIR/leetcode_problems.log"
echo "To check the service status, run: systemctl status leetcode-problems.service" 