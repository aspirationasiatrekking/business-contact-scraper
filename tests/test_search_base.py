from search.ddgs_provider import DDGSSearchProvider


provider = DDGSSearchProvider()

results = provider.search(
    "Trekking companies in Nepal",
    max_results=5
)

print(f"\nFound {len(results)} results")

for result in results:
    print("\nTitle:", result.title)
    print("URL:", result.url)
    print("Snippet:", result.snippet)
    print("Provider:", result.provider)