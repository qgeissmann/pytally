import os
import re
import subprocess
import logging
import tempfile
from pitally.utils import last_bytes_md5


def h264_to_mp4(input, output=None, remove_h264=False, add_md5_suffix=True):
    basename = os.path.splitext(os.path.basename(input))[0]
    #todo forbid _ in prefix, in client
    match = re.search(r"(?P<datetime>.*)_(?P<device>.*)_(?P<prefix>.*)_(?P<w>\d+)x(?P<h>\d+)@(?P<fps>\d+)_(?P<id>\d+)", basename)
    groups = match.groupdict()
    _, tmp_file = tempfile.mkstemp(suffix=".mp4", prefix="pitally_")
    try:
        command_arg_list = ["ffmpeg",
                            "-r", groups["fps"],
                            "-i", "'" + 'file:' + input + "'",
                            "-vcodec", "copy",
                            "-metadata", "artist=" + "'" + groups["device"] + "'",
                            "-metadata", "date=" + "'" + groups["datetime"] + "'",
                            "-metadata", "show=" + "'" + groups["datetime"] + "_" + groups["prefix"] + "'",
                            "-metadata", "episode_id=" + "'" + groups["id"] + "'",
                            "-y", "'" + tmp_file + "'",
                   #         "-loglevel",  "panic"
                            ]
        command = " ".join(command_arg_list)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stream = p.communicate()
        success = p.returncode == 0
        if not success:
            logging.error(stream)
            raise Exception("FFMPEG failed!")

        if output is None:
            suffix = ""
            if add_md5_suffix:
                suffix = last_bytes_md5(tmp_file)
            output = os.path.join(os.path.dirname(input), basename + "_" + suffix + ".mp4")
        os.rename(tmp_file, output)

        if remove_h264:
            os.remove(input)
    finally:
        try:
            os.remove(tmp_file)
        except FileNotFoundError:
            pass

    return output
