#!/bin/sh
# Check if NiceTheme source is mounted
if [ -d "/mnt/nicetheme" ]; then
    echo "Installing local NiceTheme..."
    pip install -e /mnt/nicetheme
fi

# Run the application
echo "Starting Sortomatic..."
sortomatic gui /data
