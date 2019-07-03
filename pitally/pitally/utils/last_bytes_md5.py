import subprocess
import os


def last_bytes_md5(file, n=1024):
    if not os.path.exists(file):
        raise FileNotFoundError("%s does not exist" % file)

    command = "tail  %s -c %i | md5sum" % (file, n)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = p.communicate()
    return str(out[0:32], 'utf-8')
