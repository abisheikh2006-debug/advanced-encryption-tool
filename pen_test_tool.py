import socket
import subprocess
import platform
import requests

def port_scan(target, ports):
    print(f"[*] Scanning ports on {target}")
    open_ports = []
    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((target, port))
            open_ports.append(port)
            s.close()
        except:
            continue
    return open_ports

def ping_host(host):
    print(f"[*] Pinging host {host}")
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', host]
    return subprocess.run(command, stdout=subprocess.PIPE).stdout.decode()

def whois_lookup(domain):
    print(f"[*] Performing WHOIS lookup for {domain}")
    try:
        response = requests.get(f"https://rdap.org/domain/{domain}")
        return response.json()
    except:
        return {"error": "WHOIS lookup failed or not supported"}

def main():
    target = input("Enter the target IP or domain: ")
    print("\n--- Ping Test ---")
    print(ping_host(target))

    print("\n--- Port Scan ---")
    ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3389]
    open_ports = port_scan(target, ports_to_scan)
    print(f"Open ports on {target}: {open_ports}")

    print("\n--- WHOIS Lookup ---")
    if not target.replace('.', '').isdigit():
        whois = whois_lookup(target)
        for k, v in whois.items():
            print(f"{k}: {v}")
    else:
        print("WHOIS lookup skipped for IP addresses")

if __name__ == "__main__":
    main()
