#!/usr/bin/env python

import argparse
import crypt
import hashlib

from tqdm import tqdm


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
 ____   __   ____  ____     ___  ____   __    ___  __ _ 
(  _ \ / _\ / ___)/ ___)   / __)(  _ \ / _\  / __)(  / )
 ) __//    \\___ \\___ \  ( (__  )   //    \( (__  )  ( 
(__)  \_/\_/(____/(____/   \___)(__\_)\_/\_/ \___)(__\_)
Last Modified: 22 May 2019.
- Execute a standard dictionary attack.
============================Written by t@kuz00E898======{}
""".format(colors.OKGREEN, colors.BOLD, colors.END)


def test_passwd(crypt_pass, dictionary_filename, algo):
    """
    Test passwords depending on hashing algorithm.

    DES:
    strips out the salt from the first two characters of the encrypted password
    hash and returns either after finding the password or exhausting the words
    in the dictionary.

    SHA512:
    ID (A value of 1 denotes MD5; 2 or 2a is Blowfish; 3 is NT Hash; 5 is
    SHA-256; and 6 is SHA-512.), salt and hash separated by $ This function
    currently only supports SHA512.
    """
    if algo == ("des" or "DES"):
        salt = crypt_pass[:2]
        with open(dictionary_filename, "r") as f:
            for word in tqdm(f.readlines()):
                word = word.strip()
                crypt_test = crypt.crypt(word, salt)

                if crypt_pass == crypt_test:
                    print("[+] Found password: {}".format(word))
                    return word
        print("[-] Password not found.")
        return

    elif algo == ("sha512" or "SHA512"):
        salt = str.encode(crypt_pass.split("$")[2])
        with open(dictionary_filename, "r") as f:
            for word in f.readlines():
                word = str.encode(word.strip("\n"))
                crypt_word = hashlib.sha512(salt + word)
                if crypt_word.hexdigest() == crypt_pass.split("$")[3]:
                    print("[+] Found Password: {}".format(word.decode()))
                    return
    else:
        print("Supported hashing algorithms: des / sha512")
        exit(1)


def main():
    parser = argparse.ArgumentParser(
        usage="%(prog)s --algo <des/sha512> --unknown_passwords <file list of hashed passwords> --test_passwords <file list of possible passwords>",
        description="Execute a standard dictionary attack.")

    parser.add_argument("--algo", help="specify algorithm DES or SHA512",
                        dest="algo",
                        default="des")
    parser.add_argument("--unknown_passwords", help="specify file that contains list of unknown hashed passwords",
                        dest="unknown_passwords",
                        default="password.txt")
    parser.add_argument("--test_passwords", help="specify file that contains list of possible passwords",
                        dest="test_passwords",
                        default="dictionary.txt")
    options = parser.parse_args()

    print(banner)
    with open(options.unknown_passwords) as unknown_passwords:
        for line in unknown_passwords.readlines():
            if ":" in line:
                user = line.split(":")[0]
                crypt_pass = line.split(":")[1].strip(" ")
                print("[*] Cracking Password For: {}".format(user))
                test_passwd(crypt_pass, options.test_passwords, options.algo)


if __name__ == "__main__":
    main()
