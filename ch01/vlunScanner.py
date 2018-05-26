#!/usr/bin/env python
import socket
import optparse


def get_banner(ip, port, timeout):
    socket.setdefaulttimeout(timeout)
    s = socket.socket()
    try:
        print('[+] Grabbing banner from {}:{}'.format(str(ip), port))
        s.connect((ip, port))
        ans = s.recv(1024)
        return ans
    except Exception as e:
        print("[-] Error {}:{} = {}".format(ip, port, e))
        return None


def check_vulnerabilities(banner, filename):
    """
    Check for known vulnerable services against a pre-defined list of banners.

    :param banner: Banner being checked; type: str
    :param filename: List of vulnerability banners
    """
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.strip('\n') in banner:
                print("[+] Server is vulnerable: {}".format(banner.strip('\n')))
            else:
                print("[-] Server is not vulnerable")
                continue


def main():
    parser = optparse.OptionParser('usage %prog -n <network> -t <type of probe>')

    """
    options default
    ---------------
    network     : 192.168.1.x
    subnet start: 1
    subnet end  : 254
    ports       : telnet, ssh, smtp, http, imap and https
    vlun list   : banners.txt
    timeout     : 2   
    """
    parser.add_option('-n', dest='network', type='string', default="192.168.1.X", help='specify network to search on')
    parser.add_option('--start_subnet', dest='start_subnet', type='int', default=1,
                      help='specify which subnet should the scan start')
    parser.add_option('--end_subnet', dest='end_subnet', type='int', default=254,
                      help='specify which subnet should the scan stop')
    parser.add_option('-p', dest='ports', type='string', default="21, 22, 25, 80, 110, 443",
                      help='specify list of ports, separed by comma')
    parser.add_option('--vul_filename', dest='vulnerabilities_filename', type='string', default="banners.txt",
                      help='default file with list of vulnerabilities to compare')
    parser.add_option('--socket_timeout', dest='socket_timeout', type='int', default=2,
                      help='default socket connection timeout')
    (options, args) = parser.parse_args()

    subnet = options.network.lower()
    subnet_string = subnet.replace("x", "{}")
    ip_list = map(lambda ip: subnet_string.format(ip), range(options.start_subnet, options.end_subnet))
    port_list = map(int, filter(None, map(lambda p: p.strip(), options.ports.split(","))))

    print("[*] Testing subnet of {} for {} ports: {}".format(subnet, len(list(port_list)), options.ports))
    for ip in ip_list:
        for port in options.ports.split(","):
            port_int = int(port)
            banner = get_banner(ip, port_int, timeout=options.socket_timeout)
            if banner:
                print("[+] Checking {}:{}".format(ip, port))
                check_vulnerabilities(banner, filename=options.vul_filename)


if __name__ == '__main__':
    main()
