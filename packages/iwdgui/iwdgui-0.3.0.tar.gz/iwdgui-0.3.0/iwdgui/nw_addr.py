#!/usr/bin/python3
"""
arp: provides functions to convert HW (MAC) to IP addresses and vice versa
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import socket

ARPFILE = "/proc/net/arp"

"""
The arp table look like this:
IP address       HW type     Flags       HW address            Mask     Device
192.168.149.178  0x1         0x2         00:24:2b:0b:08:09     *        wlan1
192.168.178.1    0x1         0x0         00:00:00:00:00:00     *        br-lxc
192.168.178.1    0x1         0x2         34:81:c4:ca:97:06     *        wlan0
"""

#field numbers for the ARP table:
ARP_IPADDR = 0
ARP_HWTYPE = 1
ARP_FLAGS = 2
ARP_HWADDR = 3
ARP_MASK = 4
ARP_DEVICE = 5

def arp_read():
    "Reads the arp table, returns it as a list"
    with open(ARPFILE, "r") as fh:
        next(fh)
        arp_list = []
        for line in fh:
            arp_list.append(line.split())
        return arp_list

def match(lst, search_term, search_col, result_col):
    "full table scan to find a search item in a col, returns the result col"
    for row in lst:
        if row[search_col] == search_term:
            return row[result_col]
    return None

def hwaddr2ipaddr(lst, hwaddr):
    "converts a hw address in an IP address"
    return match(lst, hwaddr, ARP_HWADDR, ARP_IPADDR)

def ipaddr2hwaddr(lst, ipaddr):
    "converts an IP address into a hardware address"
    return match(lst, ipaddr, ARP_IPADDR, ARP_HWADDR)

def hwaddr2hostname(lst, hwaddr):
    ipaddr = hwaddr2ipaddr(lst, hwaddr)
    if ipaddr:
        try:
            hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ipaddr)
            return hostname
        except Exception as e:
            print("hwaddr2hostname: could not find hostname for", ipaddr)
    return ipaddr
