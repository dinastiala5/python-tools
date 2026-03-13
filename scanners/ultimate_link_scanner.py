import requests
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime

print("=== ULTIMATE CYBER LINK SCANNER ===")

# ========================
# API KEYS (Already Added)
# ========================

VT_API = "e45db56bc90d45cb7d520eadd8d1d753a178afd6336fab7f5ab91615d36964c3"
ABUSE_API = "d96c4689c2853411074e24a550abef459f023ff615912db16f150d36a93b2f5d3068b4856753c5ad"
URLSCAN_API = "019ce670-581a-77ac-96e8-ae4da84ab194"

# ========================
# INPUT
# ========================

url = input("Enter URL to scan: ")

if not url.startswith("http"):
    url = "http://" + url

parsed = urlparse(url)
domain = parsed.netloc

print("\nDomain:", domain)

risk = 0

# ========================
# IP INFO
# ========================

print("\n=== IP INFO ===")

try:
    ip = socket.gethostbyname(domain)
    print("IP Address:", ip)
except:
    ip = None
    print("Could not resolve IP")
# ========================
# SERVER LOCATION
# ========================

print("\n=== SERVER LOCATION ===")

try:
    geo = requests.get(f"https://ipinfo.io/{ip}/json").json()

    country = geo.get("country")
    city = geo.get("city")
    org = geo.get("org")

    print("Country:", country)
    print("City:", city)
    print("Hosting provider:", org)

except:
    print("Could not detect server location")
# ========================
# TRUSTED DOMAIN CHECK
# ========================

trusted = [
"google.com",
"facebook.com",
"amazon.com",
"temu.com",
"paypal.com",
"microsoft.com"
]

print("\n=== DOMAIN TRUST CHECK ===")

safe = False

for t in trusted:
    if domain == t or domain.endswith("." + t):
        safe = True

if safe:
    print("Trusted domain or subdomain detected ✅")
else:
    print("Unknown domain ⚠")
    risk += 10

# ========================
# HOSTING CHECK
# ========================

print("\n=== HOSTING CHECK ===")

free_hosts = [
"onrender.com",
"netlify.app",
"vercel.app",
"github.io",
"firebaseapp.com"
]

for h in free_hosts:
    if domain.endswith(h):
        print("⚠ Hosted on free developer platform:", h)
        risk += 15

# ========================
# DOMAIN AGE
# ========================

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
print("\n=== DOMAIN REGISTRAR ===")

try:
    registrar = w.registrar
    print("Registrar:", registrar)
except:
    print("Registrar info unavailable")
# ========================
# PHISHING PATTERNS
# ========================

print("\n=== PHISHING PATTERN CHECK ===")

shorteners = [
"bit.ly",
"tinyurl.com",
"t.co",
"goo.gl",
"rb.gy"
]

for s in shorteners:
    if s in url:
        print("⚠ Shortened link detected:", s)
        risk += 20

if "-" in domain and not safe:
    print("⚠ Hyphen in domain")
    risk += 10

if domain.count(".") > 3:
    print("⚠ Too many subdomains")
    risk += 10
# Typosquatting detection

fake_brands = [
"paypaI",
"faceb00k",
"micr0soft",
"go0gle",
"amaz0n"
]

for f in fake_brands:
    if f in domain:
        print("🚨 Possible typosquatting domain detected:", f)
        risk += 40
# ========================
# WEBSITE CONTENT
# ========================

print("\n=== WEBSITE CONTENT ANALYSIS ===")

try:
    page = requests.get(url, timeout=5).text.lower()

    if "password" in page and "<input" in page:
        print("⚠ Login form detected")
        risk += 25

    if "paypal" in page and "paypal.com" not in domain:
        print("🚨 Possible PayPal phishing")
        risk += 50

    if "facebook" in page and "facebook.com" not in domain:
        print("🚨 Possible Facebook phishing")
        risk += 50

except:
    print("Could not analyze page")
# ========================
# REDIRECT CHECK
# ========================

print("\n=== REDIRECT CHECK ===")

try:
    response = requests.get(url, timeout=5, allow_redirects=True)

    if len(response.history) > 0:
        print("⚠ Redirect chain detected")

        for r in response.history:
            print("Redirect:", r.url)

        print("Final destination:", response.url)

        risk += 15
    else:
        print("No redirect detected")

except:
    print("Could not check redirects")
# ========================
# ABUSEIPDB
# ========================

if ip:

    print("\n=== ABUSEIPDB CHECK ===")

    try:
        headers = {
        "Key": ABUSE_API,
        "Accept": "application/json"
        }

        params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
        }

        r = requests.get(
        "https://api.abuseipdb.com/api/v2/check",
        headers=headers,
        params=params
        )

        data = r.json()

        score = data["data"]["abuseConfidenceScore"]

        print("Abuse score:", score)

        if score > 50:
            risk += 40

    except:
        print("AbuseIPDB check failed")

# ========================
# VIRUSTOTAL
# ========================

print("\n=== VIRUSTOTAL SCAN ===")

try:

    headers = {
    "x-apikey": VT_API
    }

    params = {
    "url": url
    }

    r = requests.post(
    "https://www.virustotal.com/api/v3/urls",
    headers=headers,
    data=params
    )

    print("URL submitted to VirusTotal")

except:
    print("VirusTotal scan failed")

# ========================
# URLSCAN
# ========================

print("\n=== URLSCAN MALWARE ANALYSIS ===")

try:

    headers = {
    "API-Key": URLSCAN_API,
    "Content-Type": "application/json"
    }

    data = {
    "url": url,
    "visibility": "public"
    }

    r = requests.post(
    "https://urlscan.io/api/v1/scan/",
    headers=headers,
    json=data
    )

    result = r.json()

    print("Scan submitted successfully!")
    print("Result page:", result["result"])

except:
    print("URLScan submission failed")

# ========================
# FINAL SCORE
# ========================
# ========================
# SSL CERTIFICATE CHECK
# ========================

import ssl

print("\n=== SSL CERTIFICATE CHECK ===")

try:
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
        s.settimeout(5)
        s.connect((domain, 443))
        cert = s.getpeercert()

    expire_date = cert['notAfter']
    print("Certificate expires:", expire_date)

except:
    print("⚠ Could not verify SSL certificate")
print("\n=== SECURITY RISK SCORE ===")

print("Risk score:", risk, "/100")
print("\n=== THREAT LEVEL ===")

if risk < 10:
    print("VERY SAFE 🟢")

elif risk < 30:
    print("LOW RISK 🟡")

elif risk < 60:
    print("SUSPICIOUS 🟠")

else:
    print("HIGH RISK 🔴")
print("\n=== FINAL VERDICT ===")

if risk < 20:
    print("SAFE ✅")
elif risk < 50:
    print("SUSPICIOUS ⚠")
else:
    print("POSSIBLE PHISHING 🚨")
