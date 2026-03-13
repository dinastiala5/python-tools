from urllib.parse import urlparse
import socket
import requests
import whois
from datetime import datetime

print("=== CYBER SECURITY LINK SCANNER ===")

url = input("Enter URL: ")

if not url.startswith("http"):
    url = "http://" + url

parsed = urlparse(url)
full_domain = parsed.netloc.lower()

print("\nDomain:", full_domain)

risk = 0

parts = full_domain.split(".")
if len(parts) > 2:
    domain = ".".join(parts[-2:])
else:
    domain = full_domain


# ======================
# IP INFO
# ======================

print("\n=== IP INFO ===")

ip = None

try:
    ip = socket.gethostbyname(full_domain)
    print("IP Address:", ip)
except:
    print("Could not resolve IP")


# ======================
# REDIRECT CHECK
# ======================

print("\n=== REDIRECT CHECK ===")

try:
    r = requests.get(url, timeout=5)
    final_url = r.url

    if final_url != url:
        print("⚠ Redirect detected")
        print("Final destination:", final_url)
        risk += 10
    else:
        print("No redirect detected")

except:
    print("Could not check redirect")


# ======================
# DOMAIN TRUST CHECK
# ======================

trusted_domains = [
    "google.com",
    "facebook.com",
    "amazon.com",
    "temu.com",
    "microsoft.com"
]

print("\n=== DOMAIN TRUST CHECK ===")

trusted = False

for legit in trusted_domains:
    if full_domain == legit or full_domain.endswith("." + legit):
        trusted = True

if trusted:
    print("Trusted domain or subdomain detected ✅")
else:
    print("Unknown domain ⚠")


# ======================
# HOSTING CHECK
# ======================

print("\n=== HOSTING CHECK ===")

free_hosts = [
    "onrender.com",
    "netlify.app",
    "vercel.app",
    "github.io",
    "firebaseapp.com",
    "pages.dev"
]

for host in free_hosts:
    if full_domain.endswith(host):
        print("⚠ Hosted on free developer platform:", host)
        risk += 15


# ======================
# DOMAIN AGE CHECK
# ======================

print("\n=== DOMAIN AGE CHECK ===")

try:
    w = whois.whois(domain)
    creation = w.creation_date

    if isinstance(creation, list):
        creation = creation[0]

    if creation:
        age = (datetime.now() - creation).days
        print("Domain age:", age, "days")

        if age < 30:
            print("⚠ Very new domain")
            risk += 60
        elif age < 180:
            print("⚠ Recently created domain")
            risk += 30

except:
    print("WHOIS data unavailable")


# ======================
# PHISHING PATTERN CHECK
# ======================

print("\n=== PHISHING PATTERN CHECK ===")

if "-" in full_domain and not trusted:
    print("⚠ Hyphen in domain")
    risk += 10

if full_domain.count(".") > 3:
    print("⚠ Too many subdomains")
    risk += 10


# ======================
# WEBSITE CONTENT CHECK
# ======================

print("\n=== WEBSITE CONTENT ANALYSIS ===")

try:
    page = requests.get(url, timeout=5).text.lower()

    if "<input" in page and "password" in page:
        print("⚠ Login/password form detected")
        risk += 30

    if ".apk" in page or ".exe" in page or ".zip" in page:
        print("⚠ Suspicious download link detected")
        risk += 20

except:
    print("Could not analyze webpage")


# ======================
# ABUSEIPDB CHECK
# ======================

print("\n=== ABUSEIPDB CHECK ===")

ABUSE_API_KEY = "d96c4689c2853411074e24a550abef459f023ff615912db16f150d36a93b2f5d3068b4856753c5ad"

if ip:
    headers = {
        "Key": ABUSE_API_KEY,
        "Accept": "application/json"
    }

    try:
        r = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers=headers,
            params={"ipAddress": ip}
        )

        data = r.json()["data"]
        score = data["abuseConfidenceScore"]

        print("Abuse score:", score)

        if score > 50:
            print("⚠ IP reported for malicious activity")
            risk += 30

    except:
        print("AbuseIPDB check failed")


# ======================
# VIRUSTOTAL SCAN
# ======================

print("\n=== VIRUSTOTAL SCAN ===")

VT_API_KEY = "e45db56bc90d45cb7d520eadd8d1d753a178afd6336fab7f5ab91615d36964c3"

headers = {
    "x-apikey": VT_API_KEY
}

try:
    r = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data={"url": url}
    )

    if r.status_code == 200:
        print("URL submitted to VirusTotal")

except:
    print("VirusTotal scan failed")


# ======================
# URLSCAN SUBMISSION
# ======================

print("\n=== URLSCAN MALWARE ANALYSIS ===")

URLSCAN_API = "019ce670-581a-77ac-96e8-ae4da84ab194"

headers = {
    "API-Key": URLSCAN_API,
    "Content-Type": "application/json"
}

data = {
    "url": url,
    "visibility": "public"
}

try:
    response = requests.post(
        "https://urlscan.io/api/v1/scan/",
        headers=headers,
        json=data
    )

    result = response.json()

    print("Scan submitted successfully!")
    print("Result page:", result["result"])

except:
    print("URLScan submission failed")


# ======================
# FINAL SCORE
# ======================

print("\n=== SECURITY RISK SCORE ===")

print("Risk score:", risk, "/100")

print("\n=== FINAL VERDICT ===")

if risk < 20:
    print("SAFE ✅")
elif risk < 50:
    print("SUSPICIOUS ⚠")
else:
    print("POSSIBLE PHISHING 🚨")
