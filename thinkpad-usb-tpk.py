#!/usr/bin/env python3

"""
thinkpad-usb-tpk: ThinkPad USB Keyboard TrackPoint Configuration Tool

This script configures the TrackPoint settings for the Lenovo ThinkPad Compact USB Keyboard.
It adjusts the TrackPoint speed and sensitivity, and disables the center click.

Usage: python3 thinkpad-usb-tpk.py

Requirements:
- xinput command-line tool
- X Window System
"""

import subprocess
import re
import sys
import shutil

def check_xinput():
    """Check if xinput is installed and accessible."""
    if shutil.which("xinput") is None:
        print("Error: 'xinput' command not found. Please install xinput and try again.")
        sys.exit(1)
    print("xinput is installed and accessible.")

def run_command(command):
    """Execute a command and return its output."""
    print(f"Executing: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Output:\n{result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output:\n{e.stderr.strip()}")
        return None

def get_device_id():
    """Get the device ID for the ThinkPad TrackPoint keyboard."""
    xinput_output = run_command(["xinput"])
    if xinput_output is None:
        return None

    device_lines = [line for line in xinput_output.split('\n')
                    if "Lenovo ThinkPad Compact USB Keyboard with TrackPoint" in line]

    for line in device_lines:
        device_id = re.search(r'id=(\d+)', line)
        if device_id:
            props = run_command(["xinput", "list-props", device_id.group(1)])
            if props and "libinput Accel Speed" in props:
                return device_id.group(1)

    return None

def set_trackpoint_properties(device_id):
    """Set TrackPoint properties for the given device ID."""
    # Set TrackPoint Speed
    run_command(["xinput", "set-prop", device_id, "libinput Accel Speed", "0.5"])

    # Set TrackPoint Sensitivity
    run_command(["xinput", "set-prop", device_id, "Coordinate Transformation Matrix",
                 "1", "0", "0", "0", "1", "0", "0", "0", "0.5"])

    # Disable Center Click
    run_command(["xinput", "set-button-map", device_id, "1", "0", "3", "4", "5", "6", "7"])

def main():
    print("thinkpad-usb-tpk: Configuring ThinkPad USB Keyboard TrackPoint")

    # Check if xinput is installed
    check_xinput()

    device_id = get_device_id()
    if device_id:
        print(f"ThinkPad TrackPoint device found with ID: {device_id}")
        set_trackpoint_properties(device_id)
        print("TrackPoint properties set successfully")
    else:
        print("Error: ThinkPad TrackPoint device not found")
        sys.exit(1)

if __name__ == "__main__":
    main()
