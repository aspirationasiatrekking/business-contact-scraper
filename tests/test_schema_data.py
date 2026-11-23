
import requests
from bs4 import BeautifulSoup


url = "https://www.nepalhikingteam.com/"

response = requests.get(
    url,
    timeout=15,
    headers={"User-Agent": "Mozilla/5.0"}
)

response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

schema_scripts = soup.find_all(
    "script",
    type="application/ld+json"
)

print("JSON-LD scripts found:", len(schema_scripts))

for index, script in enumerate(schema_scripts, start=1):

    print(f"\n========== SCRIPT {index} ==========")

    print(script.get_text(strip=True))

