import glob
import time
import os
from shutil import copyfile
import re


VIDEO_DIR = "/srv/ftp/videos/"
all_video_dir = glob.glob( VIDEO_DIR + "*/*/", recursive=True)


def append_and_delete(seed, tail_file, new_seed_name, mode = "b"):
    print((seed,tail_file))
    with open(tail_file, "r" + mode) as t, open(seed, "a" + mode) as s:
        s.write(t.read())
        print("%s\n=>>\n%s" %(t, s))
    os.remove(tail_file)
    os.rename(seed, new_seed_name)

for vd in all_video_dir:
    finished = False
    while not finished:
        try:
                seed_file = glob.glob(vd + "*_00000-*.h264")[0]
        except IndexError:
            first_file = glob.glob(vd + "*_00000.h264")
            if first_file:
                basename, ext = os.path.splitext(os.path.basename(first_file[0]))
                seed_file = os.path.join(os.path.dirname(first_file[0]), basename+"-00000.h264")
                print(seed_file)
                copyfile(first_file[0], seed_file)
        seed_basename = os.path.basename(seed_file)
        seed_dirname = os.path.dirname(seed_file)
        second_field_match = re.findall("^.*_00000-(\d{5}).h264$", seed_basename)
        next_file_id = int(second_field_match[0]) + 1
        exp_basename = re.findall("^(.*_)00000-\d{5}.h264$", seed_basename)
        next_file = os.path.join(seed_dirname, "%s%05d.h264" % (exp_basename[0], next_file_id))
        new_seed_name = re.sub("_00000-\d{5}.h264", "_00000-%05d.h264" % next_file_id, seed_basename)
        new_seed_name = os.path.join(seed_dirname,new_seed_name)
        try:
            append_and_delete(seed_file, next_file, new_seed_name)
        except FileNotFoundError as e:
            finished = True
            print(e)