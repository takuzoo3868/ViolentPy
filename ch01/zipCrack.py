#!/usr/bin/env python
"""
Run a dictionary attack for cracking zip file passwords.
Usage: python crackzip.py <zip_filename> <dictionary_filename>
"""
import sys
import os
import zipfile
import optparse
from tqdm import tqdm
from threading import Thread


def extract_file(file, password):
    """
    Try to extract files from secured zip file. Print password if that works
    """
    try:
        zipf = zipfile.ZipFile(file)
        zipf.extractall(path=os.path.join(file[:-4]), pwd=str.encode(password))
        print("[+] Found password {}".format(password))
    except:
        pass


def main():
    # -h help usage
    parser = optparse.OptionParser(
        '%prog --zipfile <secure zipfile> --test_passwords <file list of possible passwords>')
    # -h help options
    parser.add_option('--zipfile', dest='zipfile', type='string', default="evil.zip",
                      help='specify zip filename to crack')
    parser.add_option('--test_passwords', dest='test_passwords', type='string', default="dictionary.txt",
                      help='specify file that contains list of possible passwords')
    (options, args) = parser.parse_args()

    with open(options.test_passwords) as dictionary_file:
        for possible_password in tqdm(dictionary_file.readlines()):
            password = possible_password.strip()
            t = Thread(target=extract_file, args=(options.zipfile, password))
            t.start()


if __name__ == '__main__':
    main()
