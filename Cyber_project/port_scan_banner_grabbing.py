import socket

def scan_port(host, port):
    """Scan a single port and attempt banner grabbing."""
    try:
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Timeout for responsiveness

        # Try to connect
        result = s.connect_ex((host, port))
        if result == 0:
            # Try to detect common service by port number
            try:
                service_name = socket.getservbyport(port)
            except OSError:
                service_name = "Unknown"

            banner = ""
            try:
                # Send a generic request to provoke a banner
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = s.recv(1024).decode(errors="ignore").strip()
            except socket.error:
                banner = "No banner"

            print(f"[+] Port {port} is open | Service: {service_name} | Banner: {banner[:60]}...")
        s.close()

    except Exception as e:
        print(f"[-] Error scanning port {port}: {e}")


def scan_host(host, ports):
    """Scan multiple ports on a host."""
    print(f"Scanning host {host}...")
    for port in ports:
        scan_port(host, port)


if __name__ == "__main__":
    target_host = input("Enter target host (IP or domain): ").strip()

    # Example port list: common ports
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]
    scan_host(target_host, common_ports)
# port_scan_banner_grabbing.py 
# A simple port scanner with banner grabbing functionality. 
# This script scans a list of common ports on a target host and attempts to grab service banners. 
# Note: Use responsibly and ensure you have permission to scan the target host. 
