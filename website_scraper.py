import requests
from bs4 import BeautifulSoup

url = "https://example.com"
response = requests.get(url, timeout=10)

soup = BeautifulSoup(response.content, "html.parser")

text_content = soup.get_text(separator="\n", strip=True)
title = soup.title.string if soup.title else "No title found"

print("Title:", title)
print("Text content:", text_content[:500]) 