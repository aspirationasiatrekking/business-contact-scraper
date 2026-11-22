
import requests

from .base import SearchProvider, SearchResult


class SearchManager:

    def __init__(
        self,
        primary_provider: SearchProvider,
        fallback_provider: SearchProvider
    ):
        self.primary_provider = primary_provider
        self.fallback_provider = fallback_provider

    def search(
        self,
        query: str,
        max_results: int = 10
    ) -> list[SearchResult]:

        try:
            print("Searching with primary provider...")

            results = self.primary_provider.search(
                query,
                max_results
            )

            print("Primary provider successful.")

            return results

        except (requests.RequestException, ValueError) as error:

            print(f"Primary provider failed: {error}")
            print("Switching to fallback provider...")

            results = self.fallback_provider.search(
                query,
                max_results
            )

            print("Fallback provider successful.")

            return results
