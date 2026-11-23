
import requests
from bs4 import BeautifulSoup


url = "https://easternlighttrek.com/contact-us/"

response = requests.get(
    url,
    timeout=15,
    headers={"User-Agent": "Mozilla/5.0"}
)

response.raise_for_status()

soup = BeautifulSoup(
    response.content,
    "html.parser"
)

# Find text containing the business location
for element in soup.find_all(string=True):

    text = element.strip()

    if "Lakeside" in text:

        print("\nFound location text:")
        print(text)

        print("\nParent HTML:")
        print(element.parent.prettify())

