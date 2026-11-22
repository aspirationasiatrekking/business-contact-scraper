
from ddgs import DDGS
from ddgs.exceptions import DDGSException

query = input("Enter your search query: ")

try:
    with DDGS(timeout=30) as search:
        results = search.text(
            query,
            max_results=10,
            region="wt-wt"
        )

    print(f"\nFound {len(results)} results")

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Title:", result.get("title"))
        print("URL:", result.get("href"))
        print("Description:", result.get("body"))

except DDGSException as error:
    print("Search failed:", error)
