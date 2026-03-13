import requests

print("=== SHORT LINK EXPANDER ===")

url = input("Enter shortened URL: ")

try:
    response = requests.get(url, allow_redirects=True, timeout=10)

    print("\nOriginal short link:", url)
    print("Final destination:", response.url)

    if response.url != url:
        print("\n⚠ The link redirects to another website.")
    else:
        print("\nNo redirect detected.")

except Exception as e:
    print("Error:", e)
