import subprocess
import logging

def lftp_mirror_wrapper(server, dir, user="pi", password=""):
    lftp_command =  "set net:max-retries 1; "\
                    "open -u %s,%s %s; "\
                    "mirror -R %s  %s --Remove-source-files --include-glob='*.mp4' -c" % (user, password, server, dir, dir)
    command = 'lftp -c "%s"' % lftp_command
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        logging.error(stderr)
