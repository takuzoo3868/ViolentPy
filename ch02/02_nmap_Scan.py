#!/usr/bin/env python
import argparse
import os
import socket
import concurrent.futures
import time
import ipaddress
from typing import List
from typing import Any
from signal import SIG_DFL, SIGPIPE, signal

import nmap
from tqdm import tqdm
from tabulate import tabulate

signal(SIGPIPE, SIG_DFL)


# Return the Local IP Address of the interface
def get_local_ip(interface: str = "wlan0") -> str:
    if "nux" in sys.platform:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            return socket.inet_ntoa(
                fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', interface[:15]))[20:24]
            )

        except IOError:
            print("[!] Error, unable to detect local ip address.")
            print("[!] Check your connection to network.")
            exit()

    elif "darwin" in sys.platform:
        return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]


# Scan host and port with library Nmap
class nmap_scan:
    def __init__(self):
        self.initialize_variable()
        self.multi_thread(self.ipv4, self.target_ports)

    def initialize_variable(self):
        if options.target_host[0].isdigit():
            self.ipv4 = options.target_host
        elif options.target_host[0].isalpha():
            addr = options.target_host
            if 'http://' in addr:
                addr = addr.strip('http://')
            self.ipv4 = self.resolve(addr)

        if '-' in options.target_ports:
            self.high_range = int(options.target_ports.split('-')[1])
            self.low_range = int(options.target_ports.split('-')[0])
            self.target_ports = [i for i in range(self.low_range, (self.high_range + 1))]
        else:
            self.target_ports = [options.target_ports]

    def ip2int(self, row) -> int:
        return int(ipaddress.IPv4Address(row[0]))

    # Get website and translate it to IP address
    def resolve(self, host):
        print("[+] Target argument received website address")
        print("[+] Resolving website address to ip address")
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            print("[!] Error resolving website to ip, please get ip address manually!!!")
            exit()
        else:
            print("[+] {} = {}".format(host, ip))
            return ip

    # Check target port service using nmap -sV -p
    def scan(self, ipv4, port):
        # print("[.] Scanning %s : %s" % (ipv4,port))
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=ipv4, ports=str(port), arguments='-sV')
            nm.scaninfo()
            return nm[ipv4], port
        except KeyError:
            pass

    # Check if target is online using nmap -sP probe
    def online(self, ip):
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=ip, arguments='-sP')
            result = nm[ip].state()
        except KeyError:
            pass
        else:
            if result == 'up':
                return True
            else:
                return False

    def multi_thread(self, ipv4, ports):
        # Handles port scanning operation with multi-threading
        try:
            # Check if the target is online or offline first.
            scan_result = []
            if self.online(ipv4):
                print("[~] Target : {}".format(ipv4))
                if len(ports) > 1:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                        futures = {executor.submit(self.scan, ipv4, int(i)): i for i in ports}
                        # Progress bar
                        bar = tqdm(concurrent.futures.as_completed(futures), total=len(ports))
                        for f in bar:
                            bar.set_description("Scaning")

                else:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                        futures = executor.submit(self.scan, ipv4, int(ports[0]))

                # Generate result table
                for future in concurrent.futures.as_completed(futures):
                    result, port = future.result()
                    if result['tcp'][int(port)]['state'] == "open":
                        name = result.tcp(int(port))['name']
                        product = result.tcp(int(port))['product']
                        version = result.tcp(int(port))['version']
                        info = "{} {}".format(product, version)
                        cpe = result.tcp(int(port))['cpe']

                        scan_result.append((port, name, info, cpe))

                sort_list = sorted(scan_result)
                print("\n[Open port Information]")
                print(tabulate(sort_list, headers=["PORT", "SERVICE", "INFO", "CPE"], tablefmt="psql"))
                executor.shutdown()

                self.banner_grab(ipv4, 80)

            elif not self.online(ipv4):
                print("[!] Target IP is offline, or blocking nmap -sP probe")

        except KeyboardInterrupt:
            print("[~] Process stopped as TERMINATE Signal received")

    def banner_grab(self, ipv4, port):
        s = socket.socket()
        s.connect_ex((ipv4, port))
        s.send(b"GET HTTP/1.1 \r\n")

        response = s.recv(1024)
        time.sleep(3)
        if response:
            pass
        print("\n[Banner Information]\n{}".format(response))


def main():
    global options

    parser = argparse.ArgumentParser(usage="%(prog)s -H <target host> -p <target_port(s)>")
    parser.add_argument("-H", dest="target_host", type=str, help="Specify target host.", default="127.0.0.1")
    parser.add_argument("-p", dest="target_ports", type=str, help="Specify port range to scan separated with -.",
                        metavar="5-300 or 80", default="20-1024")

    options = parser.parse_args()

    start_time = int(time.time())

    nmap_scan()

    end_time = int(time.time())
    print("\n[*] Elasped : {} seconds".format(end_time - start_time))


if __name__ == "__main__":
    main()
