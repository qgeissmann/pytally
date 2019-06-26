import netifaces
from subprocess import call
import socket
import os
import subprocess
import logging

WPA_SUPPLICANT_CONF = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=%s
network={
	ssid="%s"
    psk="%s"
}
"""


def file_in_dir_r(file, dir):
    file_dir_path = os.path.dirname(file).rstrip("//")
    dir_path = dir.rstrip("//")
    if file_dir_path == dir_path:
        return True
    elif file_dir_path == "":
        return False
    else:
        return file_in_dir_r(file_dir_path, dir_path)


def set_auto_hostname(app, interface = "eth0"):
    add = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
    suffix = "".join(add.split(":")[3:6])
    machine_id ="pitally-" + suffix
    hostname = socket.gethostname()
    call(["hostnamectl", "set-hostname", machine_id])
    if hostname != machine_id:
        first_boot(app)
        logging.warning("Performing first boot")
    return machine_id


def wifi_config(ssid, psk, country = 'US', conf_file="/etc/wpa_supplicant/wpa_supplicant.conf"):
    content = WPA_SUPPLICANT_CONF % (country, ssid, psk)
    with open(conf_file, 'w') as f:
        f.write(content)


def enable_camera():
    command = 'sed s/"INTERACTIVE=True"/"INTERACTIVE=False"/ $(which raspi-config) > /tmp/camera_on.sh && '\
                         'echo "do_camera 0" >> /tmp/camera_on.sh && '\
                         'echo "do_memory_split 256" >> /tmp/camera_on.sh && '\
                         'bash /tmp/camera_on.sh && '\
                         'rm /tmp/camera_on.sh'

    p = subprocess.Popen(command, shell=True)

    return p.communicate()


def set_password(password, user="pi"):
    p = subprocess.Popen('echo "%s:%s"|chpasswd' % (user, password), shell=True)
    return p.communicate()


def set_ntp(app, ntp_conf_file="/etc/systemd/timesyncd.conf"):
    line = "FallbackNTP=%s\n" % app.config["FTP_HOSTNAME"]
    with open(ntp_conf_file, "w") as f:
        f.write(line)


def first_boot(app):
    wifi_config(app.config["NETWORK_SSID"],
                app.config["NETWORK_PSK"],
                app.config["NETWORK_COUNTRY"])
    enable_camera()
    set_ntp(app)
    set_password(app.config["PI_PASSWORD"])
    subprocess.call(["reboot"])

