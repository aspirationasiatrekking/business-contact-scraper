from search.manager import SearchManager
from search.serper_provider import SerperSearchProvider
from search.ddgs_provider import DDGSSearchProvider
from scraper.website import scrape_website


def main():
    query = input("Enter your search query: ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    # Initialize search provider
    search_provider = DDGSSearchProvider()

    # Search for businesses
    results = search_provider.search(query, max_results=10)

    print(f"\nFound {len(results)} search results")

    companies = []
    failed_websites = []

    for result in results:

        # SearchResult is a dataclass, so use dot notation
        url = result.url

        if not url:
            continue

        print(f"\nScraping: {url}")

        try:
            data = scrape_website(url)

            if data:
                companies.append(data)
            else:
                failed_websites.append(url)

        except Exception as error:
            print(f"Failed: {url} | {error}")
            failed_websites.append(url)

    print("\n========== SUMMARY ==========")
    print(f"Successfully scraped: {len(companies)}")
    print(f"Failed websites: {len(failed_websites)}")

    for company in companies:
        print("\nTitle:", company.get("title"))
        print("Website:", company.get("website"))
        print("Emails:", company.get("emails"))


if __name__ == "__main__":
    main()
