import os
import re
import logging
import tempfile
import subprocess
import pwd
import grp
import glob

from pitally import last_bytes_md5

class BadMatch(Exception):
    pass

def merge_and_delete(file_list, output):
    _, list_txt_file = tempfile.mkstemp(prefix = "pitally", suffix=".txt")
    tmp_out = os.path.join(os.path.dirname(output), ".tmp_" + os.path.basename(output))
    try:
        with open(list_txt_file, 'w') as f:
            for v in file_list:
                f.write("file" + " " + v + "\n")
            command_arg_list = ["ffmpeg",
                        "-f", "concat",
                        "-safe", "0",
                        "-i", list_txt_file,
                        "-c", "copy",
                        "-y",
                        "'" + tmp_out + "'"
                        ]
        command = " ".join(command_arg_list)
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stream = p.communicate()
        except Exception as e:
            logging.error("Exception while merging videos. Attempting to delete temporary file")
            try:
                os.remove(tmp_out)
            except FileNotFoundError:
                pass
            raise e

        success = p.returncode == 0
        logging.info("Making %s" % output)

        if not success:
            logging.error(stream)
        else:
            #todo dopy owner from previous files instead of hardcoding
            uid = pwd.getpwnam("ftp").pw_uid
            gid = grp.getgrnam("ftp").gr_gid
            os.rename(tmp_out, output)
            os.chown(output, uid=uid, gid=gid)
            for f in file_list[1:]:
                os.remove(f)

    finally:
        os.remove(list_txt_file)

def check_md5_vs_name(path):
    name = os.path.basename(path)
    try:
        md5_name = re.findall("^.*_\d{5}_([0-9a-f]{32}).mp4$", name)[0]
    except IndexError:
        raise BadMatch("File %s does not match re pattern" % path)
    md5_actual = last_bytes_md5(path)
    return md5_name == md5_actual

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
def clean_up_old_contigs(dir):
    all_valid = []
    for vid in glob.glob(dir + "*.mp4"):
        basename = os.path.basename(vid)
        match = re.match("^(?P<constant>.*)_(?P<start>\d{5})-(?P<end>\d{5})\.mp4$", basename)
        if match:
            match_dict = match.groupdict()
            start = int(match_dict["start"])
            end = int(match_dict["end"])
            all_valid.append({"start": start, "end": end, "path": vid})
    if len(all_valid) < 2:
        return None
    all_valid.sort(key=lambda x: 1e6 * x["start"] - x["end"])

    to_delete = [v for v in all_valid[1:] if v["start"] == 0]
    for d in to_delete:
        assert d["start"] == 0 and d["end"] < all_valid[0]["end"]
        os.remove(d["path"])

def find_next_chunks(dir):

    all_valid = []
    for vid in glob.glob(dir + "*.mp4"):
        basename = os.path.basename(vid)
        match = re.match("^(?P<constant>.*)_(?P<start>\d{5})-(?P<end>\d{5})\.mp4$", basename)
        if match:
            match_dict = match.groupdict()
            start = int(match_dict["start"])
            end = int(match_dict["end"])
            all_valid.append({"start": start, "end": end, "path": vid})

    if len(all_valid) < 2:
        return None
    all_valid.sort(key=lambda x: 1e6 * x["start"] + x["end"])
    # at this stage, there coulds be several videos starting at 0 that have not been deleted yet.
    # we want to keep the longest and discard the others. Thanks to the sorting, it should be the last ot the 0 starting
    last_zero_starting = 0
    for i, vid in enumerate(all_valid[1:]):
        if vid["start"] > 0:
            last_zero_starting = i
            break
    all_valid = all_valid[last_zero_starting:]
    seed = all_valid.pop(0)

    if seed["start"] != 0:
        logging.warning("First video missing in %s. Skipping" % dir)
        return None
    # define (only) the first contig
    contigs = [seed]
    while True:
        if not all_valid:
            break

        first = all_valid.pop(0)
        if contigs[-1]["end"] >= first["start"]:
            continue
        if contigs[-1]["end"] + 1 == first["start"]:
            contigs.append(first)
        else:
            break
    if len(contigs) == 1:
        return None
    return contigs

def process_one_dir(dir):
    validate_and_rename(dir)
    contigs = find_next_chunks(dir)
    if contigs:
        match = re.match("^(?P<constant>.*)_(?P<start>\d{5})-(?P<end>\d{5})\.mp4$",
                         os.path.basename(contigs[0]["path"]))
        match_dict = match.groupdict()
        #
        concat_output_basename = "%s_%05d-%05d.mp4" % (match_dict["constant"], contigs[0]["start"], contigs[-1]["end"])
        concat_output_path = os.path.join(dir, concat_output_basename)
        logging.debug("Making %s" % concat_output_path)
        merge_and_delete([i["path"] for i in contigs], concat_output_path)

