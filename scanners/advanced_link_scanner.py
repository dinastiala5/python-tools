import requests
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime

print("=== ADVANCED LINK SECURITY SCANNER ===")

url = input("Enter website URL: ")

if not url.startswith("http"):
    url = "http://" + url

parsed = urlparse(url)
domain = parsed.netloc

risk = 0

print("\n[+] Domain:", domain)

# IP address
try:
    ip = socket.gethostbyname(domain)
    print("[+] IP Address:", ip)
except:
    print("[-] Could not resolve IP")

# Website status
try:
    r = requests.get(url, timeout=5)
    print("[+] Website status:", r.status_code)
except:
    print("[-] Website not reachable")
    risk += 20

# WHOIS info
print("\n=== WHOIS INFO ===")

try:
    w = whois.whois(domain)

    creation = w.creation_date
    if isinstance(creation, list):
        creation = creation[0]

    print("Registrar:", w.registrar)
    print("Creation Date:", creation)
    print("Expiration Date:", w.expiration_date)

    # Domain age check
    if creation:
        age = (datetime.now() - creation).days
        print("Domain Age:", age, "days")

        if age < 180:
            print("⚠ Very new domain")
            risk += 40

except:
    print("WHOIS info not available")

# Phishing checks
print("\n=== PHISHING CHECKS ===")

if "@" in url:
    print("⚠ '@' symbol detected")
    risk += 30

if "-" in domain:
    print("⚠ Hyphen in domain")
    risk += 10

if len(domain) > 30:
    print("⚠ Very long domain")
    risk += 20

# Risk score
print("\n=== SECURITY RISK SCORE ===")
print("Risk score:", risk, "/ 100")

# Final verdict
print("\n=== FINAL VERDICT ===")

if risk < 20:
    print("SAFE ✅")
elif risk < 50:
    print("SUSPICIOUS ⚠")
else:
    print("DANGEROUS 🚨")

print("\nScan complete.")
