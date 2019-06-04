#!/usr/bin/env python
import os, sys
import urllib.request
import io
import bs4 as bs
import ssl


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def banner():
    banner = r'''{}{}
     
   ██████╗ ██████╗ ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
  ██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
  ██║   ██║██████╔╝███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
  ██║   ██║██╔══██╗╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
  ╚██████╔╝██████╔╝███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
   ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
  ======================================Written by t@kuz00E898======{}                                                                  
    '''.format(colors.OKGREEN, colors.BOLD, colors.END)

    return banner


OPTIONS = '''
1. List supported vendors
2. Search Default Password
3. Exit
'''
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


def menu():
    while True:
        try:
            choice = str(input('\n[?] Do you want to continue? \n> ')).lower()
            if choice[0] == 'y':
                return
            if choice[0] == 'n':
                sys.exit(0)
                break
        except ValueError:
            sys.exit(0)


def checkInternetConnection():
    try:
        urllib.request.urlopen('https://cirt.net/')
    except:
        print('[!] No internet connection...Please connect to the Internet')
    else:
        print('[+] Checking Internet connection...')


def formatTable(table):
    text = ''
    rows = table.find_all('tr')
    text += '%s\n' % rows[0].text

    for row in rows[1:]:
        data = row.find_all('td')
        text += '%s: %s\n' % (data[0].text, data[1].text)

    return text


def cmd_vendorSearch():
    vendor = input('Enter Vendor Name:').lower()
    urlenc = urllib.parse.quote(vendor)
    url = "https://cirt.net/passwords?vendor=" + urlenc
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    # response = urllib.quote(request)
    # print (response.read().decode('utf-8'))
    soup = bs.BeautifulSoup(response, "html.parser")
    # print(soup.find_all('a'))
    for links in soup.find_all('table'):
        # print(links.text)
        print(formatTable(links))


def cmd_openFile():
    path = './vendors.txt'
    vendors_file = open(path, 'r')
    vendors = vendors_file.read()
    print(vendors)


cmds = {
    "1": cmd_openFile,
    "2": cmd_vendorSearch,
    "3": lambda: sys.exit(0)
}


def main():
    print(banner())
    checkInternetConnection()
    try:
        while True:
            choice = input("\n%s" % OPTIONS)
            if choice not in cmds:
                print('[!] Invalid Choice')
                continue
            cmds.get(choice)()
    except KeyboardInterrupt:
        print('[!] Ctrl + C detected\n[!] Exiting')
        sys.exit(0)
    except EOFError:
        print('[!] Ctrl + D detected\n[!] Exiting')
        sys.exit(0)


if __name__ == "__main__":
    main()
