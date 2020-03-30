"""
Little program to print directory size every 5 seconds to monitor populating of the cache
"""
import os
from time import sleep

while True:
    total_size = 0
    start_path = '../cache/cache'
    for path, dirs, files in os.walk(start_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    print(f"Directory size: {total_size/1000000} mb")
    sleep(5)
