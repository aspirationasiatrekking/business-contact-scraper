
from search.ddgs_provider import DDGSSearchProvider
from search.serper_provider import SerperSearchProvider
from search.manager import SearchManager


import requests

class FailingSearchProvider:

    def search(self, query, max_results=10):
        raise requests.ConnectionError("Simulated network failure")

serper = FailingSearchProvider()
ddgs = DDGSSearchProvider()

manager = SearchManager(
    primary_provider=serper,
    fallback_provider=ddgs
)

results = manager.search(
    "Trekking companies in Nepal",
    max_results=5
)

print(f"\nTotal results: {len(results)}")

for result in results:
    print("\nTitle:", result.title)
    print("URL:", result.url)
    print("Provider:", result.provider)
