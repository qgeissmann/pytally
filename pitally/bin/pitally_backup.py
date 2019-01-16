from pitally.config import FTP, STATIC_VIDEO_DIR
import glob
from pitally.utils.wput_wrapper import wput

import time

while True:
    print((STATIC_VIDEO_DIR,FTP))
    for filename in glob.iglob(STATIC_VIDEO_DIR + "**/*.h264", recursive=True):
        print(wput(FTP, filename, delete=True))
    time.sleep(60)
