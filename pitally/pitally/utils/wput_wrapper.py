import subprocess
import os
import re

def wput(remote, file, delete = False):
    command_arg_list=  ["wput",
                        "'" + file + "'",
                        "'" + remote + "'",
                          "--tries 3",
                        #
                       ]
    if delete:
        command_arg_list.append("-R")

    command = " ".join(command_arg_list)
    p = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    #fixme
    # also say skipp if connection refused!!!
    # use -R
    # if delete and len(re.findall("Skipp.*file", stdout.decode('utf-8'))) > 0:
    #     os.remove(file)
    #     print("Removing " + file)
    return stdout

#b"Error: File `/tmp/test1.txt' does not exist. Don't know what to do about this URL.\nNothing done. Try `wput --help'.\n"
#b"--19:32:15-- `/tmp/test1.txt'\n    => ftp://anonymous:xxxxx@127.0.0.1:21//tmp/test1.txt\nConnecting to 127.0.0.1:21... connected! \nLogging in as anonymous ... Logged in!\nLength: 0\n    0K \n19:32:15 (test1.txt) - ` --.--' [0]\n\nFINISHED --19:32:15--\nTransfered 0 bytes in 1 file at  --.--\n"
#b"--19:32:47-- `/tmp/test1.txt'\n    => ftp://anonymous:xxxxx@127.0.0.1:21//tmp/test1.txt\nConnecting to 127.0.0.1:21... connected! \nLogging in as anonymous ... Logged in!\n-- Skipping file: /tmp/test1.txt\nFINISHED --19:32:47--\nSkipped 1 file.\n"
#Skipping this URL.\nError: the url `ftp://localhostw' could not be parsed\nFINISHED --19:44:07--\nTransmission of 1 file failed.
