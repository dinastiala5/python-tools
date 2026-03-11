import socket

print("\nSimple Port Scanner\n")

target = input("Enter target website (example: google.com): ")

# common ports to scan
ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]

print("\nScanning target:", target)
print("--------------------------------")

for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is OPEN")

    s.close()

print("\nScan complete")
