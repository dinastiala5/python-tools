#!/usr/bin/env python3
import sys
import os
import time

def scan():
    images = 0
    videos = 0
    python_files = 0
    text_files = 0

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".jpg", ".png")):
                images += 1
            elif file.endswith((".mp4", ".mkv")):
                videos += 1
            elif file.endswith(".py"):
                python_files += 1
            elif file.endswith(".txt"):
                text_files += 1

    print("Scan complete!\n")
    print("Images:", images)
    print("Videos:", videos)
    print("Python files:", python_files)
    print("Text files:", text_files)


def find(filename):
    for root, dirs, files in os.walk("."):
        if filename in files:
            print("File found:", os.path.join(root, filename))
            return
    print("File not found")


def watch():
    path = "."
    print("Watching folder for changes...")

    before = dict([(f, None) for f in os.listdir(path)])

    while True:
        time.sleep(3)
        after = dict([(f, None) for f in os.listdir(path)])

        added = [f for f in after if f not in before]
        removed = [f for f in before if f not in after]

        if added:
            print("Added:", ", ".join(added))

        if removed:
            print("Removed:", ", ".join(removed))

        before = after


if len(sys.argv) < 2:
    print("Usage:")
    print("toolkit scan")
    print("toolkit find filename")
    print("toolkit watch")

else:
    command = sys.argv[1]

    if command == "scan":
        scan()

    elif command == "find":
        if len(sys.argv) < 3:
            print("Please provide a filename.")
        else:
            find(sys.argv[2])

    elif command == "watch":
        watch()

    else:
        print("Unknown command")
