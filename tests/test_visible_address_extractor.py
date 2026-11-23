
import requests
from bs4 import BeautifulSoup

from extractors.address_extractor import extract_visible_address


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

address = extract_visible_address(soup)

print("Extracted visible address:")
print(address)
