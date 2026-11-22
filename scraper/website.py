

import requests
from bs4 import BeautifulSoup
from extractors.contacts import extract_emails

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
        emails = extract_emails(text_content)

        return {
            "website": response.url,
            "title": title,
            "text": text_content[:500],
            "emails": emails
        }

    except requests.RequestException as error:
        print(f"Failed: {url} - {error}")
        return None