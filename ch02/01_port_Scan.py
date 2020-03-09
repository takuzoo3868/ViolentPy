#!/usr/bin/env python
import argparse
from socket import *
from threading import Semaphore, Thread

_lock = Semaphore(value=1)


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


# From given tuple host:port, try to connect to it
def connection_scan(host, port):
    con = socket(AF_INET, SOCK_STREAM)
    try:
        con.connect((host, port))
        con.send(b"HOwaRey0u? ViolentPython3!!!\r\n")
        ans = con.recv(100)
        _lock.acquire()
        print("[+] {}:{} TCP Connection Open!".format(host, port))
        print("[+] {}!".format(ans))
    except Exception as e:
        _lock.acquire()
        print("[-] {}:{} TCP Connection Closed because {}!".format(host, port, e))
    finally:
        _lock.release()
        con.close()


# From given list of ports, try connecting given host to each port
def port_scan(host, ports, threading=False):
    try:
        host_ip = gethostbyname(host)
    except:
        print("[-] Cannot resolve host {}. Unknown host.".format(host))
        return

    try:
        host_name = gethostbyaddr(host_ip)
        print("[+] Scan Results for: {}".format(host_name[0]))
    except:
        print("[+] Scan Results for: {}".format(host_ip))

    setdefaulttimeout(1)
    for port in ports:
        print("[*] Scanning host {}:{}".format(host, port))
        if threading:
            t = Thread(target=connection_scan, args=(host, port))
            t.start()
        else:
            connection_scan(host, port)


def main():
    print(banner)

    parser = argparse.ArgumentParser(usage="%(prog)s -H <target host> -p <target_port(s)>")
    parser.add_argument("-H", dest="target_host", type=str,
                        required=True, help="Specify target host.")
    parser.add_argument("-p", dest="target_ports", type=str,
                        required=True, help="Specify target port(s) separated by comma.")
    parser.add_argument("-t", dest="threading", action="store_true",
                        help="Allow threading when connecting to different hosts.")
    options = parser.parse_args()

    target_ports = map(int, filter(None, map(lambda p: p.strip(), options.target_ports.split(","))))
    port_scan(options.target_host, target_ports, options.threading)

    # print(options)


if __name__ == "__main__":
    main()
