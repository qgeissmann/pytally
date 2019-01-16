from pitally.config import FTP, STATIC_VIDEO_DIR
import glob
from pitally.utils.wput_wrapper import wput

import time
while True:

    for filename in sorted(glob.iglob(STATIC_VIDEO_DIR + "**/*.h264", recursive=True)):
        print(wput(FTP, filename))
    time.sleep(60)
