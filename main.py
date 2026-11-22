
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

def search_web(query):
    with DDGS(timeout=30) as search:
        return search.text(query, max_results=10)

def scrape_website(url):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        title = (
            soup.title.get_text(strip=True)
            if soup.title else "No title found"
        )

        text_content = soup.get_text(
            separator="\n",
            strip=True
        )

        return {
            "website": url,
            "title": title,
            "text": text_content[:500]
        }

    except requests.RequestException as error:
        print(f"Failed: {url} - {error}")
        return None


query = input("Enter your search query: ")

results = search_web(query)

print(f"\nFound {len(results)} search results")

companies = []

for result in results:
    url = result.get("href")

    if not url:
        continue

    print(f"\nScraping: {url}")

    data = scrape_website(url)

    if data:
        companies.append(data)

print(f"\nSuccessfully scraped {len(companies)} websites")

for company in companies:
    print("\nTitle:", company["title"])
    print("Website:", company["website"])
    print("Text:", company["text"][:200])
