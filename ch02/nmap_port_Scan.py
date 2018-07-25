#!/usr/bin/env python
import nmap
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'  # Add this color for resetting back the color.


banner = r"""{}{}
 ____   __   ____  ____        ____   ___   __   __ _ 
(  _ \ /  \ (  _ \(_  _)      / ___) / __) / _\ (  ( \
 ) __/(  O ) )   /  )(        \___ \( (__ /    \/    /
(__)   \__/ (__\_) (__)       (____/ \___)\_/\_/\_)__)
============================Written by t@kuz00E898======{}
""".format(bcolors.OKGREEN, bcolors.BOLD, bcolors.ENDC)


def nmap_scan(host, port_num):
    """
    Scan host and port with library Nmap
    """
    nmapScan = nmap.PortScanner()
    nmapScan.scan(host, port_num)

    if nmapScan.scaninfo().get("error"):
        print("[-] {} tcp/{} -> {}".format(host, port_num, nmapScan.scaninfo().get("error")))
        return

    result = nmapScan._scan_result
    for _ip in result["scan"].keys():
        state = result["scan"][_ip]["tcp"][int(port_num)]["state"]
        print("[+] {} tcp/{} {}".format(host, port_num, state))


def main():
    parser = argparse.ArgumentParser(usage="%(prog)s -H <target host> -p <target_port(s)>")
    parser.add_argument("-H", dest="target_host", required=True, type=str, help="Specify target host.")
    parser.add_argument("-p", dest="target_ports", required=True, type=str,
                        help="Specify target port(s) separated by comma.")

    options = parser.parse_args()

    target_ports = filter(None, map(lambda p: p.strip(), options.target_ports.split(",")))

    print(banner)
    for port in target_ports:
        nmap_scan(options.target_host, port)

    # print(options)


if __name__ == "__main__":
    main()
