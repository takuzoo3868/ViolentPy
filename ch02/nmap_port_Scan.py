#!/usr/bin/env python
import nmap
import socket
import threading
import argparse
import time
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


banner = r"""{}{}
 ____   __  ____  ____    ____   ___   __   __ _ 
(  _ \ /  \(  _ \(_  _)  / ___) / __) / _\ (  ( \
 ) __/(  O ))   /  )(    \___ \( (__ /    \/    /
(__)   \__/(__\_) (__)   (____/ \___)\_/\_/\_)__)
============================Written by t@kuz00E898======{}
""".format(colors.OKGREEN, colors.BOLD, colors.END)


# Scan host and port with library Nmap
class nmap_scan:
    def __init__(self):
        self.verbose = False
        self.initialize_variable()
        self.multi_thread(self.ipv4, self.target_ports)

    def initialize_variable(self):
        self.verbose = False

        if options.target_host:
            if options.target_host[0].isdigit():
                self.ipv4 = options.target_host
            elif options.target_host[0].isalpha():
                addr = options.target_host
                if 'http://' in addr: addr = addr.strip('http://')
                self.ipv4 = self.resolve(addr)

        elif not options.target_host:
            print("[!] --target argument is not supplied, default value (localhost) is taken")
            self.ipv4 = '127.0.0.1'

        if options.target_ports:
            if '-' in options.target_ports:
                self.high_range = int(options.target_ports.split('-')[1])
                self.low_range = int(options.target_ports.split('-')[0])
                self.target_ports = [i for i in range(self.low_range, (self.high_range + 1))]
            else:
                self.target_ports = [options.target_ports]
                self.verbose = True

        elif not options.target_ports:
            print("[!] --target_ports argument is not supplied, default value (20-1024) is taken")
            self.high_range = 1024
            self.low_range = 20
            self.target_ports = [i for i in range(self.low_range, self.high_range)]

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

    def scan(self, ipv4, port):
        # print("[.] Scanning %s : %s" % (ipv4,port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status = s.connect_ex((ipv4, port))
        if status == 0:
            print("[+] =[\033[91m{:^6}\033[0m]= Port open".format(port))
        else:
            if self.verbose:
                print("[+]=[{}]= Port closed".format(port))
            elif not self.verbose:
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
            if self.online(ipv4):
                print("[~] Target : {}".format(ipv4))
                if len(ports) > 1:
                    for i in ports:
                        t = threading.Thread(target=self.scan, args=(ipv4, int(i),)).start()
                else:
                    t = threading.Thread(target=self.scan, args=(ipv4, int(ports[0]))).start()

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
        print("[Banner Information]\n{}".format(response))


def main():
    global options

    parser = argparse.ArgumentParser(usage="%(prog)s -H <target host> -p <target_port(s)>")
    parser.add_argument("-H", dest="target_host", type=str, help="Specify target host.")
    parser.add_argument("-p", dest="target_ports", type=str,
                        help="Specify port range to scan separated with -.", metavar="5-300 or 80")

    options = parser.parse_args()

    print(banner)
    nmap_scan()


if __name__ == "__main__":
    main()
