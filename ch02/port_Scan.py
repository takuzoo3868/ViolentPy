#!/usr/bin/env python
from socket import *
import argparse
from threading import Thread, Semaphore

_lock = Semaphore(value=1)


def connection_scan(host, port):
    """
    From given tuple host:port, try to connect to it
    """
    con = socket(AF_INET, SOCK_STREAM)
    try:
        con.connect((host, port))
        con.send(b"HOwaRey0u?\r\n")
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


def port_scan(host, ports, threading=False):
    """
    From given list of ports, try connecting given host to each port
    """
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
    parser = argparse.ArgumentParser(usage="%(prog)s -H <target host> -p <target_port(s)>")
    parser.add_argument("-H", dest="target_host", type=str,
                        required=True, help="Specify target host.")
    parser.add_argument("-p", dest="target_ports", type=str,
                        required=True, help="Specify target port(s) separated by comma.")
    parser.add_argument("-t", dest="threading", action="store_true", help="Allow threading when connecting to different hosts.")
    options = parser.parse_args()

    target_ports = map(int, filter(None, map(lambda p: p.strip(), options.target_ports.split(","))))
    port_scan(options.target_host, target_ports, options.threading)

    print(options)


if __name__ == "__main__":
    main()
