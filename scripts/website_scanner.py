import socket
import requests

def scan_website(url):
    print("\n--- Website Information Scanner ---\n")

    try:
        # Get IP address
        hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
        ip = socket.gethostbyname(hostname)
        print(f"Domain: {hostname}")
        print(f"IP Address: {ip}")

        # Send HTTP request
        response = requests.get(url)

        print(f"\nStatus Code: {response.status_code}")
        print("\n--- Headers ---")

        for header, value in response.headers.items():
            print(f"{header}: {value}")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    site = input("Enter website URL (example: https://example.com): ")
    scan_website(site)
