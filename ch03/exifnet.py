#!/usr/bin/env python
import urllib.request
import argparse
import urllib.parse
from os.path import basename, dirname
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS


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
  ___  ____  ____    _  _   __  ____  ___  _  _  ____  ____ 
 / __)(  _ \/ ___)  / )( \ / _\(_  _)/ __)/ )( \(  __)(  _ \
( (_ \ ) __/\___ \  \ /\ //    \ )( ( (__ ) __ ( ) _)  )   /
 \___/(__)  (____/  (_/\_)\_/\_/(__) \___)\_)(_/(____)(__\_)

=================================Written by t@kuz00E898======{}
""".format(colors.OKBLUE, colors.BOLD, colors.END)


# Return all img"s on given url
def find_images(url):
    print("[+] Finding images on {}".format(url))
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, "html5lib")
        return soup.findAll("img")
    except Exception as e:
        print("[-] Failed to get images from {} because: {}".format(dirname(url), str(e)))
    return ""


# From given soup img tag, try to get it"s content and save it on a new image file
def download_image(img_tag):
    try:
        print("[+] Downloading image... {}".format(img_tag))
        source = img_tag["src"]
        content = urllib.request.open(source).read()
        filename = basename(urlsplit(content)[2])
        with open(filename, "wb") as img_file:
            img_file.write(content)
        return filename
    except Exception:
        return ""


# From given img filename, print image exiftool GPS info, if there is any
def print_exiftool_data(img_filename):
    data = {}
    try:
        img_file = Image.open(img_filename)
        info = img_file._getexif()
        if not info:
            return

        for (tag, value) in info.items():
            decoded = TAGS.get(tag, tag)
            data[decoded] = value

        exifGPS = data["GPSInfo"]
        if not exifGPS:
            return

        print("[*] {} contains GPS MetaData".format(img_filename))
    except Exception:
        pass


def main():
    print(banner)
    parser = argparse.ArgumentParser(usage="%(prog)s -u <target url>")
    parser.add_argument("-u", dest="url", type=str, help="specify url address")
    options = parser.parse_args()

    url = options.url
    if not url:
        print(parser.usage)
        exit(0)

    # run pipeline
    images = find_images(url)
    print("[*] Found {} images".format(len(images)))
    map(lambda img_tag: print_exiftool_data(download_image(img_tag)), images)


if __name__ == "__main__":
    main()
