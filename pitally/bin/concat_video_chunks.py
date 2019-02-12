import glob
import time
import os
from shutil import copyfile
import re
import logging
import tempfile
import subprocess
from pitally.utils.last_bytes_md5 import last_bytes_md5


VIDEO_DIR = "/home/quentin/Desktop/videos/"
all_video_dir = glob.glob( VIDEO_DIR + "*/*/", recursive=True)


def append_and_delete_bak(seed, tail_file, new_seed_name, mode = "b"):
    print((seed,tail_file))
    with open(tail_file, "r" + mode) as t, open(seed, "a" + mode) as s:
        s.write(t.read())
        print("%s\n=>>\n%s" %(t, s))
    #os.remove(tail_file)
    os.rename(seed, new_seed_name)

def append_and_delete(seed, tail_file, new_seed_name):
    list = tempfile.mkstemp(prefix = "pitally", suffix=".txt")
    try:
        with open(list, 'w') as f:
            f.write("file" + " " + seed)
            f.write("file" + " " + tail_file)
            # ffmpeg -f concat -safe 0 -i mylist.txt -c copy output
        command_arg_list = ["ffmpeg",
                        "-f", "concat",
                        "-safe", "0",
                        "-i", f,
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
    finally:
        os.remove(list)

def check_md5_vs_name(name):
    md5_name = re.findall("^.*_\d{5}_([0-9a-f]{32}).h264$", name)[0]
    md5_actual = last_bytes_md5(name)
    return md5_name == md5_actual

for vd in all_video_dir:
    finished = False
    # todo, find any h264 that has no mp4 mirror (makefile?)
    # ffmpeg  to convert them to mp4
    # instead of apending, we can use ffmpeg concat!
    while not finished:
        try:
                seed_file = glob.glob(vd + "*_00000-*.mp4")[0]
        except IndexError:
            first_file = glob.glob(vd + "*_00000_*.mp4")
            if first_file:
                check = check_md5_vs_name(first_file[0])
                if check:
                    basename, ext = os.path.splitext(os.path.basename(first_file[0]))
                    seed_file = os.path.join(os.path.dirname(first_file[0]), basename+"-00000" + ".h264")
                    copyfile(first_file[0], seed_file)
                else:
                    logging.warning("Seed file got unexpected md5. Problem during upload?")
                    time.sleep(5)
                    continue

        seed_basename = os.path.basename(seed_file)
        seed_dirname = os.path.dirname(seed_file)
        second_field_match = re.findall("^.*_00000-(\d{5}).h264$", seed_basename)
        next_file_id = int(second_field_match[0]) + 1
        exp_basename = re.findall("^(.*_)00000-\d{5}.h264$", seed_basename)
        next_file_pattern = os.path.join(seed_dirname, "%s%05d_*.h264" % (exp_basename[0], next_file_id))

        try:
            next_file = glob.glob(next_file_pattern)[0]
        except IndexError:
            logging.debug("next file not present. finished")
            finished = True
            continue

        check = check_md5_vs_name(next_file)
        if check:
            new_seed_name = re.sub("_00000-\d{5}.h264", "_00000-%05d.h264" % next_file_id, seed_basename)
            new_seed_name = os.path.join(seed_dirname,new_seed_name)
            append_and_delete(seed_file, next_file, new_seed_name)
