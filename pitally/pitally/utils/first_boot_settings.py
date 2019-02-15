import subprocess

WPA_SUPPLICANT_CONF = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=%s

network={
	ssid="%s"
	psk="%s"
}
"""


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

def set_ntp():
    pass


def first_boot(app):
    wifi_config(app.config["NETWORK_SSID"],
                app.config["NETWORK_PSK"],
                app.config["NETWORK_COUNTRY"])
    enable_camera()
    set_ntp()
    set_password(app.config["PI_PASSWORD"])
    subprocess.call(["reboot"])

