from search.result_classifier import classify_result
from search.serper_provider import SerperSearchProvider


provider = SerperSearchProvider()

results = provider.search(
    "Trekking companies in Nepal",
    max_results=10
)

for result in results:

    category = classify_result(result)

    print(f"\nTitle: {result.title}")
    print(f"Category: {category}")
    print(f"URL: {result.url}")
    print(f"Snippet: {result.snippet}")