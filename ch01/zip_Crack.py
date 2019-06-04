#!/usr/bin/env python
import sys
import os
import zipfile
import argparse
from tqdm import tqdm
from threading import Thread


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
banner = r"""{}{}
 ____  __  ____     ___  ____   __    ___  __ _ 
(__  )(  )(  _ \   / __)(  _ \ / _\  / __)(  / )
 / _/  )(  ) __/  ( (__  )   //    \( (__  )  ( 
(____)(__)(__)     \___)(__\_)\_/\_/ \___)(__\_)
Last Modified: 22 May 2019.
- Run a dictionary attack for cracking zip file passwords.
============================Written by t@kuz00E898========={}
""".format(colors.OKGREEN, colors.BOLD, colors.END)


# Try to extract files from secured zip file. Print password if that works
def extract_file(file, password):
    try:
        zipf = zipfile.ZipFile(file)
        zipf.extractall(path=os.path.join(file[:-4]), pwd=str.encode(password))
        print("[+] Found password {}".format(password))
    except:
        pass


def main():
    parser = argparse.ArgumentParser(
        usage="%(prog)s --zipfile <secure zipfile> --test_passwords <file list of possible passwords>",
        description="Run a dictionary attack for cracking zip file passwords.")

    parser.add_argument("--zipfile", help="specify zip filename to crack",
                        dest="zipfile",
                        default="evil.zip")
    parser.add_argument("--test_passwords", help="specify file that contains list of possible passwords",
                        dest="test_passwords",
                        default="dictionary.txt")
    options = parser.parse_args()

    print(banner)
    with open(options.test_passwords) as dictionary_file:
        for possible_password in tqdm(dictionary_file.readlines()):
            password = possible_password.strip()
            t = Thread(target=extract_file, args=(options.zipfile, password))
            t.start()


if __name__ == "__main__":
    main()
