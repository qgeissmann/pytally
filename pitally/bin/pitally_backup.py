from pitally.config import FTP, FTP_HOSTNAME, STATIC_VIDEO_DIR, LOGGING_LEVEL
import glob
from pitally.utils.wput_wrapper import wput
import os
import time
import logging

logging.basicConfig(level=LOGGING_LEVEL)

while True:
    logging.debug((STATIC_VIDEO_DIR, FTP))
    response = os.system("ping -c 1 -w2 " + FTP_HOSTNAME + " > /dev/null 2>&1")
    if response == 0:
        for filename in glob.iglob(STATIC_VIDEO_DIR + "**/*.h264", recursive=True):
            logging.debug(filename)
            if not os.path.basename(filename).startswith("part_"):
                o = wput(FTP, filename, delete=True)
                logging.debug(o)
    else:
        logging.debug("ftp server not reachable, waiting")
    time.sleep(60)
