from ddgs import DDGS
from ddgs.exceptions import DDGSException

from .base import SearchProvider, SearchResult


class DDGSSearchProvider(SearchProvider):

    def search(self, query: str, max_results: int = 10) -> list[SearchResult]:

        try:
            with DDGS(timeout=30) as ddgs:
                raw_results = ddgs.text(
                    query,
                    max_results=max_results,
                    region="wt-wt"
                )

            results = []

            for item in raw_results:
                result = SearchResult(
                    title=item.get("title", ""),
                    url=item.get("href", ""),
                    snippet=item.get("body", ""),
                    provider="ddgs"
                )

                results.append(result)

            return results

        except DDGSException as error:
            print(f"DDGS search error: {error}")
            return []