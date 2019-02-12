import glob
import time
import os
import re
import logging
import tempfile
import subprocess
from pitally.utils.last_bytes_md5 import last_bytes_md5
from pitally.config import FTP_DRIVE_PATH, STATIC_VIDEO_DIR



def append_and_delete_bak(seed, tail_file, new_seed_name, mode = "b"):
    with open(tail_file, "r" + mode) as t, open(seed, "a" + mode) as s:
        s.write(t.read())
        print("%s\n=>>\n%s" %(t, s))
    os.rename(seed, new_seed_name)


def append_and_delete(seed, tail_file, new_seed_name):
    _, list_file = tempfile.mkstemp(prefix = "pitally", suffix=".txt")
    try:
        with open(list_file, 'w') as f:
            f.write("file" + " " + seed + "\n")
            f.write("file" + " " + tail_file + "\n")
            # ffmpeg -f concat -safe 0 -i mylist.txt -c copy output
        command_arg_list = ["ffmpeg",
                        "-f", "concat",
                        "-safe", "0",
                        "-i", list_file,
                        "-c", "copy",
                        "-y",
                        "'" + new_seed_name + "'"
                        ]

        command = " ".join(command_arg_list)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stream = p.communicate()
        success = p.returncode == 0
        if not success:
            logging.error(stream)
        else:
            os.remove(seed)
            os.remove(tail_file)
    finally:
        os.remove(list_file)

def check_md5_vs_name(path):
    name = os.path.basename(path)
    try:
        md5_name = re.findall("^.*_\d{5}_([0-9a-f]{32}).mp4$", name)[0]
    except IndexError:
        raise Exception("File %s does not match re pattern" % path)
    md5_actual = last_bytes_md5(path)
    return md5_name == md5_actual

def walk_and_concat(video_root_dir):
    all_video_dir = glob.glob(video_root_dir + "*/*/", recursive=True)

    for vd in all_video_dir:
        while True:
            try:
                seed_file = glob.glob(vd + "*_00000-*.mp4")[0]
            except IndexError:
                first_file = glob.glob(vd + "*_00000_*.mp4")
                if first_file:
                    check = check_md5_vs_name(first_file[0])
                    if check:
                        basename, ext = os.path.splitext(os.path.basename(first_file[0]))
                        basename_without_md5 = re.findall("^(.*_\d{5})_[0-9a-f]{32}$", basename)[0]
                        seed_file = os.path.join(os.path.dirname(first_file[0]), basename_without_md5+"-00000" + ".mp4")
                        os.rename(first_file[0], seed_file)
                    else:
                        logging.warning("Seed file got unexpected md5. Problem during upload?")
                        time.sleep(1)
                        break
                else:
                    logging.warning("No seed file in %s" % vd)
                    break
                    #raise FileNotFoundError("No seed file in %s" % vd)

            seed_basename = os.path.basename(seed_file)
            seed_dirname = os.path.dirname(seed_file)
            second_field_match = re.findall("^.*_00000-(\d{5}).mp4$", seed_basename)
            next_file_id = int(second_field_match[0]) + 1
            exp_basename = re.findall("^(.*_)00000-\d{5}.mp4$", seed_basename)
            next_file_pattern = os.path.join(seed_dirname, "%s%05d_*.mp4" % (exp_basename[0], next_file_id))

            try:
                next_file = glob.glob(next_file_pattern)[0]

            except IndexError:
                logging.debug("next file not present. finished")
                break

            check = check_md5_vs_name(next_file)

            if check:
                new_seed_name = re.sub("_00000-\d{5}.mp4", "_00000-%05d.mp4" % next_file_id, seed_basename)
                if new_seed_name == seed_basename:
                    raise Exception("Cannot generate new seed name")

                new_seed_name = os.path.join(seed_dirname,new_seed_name)
                append_and_delete(seed_file, next_file, new_seed_name)
            else:
                logging.warning("Seed file got unexpected md5. Problem during upload?")
                time.sleep(5)
                break


if __name__ == "__main__":
    video_root_dir = "/".join([FTP_DRIVE_PATH, STATIC_VIDEO_DIR])
    while True:
        walk_and_concat(video_root_dir)
        time.sleep(30)

