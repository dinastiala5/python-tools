import os
import time

path = "."

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
