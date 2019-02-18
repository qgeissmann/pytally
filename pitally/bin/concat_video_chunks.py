#! /usr/bin/python

import glob
from pitally.config import FTP_DRIVE_PATH, STATIC_VIDEO_DIR
from pitally.utils.concat_tools import process_one_dir, clean_up_old_contigs
from optparse import OptionParser
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-c", "--cleanup", dest="cleanup", default=False, help="cleanup old videos",
                      action="store_true")
    (options, args) = parser.parse_args()
    option_dict = vars(options)
    cleanup = option_dict["cleanup"]

    video_root_dir = "/".join([FTP_DRIVE_PATH, STATIC_VIDEO_DIR])
    all_video_dir = glob.glob(video_root_dir + "*/*/", recursive=True)

    for vd in all_video_dir:
        if cleanup:
            clean_up_old_contigs(vd)
        process_one_dir(vd)

# on the server sid, to list all possible seeds one can do:
#  lftp -e "find /;quit" "ftp://localhost" | grep -e "^.*_0\{5\}-[0-9]\{5\}\.mp4$"
# then serve the last ones per dir in a dir
# clean up all seeds / backup etc e.g. once a week during night