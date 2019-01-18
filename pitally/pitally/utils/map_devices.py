#! /usr/bin/env python
# vim: set fenc=utf8 ts=4 sw=4 et :
#
# Layer 2 network neighbourhood discovery tool
# written by Benedikt Waldvogel (mail at bwaldvogel.de)

from __future__ import absolute_import, division, print_function
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
import errno
import logging


def long2net(arg):
    if (arg <= 0 or arg >= 0xFFFFFFFF):
        raise ValueError("illegal netmask value", hex(arg))
    return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))


def to_CIDR_notation(bytes_network, bytes_netmask):
    network = scapy.utils.ltoa(bytes_network)
    netmask = long2net(bytes_netmask)
    net = "%s/%s" % (network, netmask)
    if netmask < 16:
        logging.warn("%s is too big. skipping" % net)
        return None
    return net


def scan_and_print_neighbors(net, interface, timeout=5):
    out = {}
    try:
        ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=True)
        for s, r in ans.res:
            try:
                hostname = socket.gethostbyaddr(r.psrc)
                if hostname and hostname[0].startswith("pitally"):
                    device = {hostname[0].split(".")[0]: {"mac":r.sprintf("%Ether.src%"),
                                           "ip": r.sprintf("%ARP.psrc%")}}
                    out.update(device)
            except socket.herror:
                pass

    except socket.error as e:
        if e.errno == errno.EPERM:     # Operation not permitted
            logging.error("%s. Did you run as root?", e.strerror)
        else:
            raise
    return out


def map_devices():
    devices = {}
    for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:
    # skip loopback network and default gw
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue

        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue

        net = to_CIDR_notation(network, netmask)

        if net:
            devs = scan_and_print_neighbors(net, interface)
            devices.update(devs)
    return devices


