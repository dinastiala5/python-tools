import os

images = 0
videos = 0
python_files = 0
text_files = 0

for root, dirs, files in os.walk("."):
    for file in files:

        if file.endswith(".jpg") or file.endswith(".png"):
            images += 1

        elif file.endswith(".mp4"):
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
