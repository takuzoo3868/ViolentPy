#!/usr/bin/env python
"""
Usage: python vlunScanner.py <vulnerability_list_filename>
"""
import socket
import sys
import os


def get_banner(ip, portlist):
    """
    Scan for and return banners(first 1024 bytes message) from anIP across a port range.

    :return: Dictionary -- {PORT:BANNER}
    """
    socket.setdefaulttimeout(2)
    banner = {}
    for port in portlist:
        try:
            s = socket.socket()
            print('Grabbing banner from {}:{}'.format(str(ip), port))
            s.connect((ip, port))
            banner[port] = s.recv(1024)
            s.detach()
        except:
            continue
    return banner


def check_vulns(ip, port, filename, banner):
    """
    Check for known vulnerable services against a pre-defined list of banners.

    :param ip: IP address being scanned; type: str
    :param port: Port being scanned
    :param filename: List of vulnerability banners
    :param banner: Banner being checked; type: str
    :return: 0
    """
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.strip('\n') in banner:
                print('[+] IP: {} PORT: {}'.format(ip, port))
                print("[+] Server is vulnerable: {}".format(banner.strip('\n')))
            else:
                print("[-] Server is not vulnerable")
                continue
    return 0


def main():
    if len(sys.argv) == 2:
        vuln_list = sys.argv[1]
        if not os.path.isfile(vuln_list):
            print('Vulnerability list ({}) missing'.format(vuln_list))
            exit(1)
        elif not os.access(vuln_list, os.R_OK):
            print('Access to Vulnerability List File Denied')
            exit(1)
        else:
            print('Scanning IP range 10.10.10.(1 - 255)')
            port_list = list(range(1, 1001))
            banner = {}

            for i in range(1, 255):
                ip = '10.10.10.' + str(i)  # Change to appropriate IP range
                banner[ip] = get_banner(ip, port_list)

            for ip in list(banner.keys()):
                for port in banner[ip].keys():
                    check_vulns(ip, port, vuln_list, str(banner[ip][port]))
    else:
        print('Usage: python vlunScanner.py <vulnerability_list_filename>')
        exit(1)

    return 0


if __name__ == '__main__':
    main()
