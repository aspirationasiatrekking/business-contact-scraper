
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

        url = "https://google.serper.dev/search"

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query,
            "num": max_results,
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

        results = []

        for item in data.get("organic", []):

            result = SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                provider="serper"
            )

            results.append(result)

        return results
