#!/bin/bash
# uninstall_launchagent.sh
# Removes the LaunchAgent for AI Voice Dictation

PLIST_NAME="com.user.aidictation.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "Uninstalling LaunchAgent for AI Voice Dictation..."

# Check if plist exists
if [ ! -f "$PLIST_DEST" ]; then
    echo "LaunchAgent not installed (plist not found at $PLIST_DEST)"
    exit 0
fi

# Stop the agent if running
echo "Stopping agent..."
launchctl stop com.user.aidictation 2>/dev/null

# Unload the agent
echo "Unloading agent..."
launchctl unload "$PLIST_DEST" 2>/dev/null

# Remove the plist
echo "Removing plist..."
rm "$PLIST_DEST"

# Clean up log files (optional)
echo "Cleaning up log files..."
rm -f /tmp/aidictation.out.log /tmp/aidictation.err.log

echo "Done! AI Voice Dictation will no longer start at login."
