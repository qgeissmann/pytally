# non python deps:
wput tree ipython3 tcpdump nmap
# setup ftp server

* install bftpd
* enable bftpd.socket
* comment out `DENY_LOGIN="Anonymous login disabled."`
* set `ALLOWCOMMAND_DELE="yes"`

# push to the server
* install wput

```
import subprocess
target = "/tmp/test1.txt"
remote ="ftp://localhost"
    command_arg_list=  ["wput",
                        target,
                        remote
                        ]
    p = subprocess.Popen(command_arg_list,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

```