import os
import re
import subprocess
import logging

def h264_to_mp4(input, output=None, remove_h264=False):
    basename = os.path.splitext(os.path.basename(input))[0]
    # eg '2019-01-30T05:12:36(UTC)_pitally-dbee1b_my-video_1640x1232@25_00008.h264'
    #todo forbic _ in prefix, in client
    #basename = '2019-01-30T05:12:36(UTC)_pitally-dbee1b_my-video_1640x1232@25_00008.h264'
    match = re.search(r"(?P<datetime>.*)_(?P<device>.*)_(?P<prefix>.*)_(?P<w>\d+)x(?P<h>\d+)@(?P<fps>\d+)_(?P<id>\d+)", basename)
    groups = match.groupdict()
    # from @ethoscope ffmpeg -r $fps -i $TMP_FILE -vcodec copy -y $prefix.mp4 -loglevel panic

    if output is None:
        # output_basename = groups["datetime"] + "_" +\
        #                  groups["device"] + "_" +\
        #                  groups["prefix"] + "_" +\
        #                  groups["w"] + "x" + groups["h"] + "@" + groups["fps"] + ".mp4"
        output = os.path.join(os.path.dirname(input), basename + ".mp4")


    command_arg_list = ["ffmpeg",
                        "-r", groups["fps"],
                        "-i", "'" + 'file:' + input + "'",
                        "-vcodec", "copy",
                        "-metadata", "artist=" + "'" + groups["device"]+ "'",
                        "-metadata", "date=" + "'" + groups["datetime"] + "'",
                        "-metadata", "show=" + "'" + groups["datetime"]+ "_" + groups["prefix"]+ "'",
                        "-metadata", "episode_id=" + "'" + groups["id"]+ "'",
                        "-y", "'" + output + "'",
               #         "-loglevel",  "panic"
                        ]
    command = " ".join(command_arg_list)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stream = p.communicate()
    success = p.returncode == 0
    if not success:
        logging.error(stream)
        try:
            os.remove(output)
        except FileNotFoundError:
            pass
        return None
    if remove_h264:
        os.remove(input)
    return output
