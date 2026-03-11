import os

filename = input("Enter file name to search: ")

found = False

for root, dirs, files in os.walk("."):
    if filename in files:
        print("File found in:", os.path.join(root, filename))
        found = True

if not found:
    print("File not found")
