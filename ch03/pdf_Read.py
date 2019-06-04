#!/usr/bin/env python
import PyPDF2
import argparse
from PyPDF2 import PdfFileReader


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
 ____   ___   __   __ _    ____  ____  ____ 
/ ___) / __) / _\ (  ( \  (  _ \(    \(  __)
\___ \( (__ /    \/    /   ) __/ ) D ( ) _) 
(____/ \___)\_/\_/\_)__)  (__)  (____/(__)  
=====================Written by t@kuz00E898======{}
""".format(colors.OKGREEN, colors.BOLD, colors.END)


def print_metadata(filename):
    pdf_file = PdfFileReader(open(filename, 'rb'))
    doc_info = pdf_file.getDocumentInfo()
    print("[*] PDF MetaData For: {}".format(filename))

    for meta_item in doc_info:
        print("[+] {}: {}".format(meta_item, doc_info[meta_item]))


def main():
    print(banner)
    parser = argparse.ArgumentParser(usage="%(prog)s -f <PDF filename>")
    parser.add_argument("-f", dest="filename", type=str, required=True, help="specify PDF file name")
    options = parser.parse_args()

    filename = options.filename
    print_metadata(filename)


if __name__ == '__main__':
    main()
