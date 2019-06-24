import netifaces
from subprocess import call
import socket


def file_in_dir_r(file, dir):
    file_dir_path = os.path.dirname(file).rstrip("//")
    dir_path = dir.rstrip("//")
    if file_dir_path == dir_path:
        return True
    elif file_dir_path == "":
        return False
    else:
        return file_in_dir_r(file_dir_path, dir_path)

def set_auto_hostname(interface = "eth0"):
    add = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
    suffix = "".join(add.split(":")[3:6])
    machine_id ="pitally-" + suffix
    hostname = socket.gethostname()
    call(["hostnamectl", "set-hostname", machine_id])
    if hostname != machine_id:
        first_boot(app)
        logging.warning("Perfroming first boot")
    return machine_id
