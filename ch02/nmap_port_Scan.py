import nmap
import argparse


def nmap_scan(host, port_num):
    """
    Scan host and port with library Nmap
    """
    nmScan = nmap.PortScanner()
    nmScan.scan(host, port_num)
    if nmScan.scaninfo().get("error"):
        print("[-] {} tcp/{} -> {}".format(host, port_num, nmScan.scaninfo().get("error")))
        return

    result = nmScan._scan_result
    for _ip in result["scan"].keys():
        state = result["scan"][_ip]["tcp"][int(port_num)]["state"]
        print("[+] {} tcp/{} {}".format(host, port_num, state))


def main():
    parser = argparse.ArgumentParser(usage="%(prog)s -H <target host> -p <target_port(s)>")
    parser.add_argument("-H", dest="target_host", required=True, type=str, help="Specify target host.")
    parser.add_argument("-p", dest="target_ports", required=True, type=str,
                        help="Specify target port(s) separated by comma.")

    options = parser.parse_args()

    target_ports = filter(None, map(lambda p: p.strip(), options.target_ports.split(",")))
    for port in target_ports:
        nmap_scan(options.target_host, port)

    print(options)


if __name__ == "__main__":
    main()
