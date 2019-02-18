from pitally.config import FTP, FTP_HOSTNAME, STATIC_VIDEO_DIR, LOGGING_LEVEL, FTP_PASSWORD, FTP_USER
import glob
from pitally.utils.wput_wrapper import wput
from pitally.utils.lftp_mirror_wrapper import lftp_mirror_wrapper
from pitally.utils.h246_to_mp4 import h264_to_mp4
import os
import time
import logging

# logging.basicConfig(level=LOGGING_LEVEL)

while True:
    logging.debug((STATIC_VIDEO_DIR, FTP))

    # screen all h264 to convert them to mp4
    for filename in glob.iglob(STATIC_VIDEO_DIR + "**/*.h264", recursive=True):
        if not os.path.basename(filename).startswith("part_"):
            o = h264_to_mp4(filename, remove_h264=True)
            logging.debug(o)
    #ping the ftp server and upload the mp4 files to it
    response = os.system("ping -c 1 -w2 " + FTP_HOSTNAME + " > /dev/null 2>&1")
    if response == 0:
        lftp_mirror_wrapper(FTP, STATIC_VIDEO_DIR, FTP_USER, FTP_PASSWORD)
    else:
        logging.warning("ftp server not reachable, waiting")
    time.sleep(60)
