# just for testing pusposes a made up list of devices
import time

def fake_dev_map():
    time.sleep(2)
    return [{"hostname": "pitally-012345.lan", "mac": "01:23:45:67:89:ab", "ip":"192.168.1.2"},
            {"hostname": "pitally-56789a.lan", "mac": "01:23:45:67:89:ac", "ip": "192.168.1.5"},
            {"hostname": "pitally-789abc.lan", "mac": "01:23:45:67:89:ad", "ip": "192.168.1.3"}
            ]
