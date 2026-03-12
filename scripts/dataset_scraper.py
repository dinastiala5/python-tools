import requests
from bs4 import BeautifulSoup
import csv

print("\n--- Dataset Web Scraper ---\n")

url = input("Enter website URL: ")

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

title = soup.title.string if soup.title else "No Title"

links = soup.find_all("a")

with open("links_dataset.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Page Title", "Link"])

    for link in links:
        href = link.get("href")
        if href:
            writer.writerow([title, href])

print("\nDataset saved to links_dataset.csv")
