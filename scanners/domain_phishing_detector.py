from urllib.parse import urlparse
import whois
from datetime import datetime

print("=== DOMAIN PHISHING DETECTOR ===")

url = input("Enter URL: ")

if not url.startswith("http"):
    url = "http://" + url

parsed = urlparse(url)
full_domain = parsed.netloc.lower()

print("\nDomain:", full_domain)

risk = 0

# Extract main domain for WHOIS
parts = full_domain.split(".")
if len(parts) > 2:
    domain = ".".join(parts[-2:])
else:
    domain = full_domain

# Trusted domains list
trusted_domains = [
    "temu.com",
    "google.com",
    "facebook.com",
    "amazon.com",
    "microsoft.com",
    "apple.com"
]

# Check trusted domains or subdomains
trusted = False
for legit in trusted_domains:
    if full_domain == legit or full_domain.endswith("." + legit):
        trusted = True

if trusted:
    print("Trusted domain or subdomain detected ✅")
else:
    print("Unknown domain ⚠")

# Detect free hosting platforms
print("\nChecking hosting platform...")

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
        print("Manual inspection recommended")
        risk += 15

# WHOIS domain age check
print("\nChecking domain age...")

try:
    w = whois.whois(domain)
    creation = w.creation_date

    if isinstance(creation, list):
        creation = creation[0]

    if creation:
        age_days = (datetime.now() - creation).days
        print("Domain age:", age_days, "days")

        if age_days < 30:
            print("⚠ Very new domain")
            risk += 60
        elif age_days < 180:
            print("⚠ Recently created domain")
            risk += 30

except:
    print("WHOIS data unavailable")

# Suspicious patterns
if "-" in full_domain and not trusted:
    print("⚠ Hyphen in domain")
    risk += 10

if full_domain.count(".") > 3:
    print("⚠ Too many subdomains")
    risk += 10

# Final result
print("\nRisk score:", risk, "/100")

print("\n=== FINAL VERDICT ===")

if risk < 20:
    print("SAFE ✅")
elif risk < 50:
    print("SUSPICIOUS ⚠")
else:
    print("POSSIBLE PHISHING 🚨")
