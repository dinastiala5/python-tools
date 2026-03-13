import requests

print("=== URLSCAN LINK SCANNER ===")

url = input("Enter URL: ")

API_KEY = "019ce670-581a-77ac-96e8-ae4da84ab194"

headers = {
    "API-Key": API_KEY,
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

    print("\nScan submitted successfully!")

    print("Scan ID:", result.get("uuid"))
    print("Result page:", result.get("result"))
    print("Screenshot:", result.get("screenshot"))

    print("\nOpen the result page to see:")
    print("- Malware detection")
    print("- Phishing behavior")
    print("- Network activity")
    print("- Website reputation")

except Exception as e:
    print("Error:", e)
