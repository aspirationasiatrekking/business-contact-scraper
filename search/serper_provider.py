
import os
import requests

from dotenv import load_dotenv

from .base import SearchProvider, SearchResult


load_dotenv()


class SerperSearchProvider(SearchProvider):

    
    def search(self, query: str, max_results: int = 10) -> list[SearchResult]:

        api_key = os.getenv("SERPER_API_KEY")

        if not api_key:
            raise ValueError("SERPER_API_KEY not found in .env")

        if max_results <= 0:
            return []

        url = "https://google.serper.dev/search"

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        page_size = 10
        results = []
        seen_urls = set()

        # Calculate how many pages we need
        total_pages = (max_results + page_size - 1) // page_size

        for page in range(1, total_pages + 1):

            print(f"Fetching search page {page}/{total_pages}...")

            payload = {
                "q": query,
                "num": page_size,
                "page": page,
                "gl": "np",
                "hl": "en"
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            organic_results = data.get("organic", [])

            if not organic_results:
                print("No more search results.")
                break

            for item in organic_results:

                result_url = item.get("link", "")

                # Skip empty or duplicate URLs
                if not result_url or result_url in seen_urls:
                    continue

                seen_urls.add(result_url)

                result = SearchResult(
                    title=item.get("title", ""),
                    url=result_url,
                    snippet=item.get("snippet", ""),
                    provider="serper"
                )

                results.append(result)

                if len(results) >= max_results:
                    break

            if len(results) >= max_results:
                break

        return results
