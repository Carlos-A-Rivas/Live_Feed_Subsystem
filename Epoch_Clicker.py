#!/usr/bin/env python3

import time
import csv
from pynput.keyboard import Listener, Key

# CSV filename to store Enter key press times
CSV_FILE = 'enter_times.csv'

# Initialize CSV file with header if it doesn't exist
try:
    with open(CSV_FILE, 'r', newline='') as f:
        pass
except FileNotFoundError:
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['epoch_time'])


def on_press(key):
    """
    Callback for keyboard key press events. Prints every key and logs Enter presses.
    """
    print(f"Key pressed: {key}")  # Debug: show all key presses
    if key == Key.enter:
        epoch_time = time.time()
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([epoch_time])
        print(f"Recorded Enter at {epoch_time}")


def on_release(key):
    """
    Stop listener when Escape is pressed.
    """
    if key == Key.esc:
        print("Escape pressed, exiting.")
        return False


if __name__ == '__main__':
    print(f"Logging Enter key presses to '{CSV_FILE}'. Press ESC to stop.")
    # Start listening to keyboard events
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
