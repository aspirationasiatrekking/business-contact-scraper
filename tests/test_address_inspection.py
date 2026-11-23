
import json
import requests
from bs4 import BeautifulSoup


url = "https://nepalguidetrekking.com/"

response = requests.get(
    url,
    timeout=15,
    headers={"User-Agent": "Mozilla/5.0"}
)

response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

scripts = soup.find_all(
    "script",
    type="application/ld+json"
)

print(f"Found {len(scripts)} JSON-LD scripts")

for index, script in enumerate(scripts, start=1):

    try:
        data = json.loads(script.get_text(strip=True))

        print(f"\n========== SCRIPT {index} ==========")
        print(json.dumps(data, indent=4, ensure_ascii=False))

    except json.JSONDecodeError:
        print(f"Invalid JSON-LD in script {index}")
