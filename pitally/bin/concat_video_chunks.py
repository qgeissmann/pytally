import glob
import time
import os
import re
import logging
import tempfile
import subprocess
from pitally.utils.last_bytes_md5 import last_bytes_md5
from pitally.config import FTP_DRIVE_PATH, STATIC_VIDEO_DIR

class BadMatch(Exception):
    pass

def merge_and_delete(file_list, output):
    _, list_file = tempfile.mkstemp(prefix = "pitally", suffix=".txt")
    try:
        with open(list_file, 'w') as f:
            for v in file_list:
                f.write("file" + " " + v + "\n")
            command_arg_list = ["ffmpeg",
                        "-f", "concat",
                        "-safe", "0",
                        "-i", list_file,
                        "-c", "copy",
                        "-y",
                        "'" + output + "'"
                        ]

        command = " ".join(command_arg_list)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stream = p.communicate()
        success = p.returncode == 0
        if not success:
            logging.error(stream)
        else:
            for v in file_list:
                os.remove(v)
    finally:
        os.remove(list_file)

def check_md5_vs_name(path):
    name = os.path.basename(path)
    try:
        md5_name = re.findall("^.*_\d{5}_([0-9a-f]{32}).mp4$", name)[0]
    except IndexError:
        raise BadMatch("File %s does not match re pattern" % path)
    md5_actual = last_bytes_md5(path)
    return md5_name == md5_actual
#
# def walk_and_concat(video_root_dir):
#     all_video_dir = glob.glob(video_root_dir + "*/*/", recursive=True)
#
#     for vd in all_video_dir:
#         while True:
#             try:
#                 seed_file = glob.glob(vd + "*_00000-*.mp4")[0]
#             except IndexError:
#                 first_file = glob.glob(vd + "*_00000_*.mp4")
#                 if first_file:
#                     check = check_md5_vs_name(first_file[0])
#                     if check:
#                         basename, ext = os.path.splitext(os.path.basename(first_file[0]))
#                         basename_without_md5 = re.findall("^(.*_\d{5})_[0-9a-f]{32}$", basename)[0]
#                         seed_file = os.path.join(os.path.dirname(first_file[0]), basename_without_md5+"-00000" + ".mp4")
#                         os.rename(first_file[0], seed_file)
#                     else:
#                         logging.warning("Seed file got unexpected md5 %s. Problem during upload?" % first_file[0])
#                         time.sleep(1)
#                         break
#                 else:
#                     logging.warning("No seed file in %s" % vd)
#                     break
#                     #raise FileNotFoundError("No seed file in %s" % vd)
#
#             seed_basename = os.path.basename(seed_file)
#             seed_dirname = os.path.dirname(seed_file)
#             second_field_match = re.findall("^.*_00000-(\d{5}).mp4$", seed_basename)
#             next_file_id = int(second_field_match[0]) + 1
#             exp_basename = re.findall("^(.*_)00000-\d{5}.mp4$", seed_basename)
#             next_file_pattern = os.path.join(seed_dirname, "%s%05d_*.mp4" % (exp_basename[0], next_file_id))
#
#             try:
#                 next_file = glob.glob(next_file_pattern)[0]
#
#             except IndexError:
#                 logging.debug("next file not present. finished")
#                 break
#
#             check = check_md5_vs_name(next_file)
#
#             if check:
#                 new_seed_name = re.sub("_00000-\d{5}.mp4", "_00000-%05d.mp4" % next_file_id, seed_basename)
#                 if new_seed_name == seed_basename:
#                     raise Exception("Cannot generate new seed name")
#
#                 new_seed_name = os.path.join(seed_dirname,new_seed_name)
#                 append_and_delete(seed_file, next_file, new_seed_name)
#             else:
#                 logging.warning("Seed file got unexpected md5 %s. Problem during upload?" % next_file)
#                 time.sleep(5)
#                 break

def validate_and_rename(dir):
    for vid in glob.glob(dir + "*.mp4"):
        try:
            if check_md5_vs_name(vid):
                basename = os.path.basename(vid)
                # basename = "2019-02-16T17-05-27-UTC_pitally-d94abf_my-video_1640x1232@25_00001_7f560f53e03ea59063c58e5ff2b5f4e7.mp4"
                match = re.match("^(?P<constant>.*)_(?P<id>\d{5})_(?P<md5>[0-9a-f]{32})\.mp4$", basename)
                match_dict = match.groupdict()
                new_basename = "%s_%s-%s.mp4" % (match_dict["constant"], match_dict["id"], match_dict["id"])
                new_path = os.path.join(os.path.dirname(vid), new_basename)
                logging.info( "Checked %s. renaming to %s" %(vid, new_path))
                os.rename(vid, new_path)
        except BadMatch:
            continue

def find_contiguous_vids(dir):
    all_valid = []
    for vid in glob.glob(dir + "*.mp4"):
        basename = os.path.basename(vid)
        # basename = "2019-02-16T17-05-27-UTC_pitally-d94abf_my-video_1640x1232@25_00001_7f560f53e03ea59063c58e5ff2b5f4e7.mp4"
        match = re.match("^(?P<constant>.*)_(?P<start>\d{5})-(?P<end>\d{5})\.mp4$", basename)
        if match:
            match_dict = match.groupdict()
            start = int(match_dict["start"])
            end = int(match_dict["end"])
            all_valid.append({"start":start, "end":end, "path": vid})
    all_valid.sort(key=lambda x: x["start"])
    logging.debug(all_valid)
    contigs = []
    new_contig = []
    for i, vid in enumerate(all_valid):
        path = vid["path"]
        # while True:
        logging.debug(path)
        if len(new_contig) == 0:
            new_contig.append(vid)
            logging.debug("starting new contig")
        else:
            current_start = vid["start"]
            previous_end = all_valid[i-1]["end"]
            logging.debug((current_start, previous_end))
            if current_start - previous_end == 1:
                new_contig.append(vid)
                logging.debug("could be appended to previous")
            else :

                logging.debug("could be NOT be appended to previous, starting new one")
                contigs.append(new_contig)
                new_contig = [vid]

    contigs.append(new_contig)
    return contigs
if __name__ == "__main__":
    while True:
        video_root_dir = "/".join([FTP_DRIVE_PATH, STATIC_VIDEO_DIR])
        all_video_dir = glob.glob(video_root_dir + "*/*/", recursive=True)
        for vd in all_video_dir:
            validate_and_rename(vd)
            contigs = find_contiguous_vids(vd)
            for c in contigs:
                #todo check all constant names are equal
                match = re.match("^(?P<constant>.*)_(?P<start>\d{5})-(?P<end>\d{5})\.mp4$", os.path.basename(c[0]["path"]))
                match_dict = match.groupdict()

                concat_output_basename  = "%s_%05d_%05d.mp4" % (match_dict["constant"], c[0]["start"], c[-1]["end"])
                concat_output_path = os.path.join(vd, concat_output_basename)
                logging.debug("Making %s" % concat_output_path)
                merge_and_delete([i["path"] for i in c], concat_output_path)


    #     validate_and_rename(video_root_dir)
    #     walk_and_concat(video_root_dir)
        time.sleep(30)

