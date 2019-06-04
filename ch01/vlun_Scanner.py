#!/usr/bin/env python
import socket
import argparse
from colorama import Fore, Style


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# font Graceful
logo = r"""{}{}
 _  _  _  _  __    __ _    ____   ___   __   __ _ 
/ )( \/ )( \(  )  (  ( \  / ___) / __) / _\ (  ( \
\ \/ /) \/ (/ (_/\/    /  \___ \( (__ /    \/    /
 \__/ \____/\____/\_)__)  (____/ \___)\_/\_/\_)__)
Last Modified: 22 May 2019.
- grab network banner from vlun server
============================Written by t@kuz00E898======{}
""".format(colors.OKGREEN, colors.BOLD, colors.END)


def get_banner(ip, port, timeout):
    socket.setdefaulttimeout(timeout)
    s = socket.socket()
    try:
        print("[*] Grabbing banner from {}:{}".format(str(ip), port))
        s.connect((ip, port))
        ans = s.recv(1024)
        print("{}[+]{} Connection to {}:{} is succeeded!".format(Fore.GREEN, Style.RESET_ALL, str(ip), port))
        print("{}[+]{} {}".format(Fore.GREEN, Style.RESET_ALL, str(ans)))
        return ans
    except Exception as e:
        print("{}[-]{} Unable to grab any information: {}".format(Fore.RED, Style.RESET_ALL, ip, port, e))
        return None

# Check for known vulnerable services against a pre-defined list of banners.
def check_vulnerabilities(banner, filename):
    with open(filename, "r") as f:
        for line in f.readlines():
            if line.strip("\n") in banner:
                print("{}[-]{} Server is vulnerable: {}".format(Fore.RED, Style.RESET_ALL, banner.strip("\n")))
            else:
                continue


def main():
    parser = argparse.ArgumentParser(usage="%(prog)s -n <IP address>")
    parser.add_argument("-n", "--network", help="specify IP address to search on",
                        dest="network",
                        default="192.168.58.X")
    parser.add_argument("-start", "--start_subnet", help="specify which subnet should the scan start",
                        dest="start_subnet",
                        type=int, default=1)
    parser.add_argument("-end", "--end_subnet", help="specify which subnet should the scan stop",
                        dest="end_subnet",
                        type=int, default=5)
    parser.add_argument("-p", "--port", help="specify list of ports, separed by comma",
                        dest="ports",
                        default="21, 22, 25, 80, 110, 443")
    parser.add_argument("-f", "--file", help="default file with list of vulnerabilities to compare",
                        dest="file",
                        default="banners.txt")
    parser.add_argument("-out", "--socket_timeout", help="default socket connection timeout",
                        dest="socket_timeout",
                        type=int, default=2)
    options = parser.parse_args()

    print(logo)

    subnet = options.network.lower()
    subnet_string = subnet.replace("x", "{}")
    ip_list = map(lambda ip: subnet_string.format(ip), range(options.start_subnet, options.end_subnet))
    port_list = map(int, filter(None, map(lambda p: p.strip(), options.ports.split(","))))

    print("[*] Testing subnet of {} for {} ports: {}".format(subnet, len(list(port_list)), options.ports))
    for ip in ip_list:
        for port in options.ports.split(","):
            port_int = int(port)
            banner = get_banner(ip, port_int, timeout=options.socket_timeout)
            if banner:
                print("[*] Checking {}:{}".format(ip, port))
                check_vulnerabilities(str(banner), filename=options.file)
                print("[*] Nothing vulnerable server :)")


if __name__ == "__main__":
    main()
